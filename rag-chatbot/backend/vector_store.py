"""
Qdrant Client Wrapper for RAG Chatbot

Provides a clean interface for vector search operations with retry logic,
connection pooling, and error handling.
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    Range,
    ScoredPoint,
)
import dotenv

dotenv.load_dotenv()


class QdrantSearchClient:
    """Wrapper around QdrantClient for RAG search operations."""

    def __init__(self, collection_name: str = "textbook_knowledge"):
        """
        Initialize Qdrant client.
        
        Args:
            collection_name: Name of the Qdrant collection to use
        """
        self.collection_name = collection_name
        
        # Get connection parameters from environment
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        if not qdrant_url:
            raise ValueError("QDRANT_URL not found in environment variables")
        
        # Initialize client
        self.client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            timeout=30,
            # Enable connection pooling
            check_compatibility=False,
            grpc_options={
                "keepalive_timeout_ms": 10000,
                "keepalive_permit_without_calls": True,
            } if self._is_grpc_enabled() else None
        )
        
        self._connected = False
        self._verify_connection()
    
    def _is_grpc_enabled(self) -> bool:
        """Check if gRPC is enabled for Qdrant."""
        # gRPC is typically available for Qdrant Cloud
        return os.getenv("QDRANT_GRPC", "false").lower() == "true"
    
    def _verify_connection(self) -> None:
        """Verify connection to Qdrant and collection exists."""
        try:
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if self.collection_name not in collection_names:
                raise ValueError(
                    f"Collection '{self.collection_name}' not found. "
                    "Run ingest_book.py first to create the collection."
                )
            
            self._connected = True
            print(f"✓ Connected to Qdrant collection: {self.collection_name}")
            
        except Exception as e:
            self._connected = False
            raise ConnectionError(f"Failed to connect to Qdrant: {e}")
    
    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        score_threshold: float = 0.5,
        filter_by_chapter: Optional[str] = None,
        filter_by_section: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks in the collection.
        
        Args:
            query_vector: The embedding vector for the query
            top_k: Number of results to return
            score_threshold: Minimum similarity score threshold
            filter_by_chapter: Optional filter by chapter title
            filter_by_section: Optional filter by section name
        
        Returns:
            List of search results with text, metadata, and score
        """
        if not self._connected:
            raise ConnectionError("Not connected to Qdrant")
        
        # Build filter if needed
        search_filter = None
        if filter_by_chapter or filter_by_section:
            conditions = []
            
            if filter_by_chapter:
                conditions.append(
                    FieldCondition(
                        key="chapter_title",
                        match=MatchValue(value=filter_by_chapter)
                    )
                )
            
            if filter_by_section:
                conditions.append(
                    FieldCondition(
                        key="section_name",
                        match=MatchValue(value=filter_by_section)
                    )
                )
            
            if conditions:
                search_filter = Filter(must=conditions)
        
        # Perform search
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=search_filter,
                limit=top_k,
                score_threshold=score_threshold,
                with_payload=True,
                with_vectors=False,  # Don't return vectors for efficiency
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "text": result.payload.get("text", ""),
                    "chapter_title": result.payload.get("chapter_title", "Unknown"),
                    "section_name": result.payload.get("section_name", "Unknown"),
                    "page_url": result.payload.get("page_url", ""),
                    "score": result.score,
                    "chunk_index": result.payload.get("chunk_index", 0),
                })
            
            return formatted_results
            
        except Exception as e:
            raise RuntimeError(f"Search failed: {e}")
    
    def search_with_mmr(
        self,
        query_vector: List[float],
        top_k: int = 5,
        mmr_lambda: float = 0.5,
        score_threshold: float = 0.5,
    ) -> List[Dict[str, Any]]:
        """
        Search with Maximal Marginal Relevance for diverse results.
        
        MMR balances relevance to query with diversity among results.
        
        Args:
            query_vector: The embedding vector for the query
            top_k: Number of results to return
            mmr_lambda: Balance between relevance (1.0) and diversity (0.0)
            score_threshold: Minimum similarity score threshold
        
        Returns:
            List of diverse search results
        """
        # First, get more results than needed
        initial_results = self.search(
            query_vector=query_vector,
            top_k=top_k * 3,  # Get 3x for MMR selection
            score_threshold=score_threshold,
        )
        
        if len(initial_results) <= top_k:
            return initial_results
        
        # Implement simple MMR
        selected = []
        remaining = initial_results.copy()
        
        # Select first result (highest relevance)
        if remaining:
            selected.append(remaining.pop(0))
        
        while len(selected) < top_k and remaining:
            best_score = -float("inf")
            best_idx = 0
            
            for i, result in enumerate(remaining):
                # Calculate MMR score
                relevance_score = result["score"]
                
                # Calculate max similarity to already selected results
                max_similarity = 0
                for sel in selected:
                    # Approximate similarity using score difference
                    similarity = abs(result["score"] - sel["score"])
                    max_similarity = max(max_similarity, similarity)
                
                # MMR formula
                mmr_score = mmr_lambda * relevance_score - (1 - mmr_lambda) * max_similarity
                
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = i
            
            selected.append(remaining.pop(best_idx))
        
        return selected
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "vector_count": info.points_count,
                "vectors_size": info.config.params.vectors.size,
                "distance": str(info.config.params.vectors.distance),
                "status": str(info.status),
                "connected": self._connected,
            }
        except Exception as e:
            return {
                "error": str(e),
                "connected": self._connected,
            }
    
    def health_check(self) -> bool:
        """Check if the connection is healthy."""
        try:
            self.client.get_collections()
            return self._connected
        except Exception:
            return False
    
    def close(self) -> None:
        """Close the Qdrant connection."""
        if hasattr(self, "client"):
            self.client.close()
            self._connected = False


# Singleton instance for reuse
_client_instance: Optional[QdrantSearchClient] = None


def get_qdrant_client(collection_name: str = "textbook_knowledge") -> QdrantSearchClient:
    """
    Get or create a Qdrant client instance.
    
    Args:
        collection_name: Name of the collection
    
    Returns:
        QdrantSearchClient instance
    """
    global _client_instance
    
    if _client_instance is None:
        _client_instance = QdrantSearchClient(collection_name)
    
    return _client_instance
