#!/usr/bin/env python3
"""
RAG Knowledge Builder - Ingest textbook markdown files into Qdrant vector database.

This script scans all markdown files in the /docs folder, splits them into semantic
chunks, generates embeddings using OpenAI, and stores vectors in Qdrant.

Usage:
    python ingest_book.py              # Full ingestion
    python ingest_book.py --rebuild    # Delete and recreate collection
    python ingest_book.py --stats      # Show collection statistics
    python ingest_book.py --dry-run    # Preview without ingesting
"""

import os
import sys
import hashlib
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

import dotenv
from openai import OpenAI, RateLimitError
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from tqdm import tqdm

# Load environment variables
dotenv.load_dotenv()


class TextbookIngestor:
    """Handles ingestion of textbook markdown files into Qdrant."""

    def __init__(self, collection_name: str = "textbook_knowledge"):
        """Initialize the ingestor with OpenAI and Qdrant clients."""
        self.collection_name = collection_name
        self.vector_size = 1536  # text-embedding-ada-002 dimension
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.openai_client = OpenAI(api_key=api_key)
        
        # Initialize Qdrant client
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        if not qdrant_url:
            raise ValueError("QDRANT_URL not found in environment")
        
        self.qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            timeout=30,
            prefer_grpc=False,
            check_compatibility=False
        )
        
        print(f"✓ Connected to Qdrant: {qdrant_url}")
        print(f"✓ OpenAI client initialized")
        
        # Test connection
        try:
            self.qdrant_client.get_collections()
            print(f"✓ Qdrant connection verified")
        except Exception as e:
            print(f"⚠ Qdrant connection test failed: {e}")
            print(f"  Continuing anyway...")

    def create_collection(self, rebuild: bool = False) -> None:
        """Create the Qdrant collection if it doesn't exist."""
        try:
            collections = self.qdrant_client.get_collections().collections
            collection_names = [c.name for c in collections]
        except Exception:
            # If we can't get collections, assume collection doesn't exist
            collection_names = []
        
        if self.collection_name in collection_names:
            if rebuild:
                print(f"⚠ Deleting existing collection: {self.collection_name}")
                self.qdrant_client.delete_collection(self.collection_name)
                print(f"✓ Collection deleted")
            else:
                print(f"✓ Collection '{self.collection_name}' already exists")
                return
        
        print(f"Creating collection: {self.collection_name}")
        self.qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE
            ),
            hnsw_config={
                "m": 16,
                "ef_construct": 100,
            }
        )
        print(f"✓ Collection created successfully")

    def parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract frontmatter metadata from markdown content."""
        metadata = {}
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.strip().split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        metadata[key.strip()] = value.strip().strip('"\'')
        
        return metadata

    def split_by_headings(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Split markdown content by H2 headings into semantic chunks."""
        chunks = []
        metadata = self.parse_frontmatter(content)
        
        # Remove frontmatter from content
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2]
        
        lines = content.split("\n")
        current_section = {
            "title": metadata.get("title", Path(file_path).stem),
            "content": [],
            "level": 0
        }
        
        for i, line in enumerate(lines):
            if line.startswith("## "):
                # Save previous section if it has content
                if current_section["content"]:
                    chunks.append({
                        "section_name": current_section["title"],
                        "content": "\n".join(current_section["content"]).strip(),
                        "heading_level": 2
                    })
                
                # Start new section
                current_section = {
                    "title": line[3:].strip(),
                    "content": [],
                    "level": 2
                }
            elif line.startswith("### "):
                # H3 - subsection
                if current_section["content"]:
                    chunks.append({
                        "section_name": current_section["title"],
                        "content": "\n".join(current_section["content"]).strip(),
                        "heading_level": 2
                    })
                
                current_section = {
                    "title": line[4:].strip(),
                    "content": [],
                    "level": 3
                }
            else:
                current_section["content"].append(line)
        
        # Don't forget the last section
        if current_section["content"]:
            chunks.append({
                "section_name": current_section["title"],
                "content": "\n".join(current_section["content"]).strip(),
                "heading_level": current_section["level"]
            })
        
        # Add chapter title from frontmatter or filename
        chapter_title = metadata.get("title", metadata.get("sidebar_label", Path(file_path).stem))
        
        for chunk in chunks:
            chunk["chapter_title"] = chapter_title
            chunk["page_url"] = f"/docs/{Path(file_path).stem}"
        
        return chunks

    def filter_chunk(self, content: str, min_length: int = 50, max_length: int = 2000) -> bool:
        """Check if chunk meets length requirements."""
        return min_length <= len(content) <= max_length

    def generate_embedding(self, text: str, max_retries: int = 3) -> Optional[List[float]]:
        """Generate embedding for text with retry logic."""
        for attempt in range(max_retries):
            try:
                response = self.openai_client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=text
                )
                return response.data[0].embedding
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    import time
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"⏳ Rate limit hit, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"✗ Failed after {max_retries} retries: {e}")
                    return None
            except Exception as e:
                print(f"✗ Embedding error: {e}")
                return None
        
        return None

    def generate_chunk_id(self, file_path: str, section_name: str, chunk_index: int) -> str:
        """Generate unique ID for a chunk using hash."""
        unique_string = f"{file_path}:{section_name}:{chunk_index}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def ingest_file(self, file_path: str, dry_run: bool = False) -> Tuple[int, int]:
        """
        Ingest a single markdown file.
        
        Returns:
            Tuple of (chunks_created, chunks_ingested)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"✗ Error reading {file_path}: {e}")
            return 0, 0
        
        # Split into chunks
        chunks = self.split_by_headings(content, file_path)
        
        # Filter chunks
        valid_chunks = [c for c in chunks if self.filter_chunk(c["content"])]
        
        if not valid_chunks:
            print(f"⚠ No valid chunks in {file_path}")
            return len(chunks), 0
        
        if dry_run:
            print(f"📄 {file_path}: {len(valid_chunks)} chunks would be ingested")
            return len(chunks), len(valid_chunks)
        
        # Prepare points for Qdrant
        points = []
        for i, chunk in enumerate(valid_chunks):
            # Generate embedding
            embedding = self.generate_embedding(chunk["content"])
            if not embedding:
                continue
            
            # Create point ID
            point_id = self.generate_chunk_id(file_path, chunk["section_name"], i)
            
            # Create payload
            payload = {
                "text": chunk["content"],
                "chapter_title": chunk["chapter_title"],
                "section_name": chunk["section_name"],
                "page_url": chunk["page_url"],
                "heading_level": chunk["heading_level"],
                "chunk_index": i,
                "total_chunks": len(valid_chunks),
                "source_file": str(file_path),
                "ingested_at": datetime.now().isoformat()
            }
            
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload
            )
            points.append(point)
        
        # Upsert to Qdrant
        if points:
            try:
                self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                print(f"✓ {file_path}: Ingested {len(points)}/{len(valid_chunks)} chunks")
                return len(chunks), len(points)
            except Exception as e:
                print(f"✗ Error upserting {file_path}: {e}")
                return len(chunks), 0
        
        return len(chunks), 0

    def ingest_directory(self, docs_dir: str, dry_run: bool = False) -> Dict[str, int]:
        """
        Ingest all markdown files from a directory.
        
        Returns:
            Statistics dictionary
        """
        docs_path = Path(docs_dir)
        
        if not docs_path.exists():
            raise FileNotFoundError(f"Docs directory not found: {docs_dir}")
        
        markdown_files = list(docs_path.rglob("*.md"))
        
        if not markdown_files:
            print(f"⚠ No markdown files found in {docs_dir}")
            return {"files": 0, "chunks_created": 0, "chunks_ingested": 0}
        
        print(f"\n📚 Found {len(markdown_files)} markdown files")
        print("=" * 60)
        
        stats = {"files": 0, "chunks_created": 0, "chunks_ingested": 0}
        
        for file_path in tqdm(markdown_files, desc="Processing files"):
            chunks_created, chunks_ingested = self.ingest_file(str(file_path), dry_run)
            stats["files"] += 1
            stats["chunks_created"] += chunks_created
            stats["chunks_ingested"] += chunks_ingested
        
        return stats

    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        try:
            info = self.qdrant_client.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "vector_count": info.points_count,
                "vectors_size": info.config.params.vectors.size,
                "distance": info.config.params.vectors.distance,
                "status": info.status
            }
        except Exception as e:
            return {"error": str(e)}

    def close(self):
        """Close connections."""
        if hasattr(self, 'qdrant_client'):
            self.qdrant_client.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Ingest textbook markdown files into Qdrant for RAG"
    )
    parser.add_argument(
        "--docs-dir",
        type=str,
        default="docs",
        help="Directory containing markdown files (default: docs)"
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="textbook_knowledge",
        help="Qdrant collection name (default: textbook_knowledge)"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Delete and recreate collection"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview ingestion without actually ingesting"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show collection statistics and exit"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📖 RAG Knowledge Builder")
    print("=" * 60)
    
    try:
        ingestor = TextbookIngestor(collection_name=args.collection)
        
        # Show stats only
        if args.stats:
            stats = ingestor.get_stats()
            print("\n📊 Collection Statistics:")
            print("-" * 40)
            for key, value in stats.items():
                print(f"  {key}: {value}")
            ingestor.close()
            return
        
        # Create collection
        if not args.dry_run:
            ingestor.create_collection(rebuild=args.rebuild)
        
        # Ingest files
        stats = ingestor.ingest_directory(args.docs_dir, dry_run=args.dry_run)
        
        # Print summary
        print("\n" + "=" * 60)
        if args.dry_run:
            print("🔍 DRY RUN - No data was ingested")
            print(f"   Files scanned: {stats['files']}")
            print(f"   Chunks that would be created: {stats['chunks_created']}")
            print(f"   Chunks that would be ingested: {stats['chunks_ingested']}")
        else:
            print("✅ Ingestion Complete!")
            print(f"   Files processed: {stats['files']}")
            print(f"   Chunks created: {stats['chunks_created']}")
            print(f"   Chunks ingested: {stats['chunks_ingested']}")
            
            # Show final stats
            final_stats = ingestor.get_stats()
            print(f"\n📊 Collection Info:")
            print(f"   Total vectors: {final_stats.get('vector_count', 'N/A')}")
        
        print("=" * 60)
        
        ingestor.close()
        
    except ValueError as e:
        print(f"\n✗ Configuration error: {e}")
        print("\nMake sure your .env file contains:")
        print("  OPENAI_API_KEY=your_key")
        print("  QDRANT_URL=your_qdrant_url")
        print("  QDRANT_API_KEY=your_qdrant_key")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
