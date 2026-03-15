"""
Embedding service for textbook content.
Handles chunking, embedding generation, and vector storage.
"""
import logging
from typing import List, Dict, Any, Optional
from qdrant_client.models import PointStruct
from src.services.llm_service import get_openai_service
from src.services.qdrant_service import get_qdrant_service
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class EmbeddingService:
    """Service for generating and storing embeddings."""
    
    def __init__(self):
        """Initialize embedding service."""
        self.openai_service = get_openai_service()
        self.qdrant_service = get_qdrant_service()
        
        # Chunking configuration
        self.chunk_size = 800  # characters
        self.chunk_overlap = 100  # characters
        
        logger.info("EmbeddingService initialized")
    
    def chunk_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks with metadata.
        
        Args:
            text: Input text to chunk
            metadata: Optional metadata to attach to each chunk
        
        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        
        # Simple character-based chunking with overlap
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                for sep in ['. ', '.\n', '!\n', '?\n']:
                    last_sep = text[start:end].rfind(sep)
                    if last_sep > 0:
                        end = start + last_sep + len(sep)
                        break
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunk_metadata = {
                    "id": f"chunk_{chunk_id}",
                    "chunk_index": chunk_id,
                    "text": chunk_text,
                    "start_char": start,
                    "end_char": end,
                    **(metadata or {}),
                }
                chunks.append(chunk_metadata)
                chunk_id += 1
            
            start = end - self.chunk_overlap
        
        logger.info(f"Created {len(chunks)} chunks from {len(text)} characters")
        return chunks
    
    def embed_and_store(
        self,
        text: str,
        metadata: Dict[str, Any],
    ) -> bool:
        """
        Embed text and store in vector database.
        
        Args:
            text: Input text to embed
            metadata: Metadata for the text (chapter_id, section, etc.)
        
        Returns:
            True if successful, False on error
        """
        try:
            # Chunk the text
            chunks = self.chunk_text(text, metadata)
            
            if not chunks:
                logger.warning("No chunks created")
                return False
            
            # Generate embeddings
            texts_to_embed = [chunk["text"] for chunk in chunks]
            embeddings = self.openai_service.generate_embeddings_batch(texts_to_embed)
            
            # Filter out failed embeddings
            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                if embedding is None:
                    logger.warning(f"Skipping chunk {i} due to embedding failure")
                    continue
                
                point = PointStruct(
                    id=i,
                    vector=embedding,
                    payload=chunk,
                )
                points.append(point)
            
            if not points:
                logger.error("No valid points to upsert")
                return False
            
            # Store in Qdrant
            success = self.qdrant_service.upsert_points(points)
            
            if success:
                logger.info(f"Stored {len(points)} embeddings")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to embed and store: {e}")
            return False
    
    def search_similar(
        self,
        query: str,
        limit: int = 5,
        chapter_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar content.
        
        Args:
            query: Search query
            limit: Maximum results to return
            chapter_id: Optional chapter to filter by
        
        Returns:
            List of results with content and metadata
        """
        # Generate query embedding
        embedding = self.openai_service.generate_embedding(query)
        
        if not embedding:
            logger.error("Failed to generate query embedding")
            return []
        
        # Search in Qdrant
        results = self.qdrant_service.search(
            vector=embedding,
            limit=limit,
            chapter_id=chapter_id,
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "content": result.payload.get("text", ""),
                "metadata": {
                    k: v for k, v in result.payload.items()
                    if k not in ["text", "id", "chunk_index", "start_char", "end_char"]
                },
                "score": result.score,
            })
        
        logger.info(f"Found {len(formatted_results)} similar results")
        return formatted_results


# Global service instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """Get or create EmbeddingService instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
