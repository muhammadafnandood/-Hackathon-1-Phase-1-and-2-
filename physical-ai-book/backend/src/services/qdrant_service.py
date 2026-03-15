"""
Qdrant vector database service.
Handles vector storage, search, and collection management.
"""
import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    SearchParams,
    ScoredPoint,
)

from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database."""
    
    def __init__(self):
        """Initialize Qdrant client."""
        settings = get_settings()
        
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            https=True,
        )
        
        self.collection_name = settings.QDRANT_COLLECTION
        self.vector_size = settings.QDRANT_VECTOR_SIZE
        
        logger.info(f"QdrantService initialized with collection: {self.collection_name}")
    
    def create_collection(self) -> bool:
        """
        Create the textbook embeddings collection if it doesn't exist.
        
        Returns:
            True if collection created or already exists, False on error
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            
            for collection in collections.collections:
                if collection.name == self.collection_name:
                    logger.info(f"Collection {self.collection_name} already exists")
                    return True
            
            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
                hnsw_config={
                    "m": 16,
                    "ef_construct": 100,
                },
            )
            
            logger.info(f"Created collection: {self.collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            return False
    
    def upsert_points(
        self,
        points: List[PointStruct],
        wait: bool = True,
    ) -> bool:
        """
        Upsert (insert or update) points into the collection.
        
        Args:
            points: List of PointStruct objects to upsert
            wait: Wait for operation to complete
        
        Returns:
            True if successful, False on error
        """
        try:
            result = self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=wait,
            )
            
            logger.info(f"Upserted {len(points)} points")
            return result.status == "completed"
            
        except Exception as e:
            logger.error(f"Failed to upsert points: {e}")
            return False
    
    def search(
        self,
        vector: List[float],
        limit: int = 5,
        chapter_id: Optional[str] = None,
    ) -> List[ScoredPoint]:
        """
        Search for similar vectors in the collection.
        
        Args:
            vector: Query vector (embedding)
            limit: Maximum number of results to return
            chapter_id: Optional chapter ID to filter by
        
        Returns:
            List of scored points
        """
        try:
            # Build filter if chapter_id provided
            search_filter = None
            if chapter_id:
                search_filter = Filter(
                    must=[
                        FieldCondition(
                            key="chapter_id",
                            match=MatchValue(value=chapter_id),
                        )
                    ]
                )
            
            # Search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                query_filter=search_filter,
                limit=limit,
                search_params=SearchParams(
                    hnsw_ef=128,
                    exact=False,
                ),
            )
            
            logger.info(f"Search returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def delete_points(self, ids: List[str]) -> bool:
        """
        Delete points by ID.
        
        Args:
            ids: List of point IDs to delete
        
        Returns:
            True if successful, False on error
        """
        try:
            result = self.client.delete(
                collection_name=self.collection_name,
                points_selector=ids,
            )
            
            logger.info(f"Deleted {len(ids)} points")
            return result.status == "completed"
            
        except Exception as e:
            logger.error(f"Failed to delete points: {e}")
            return False


# Global service instance
_qdrant_service: Optional[QdrantService] = None


def get_qdrant_service() -> QdrantService:
    """Get or create QdrantService instance."""
    global _qdrant_service
    if _qdrant_service is None:
        _qdrant_service = QdrantService()
    return _qdrant_service
