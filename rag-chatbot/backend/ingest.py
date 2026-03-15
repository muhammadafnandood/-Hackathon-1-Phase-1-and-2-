import os
import hashlib
from pathlib import Path
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

class DocumentIngestor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = "book_chunks"
        self.vector_size = 1536
        
    def create_collection(self):
        collections = self.qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.collection_name not in collection_names:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
            print(f"Created collection: {self.collection_name}")
        else:
            print(f"Collection {self.collection_name} already exists")
    
    def embed_text(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    
    def chunk_document(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split document into overlapping chunks at paragraph boundaries when possible."""
        chunks = []
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > chunk_size:
                sub_chunks = self._split_large_chunk(chunk, chunk_size, overlap)
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)
        
        return final_chunks
    
    def _split_large_chunk(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split large chunks with overlap."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks
    
    def ingest_file(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chunks = self.chunk_document(content)
        points = []
        
        for i, chunk in enumerate(chunks):
            vector = self.embed_text(chunk)
            point_id = hashlib.md5(f"{file_path}_{i}".encode()).hexdigest()
            
            point = PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "text": chunk,
                    "source": file_path,
                    "chunk_index": i
                }
            )
            points.append(point)
        
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"Ingested {len(chunks)} chunks from {file_path}")
    
    def ingest_directory(self, dir_path: str, pattern: str = "*.md"):
        book_dir = Path(dir_path)
        files = list(book_dir.glob(pattern))
        
        for file_path in files:
            self.ingest_file(str(file_path))

if __name__ == "__main__":
    print("=" * 50)
    print("RAG Ingestion Pipeline")
    print("=" * 50)
    
    ingestor = DocumentIngestor()
    
    print("\n[1/4] Reading markdown files...")
    ingestor.create_collection()
    
    print("\n[2/4] Splitting into chunks...")
    print("[3/4] Creating embeddings...")
    print("[4/4] Storing in Qdrant...")
    ingestor.ingest_directory("../book/docs", "*.md")
    
    print("\n" + "=" * 50)
    print("✓ Ingestion complete!")
    print("=" * 50)
