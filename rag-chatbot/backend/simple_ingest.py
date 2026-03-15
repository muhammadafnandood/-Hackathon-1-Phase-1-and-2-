#!/usr/bin/env python3
"""
Simple RAG Ingestor - Creates a local SQLite-based vector store for testing.

This script provides a fallback when Qdrant Cloud is not available.
It uses SQLite with sentence-transformers for local vector storage.
"""

import os
import sys
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

import dotenv

dotenv.load_dotenv()

# Check if we can use sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    print("⚠ sentence-transformers not installed. Using simple text storage.")
    print("  Install with: pip install sentence-transformers")

import sqlite3


class SimpleVectorStore:
    """Simple SQLite-based vector store for testing."""
    
    def __init__(self, db_path: str = "vector_store.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
        
        # Initialize embedding model if available
        if HAS_SENTENCE_TRANSFORMERS:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.embedding_dim = 384
            print(f"✓ Using sentence-transformers (dim={self.embedding_dim})")
        else:
            self.model = None
            self.embedding_dim = 0
            print("✓ Using simple text storage (no embeddings)")
    
    def _create_tables(self):
        """Create database tables."""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                chapter_title TEXT,
                section_name TEXT,
                page_url TEXT,
                heading_level INTEGER,
                chunk_index INTEGER,
                source_file TEXT,
                ingested_at TEXT,
                embedding BLOB
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection_info (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        self.conn.commit()
    
    def generate_id(self, file_path: str, section_name: str, chunk_index: int) -> str:
        """Generate unique ID for a chunk."""
        unique_string = f"{file_path}:{section_name}:{chunk_index}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    def add_chunk(self, chunk: Dict[str, Any]):
        """Add a chunk to the store."""
        cursor = self.conn.cursor()
        
        # Generate embedding if model available
        embedding = None
        if self.model:
            embedding = self.model.encode(chunk['text']).tobytes()
        
        cursor.execute('''
            INSERT OR REPLACE INTO chunks 
            (id, text, chapter_title, section_name, page_url, heading_level, 
             chunk_index, source_file, ingested_at, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            chunk['id'],
            chunk['text'],
            chunk['chapter_title'],
            chunk['section_name'],
            chunk['page_url'],
            chunk['heading_level'],
            chunk['chunk_index'],
            chunk['source_file'],
            chunk['ingested_at'],
            embedding
        ))
        
        self.conn.commit()
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant chunks using keyword matching."""
        cursor = self.conn.cursor()
        
        # Simple keyword-based search
        query_words = query.lower().split()
        
        cursor.execute('SELECT * FROM chunks')
        chunks = cursor.fetchall()
        
        results = []
        for chunk in chunks:
            text = chunk[1].lower()
            chapter = chunk[2].lower() if chunk[2] else ""
            section = chunk[3].lower() if chunk[3] else ""
            
            # Count matching words
            matches = sum(1 for word in query_words if word in text or word in chapter or word in section)
            
            if matches > 0:
                # Score based on number of matches and text length
                score = matches / len(query_words)
                results.append({
                    'text': chunk[1],
                    'chapter_title': chunk[2],
                    'section_name': chunk[3],
                    'page_url': chunk[4],
                    'score': score,
                    'chunk_index': chunk[6],
                    'heading_level': chunk[5]
                })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics."""
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM chunks')
        count = cursor.fetchone()[0]
        
        return {
            'collection_name': 'local_vector_store',
            'vector_count': count,
            'embedding_dim': self.embedding_dim,
            'using_embeddings': HAS_SENTENCE_TRANSFORMERS
        }
    
    def close(self):
        """Close database connection."""
        self.conn.close()


class SimpleIngestor:
    """Simple ingestor for local vector store."""
    
    def __init__(self, db_path: str = "vector_store.db"):
        self.store = SimpleVectorStore(db_path)
    
    def split_by_headings(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Split markdown content by H2 headings."""
        chunks = []
        lines = content.split("\n")
        current_section = {
            "title": Path(file_path).stem,
            "content": []
        }
        
        # Extract title from frontmatter if present
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.strip().split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        if key.strip() == "title":
                            current_section["title"] = value.strip().strip('"\'')
                
                content = parts[2]
        
        for line in lines:
            if line.startswith("## "):
                if current_section["content"]:
                    chunks.append({
                        "section_name": current_section["title"],
                        "content": "\n".join(current_section["content"]).strip()
                    })
                
                current_section = {
                    "title": line[3:].strip(),
                    "content": []
                }
            else:
                current_section["content"].append(line)
        
        # Don't forget the last section
        if current_section["content"]:
            chunks.append({
                "section_name": current_section["title"],
                "content": "\n".join(current_section["content"]).strip()
            })
        
        return chunks
    
    def ingest_file(self, file_path: str) -> int:
        """Ingest a single markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"✗ Error reading {file_path}: {e}")
            return 0
        
        chunks = self.split_by_headings(content, file_path)
        
        # Filter chunks by length
        valid_chunks = [c for c in chunks if 50 <= len(c["content"]) <= 2000]
        
        chapter_title = Path(file_path).stem.replace('_', ' ').title()
        
        for i, chunk in enumerate(valid_chunks):
            chunk_data = {
                'id': self.store.generate_id(file_path, chunk['section_name'], i),
                'text': chunk['content'],
                'chapter_title': chapter_title,
                'section_name': chunk['section_name'],
                'page_url': f"/docs/{Path(file_path).stem}",
                'heading_level': 2,
                'chunk_index': i,
                'source_file': str(file_path),
                'ingested_at': datetime.now().isoformat()
            }
            
            self.store.add_chunk(chunk_data)
        
        return len(valid_chunks)
    
    def ingest_directory(self, docs_dir: str) -> Dict[str, int]:
        """Ingest all markdown files from a directory."""
        docs_path = Path(docs_dir)
        
        if not docs_path.exists():
            raise FileNotFoundError(f"Docs directory not found: {docs_dir}")
        
        markdown_files = list(docs_path.rglob("*.md"))
        
        if not markdown_files:
            print(f"⚠ No markdown files found in {docs_dir}")
            return {"files": 0, "chunks": 0}
        
        print(f"\n📚 Found {len(markdown_files)} markdown files")
        print("=" * 60)
        
        stats = {"files": 0, "chunks": 0}
        
        for file_path in markdown_files:
            chunks = self.ingest_file(str(file_path))
            stats["files"] += 1
            stats["chunks"] += chunks
            print(f"✓ {file_path.name}: {chunks} chunks")
        
        return stats
    
    def close(self):
        """Close connections."""
        self.store.close()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Simple RAG ingestor with local vector store"
    )
    parser.add_argument(
        "--docs-dir",
        type=str,
        default="docs",
        help="Directory containing markdown files"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default="vector_store.db",
        help="SQLite database path"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show collection statistics"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📖 Simple RAG Knowledge Builder")
    print("=" * 60)
    
    try:
        ingestor = SimpleIngestor(db_path=args.db_path)
        
        if args.stats:
            stats = ingestor.store.get_stats()
            print("\n📊 Collection Statistics:")
            print("-" * 40)
            for key, value in stats.items():
                print(f"  {key}: {value}")
            ingestor.close()
            return
        
        # Ingest files
        stats = ingestor.ingest_directory(args.docs_dir)
        
        # Print summary
        print("\n" + "=" * 60)
        print("✅ Ingestion Complete!")
        print(f"   Files processed: {stats['files']}")
        print(f"   Chunks created: {stats['chunks']}")
        
        # Show final stats
        final_stats = ingestor.store.get_stats()
        print(f"\n📊 Collection Info:")
        print(f"   Total vectors: {final_stats['vector_count']}")
        print(f"   Using embeddings: {final_stats['using_embeddings']}")
        print(f"   Database: {args.db_path}")
        
        print("=" * 60)
        
        ingestor.close()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
