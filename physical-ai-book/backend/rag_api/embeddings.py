"""
Embedding service for generating vector embeddings
"""

import os
from typing import List, Union
from openai import OpenAI
import numpy as np


class EmbeddingService:
    """Service for generating text embeddings."""
    
    def __init__(self, model_name: str = "text-embedding-ada-002"):
        self.model_name = model_name
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.dimension = 1536  # ada-002 dimension
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding
        """
        response = self.client.embeddings.create(
            model=self.model_name,
            input=text
        )
        return response.data[0].embedding
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
        """
        response = self.client.embeddings.create(
            model=self.model_name,
            input=texts
        )
        # Sort by index to maintain order
        sorted_embeddings = sorted(response.data, key=lambda x: x.index)
        return [embedding.embedding for embedding in sorted_embeddings]
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        
        For some models, queries might need different processing.
        """
        return self.embed_text(query)
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score (0 to 1)
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
