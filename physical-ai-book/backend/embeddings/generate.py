# Embeddings Generator Service
# Generates embeddings for textbook content and stores in Qdrant

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import uuid

load_dotenv()


class EmbeddingsGenerator:
    """Generate and store embeddings for textbook content."""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.qdrant = QdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = "textbook_chunks"
        self.dimension = 1536  # ada-002
        
    def init_collection(self):
        """Initialize Qdrant collection."""
        collections = self.qdrant.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.collection_name not in collection_names:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.dimension,
                    distance=Distance.COSINE
                )
            )
            print(f"✅ Created collection: {self.collection_name}")
        else:
            print(f"✅ Collection exists: {self.collection_name}")
    
    def chunk_text(self, text: str, chunk_size: int = 500) -> list:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size // 2):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def generate_embedding(self, text: str) -> list:
        """Generate embedding for text."""
        response = self.openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    
    def process_markdown_file(self, file_path: str, chapter_id: str):
        """Process a markdown file and generate embeddings."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by headings
        sections = self.split_by_headings(content)
        
        points = []
        for heading, section_content in sections.items():
            # Generate embedding for section
            embedding = self.generate_embedding(section_content)
            
            # Create point
            point_id = uuid.uuid4().int >> 64
            
            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "chapter_id": chapter_id,
                        "heading": heading,
                        "content": section_content,
                        "file_path": file_path
                    }
                )
            )
        
        # Upsert to Qdrant
        if points:
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"✅ Indexed {len(points)} chunks from {file_path}")
    
    def split_by_headings(self, content: str) -> dict:
        """Split markdown content by headings."""
        sections = {}
        current_heading = "Introduction"
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('#'):
                # Save previous section
                if current_content:
                    sections[current_heading] = '\n'.join(current_content)
                
                # Start new section
                current_heading = line.lstrip('#').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_heading] = '\n'.join(current_content)
        
        return sections
    
    def index_directory(self, docs_dir: str):
        """Index all markdown files in a directory."""
        docs_path = Path(docs_dir)
        
        for md_file in docs_path.rglob("*.md"):
            # Use file path as chapter ID
            chapter_id = str(md_file.relative_to(docs_path))
            
            print(f"Processing: {md_file}")
            self.process_markdown_file(str(md_file), chapter_id)


def main():
    """Main entry point."""
    generator = EmbeddingsGenerator()
    generator.init_collection()
    
    # Index docs directory
    docs_dir = os.getenv("DOCS_DIR", "../../../docs")
    generator.index_directory(docs_dir)
    
    print("\n✅ Embedding generation complete!")


if __name__ == "__main__":
    main()
