"""
OpenAI LLM service for text generation and embeddings.
Handles all interactions with OpenAI API.
"""
import logging
from typing import List, Optional, Dict, Any
from openai import OpenAI
from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        settings = get_settings()
        
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL
        self.llm_model = settings.OPENAI_LLM_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        
        logger.info(f"OpenAIService initialized with model: {self.llm_model}")
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding vector for text.
        
        Args:
            text: Input text to embed
        
        Returns:
            Embedding vector as list of floats, or None on error
        """
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text,
            )
            
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding with {len(embedding)} dimensions")
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return None
    
    def generate_embeddings_batch(
        self,
        texts: List[str],
        batch_size: int = 100,
    ) -> List[Optional[List[float]]]:
        """
        Generate embeddings for multiple texts in batches.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts per batch
        
        Returns:
            List of embedding vectors
        """
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            try:
                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=batch,
                )
                
                # Sort by index to maintain order
                sorted_data = sorted(response.data, key=lambda x: x.index)
                batch_embeddings = [item.embedding for item in sorted_data]
                all_embeddings.extend(batch_embeddings)
                
                logger.debug(f"Processed batch {i // batch_size + 1}")
                
            except Exception as e:
                logger.error(f"Failed to generate batch embeddings: {e}")
                # Add None for failed batch
                all_embeddings.extend([None] * len(batch))
        
        return all_embeddings
    
    def generate_completion(
        self,
        prompt: str,
        system_message: str = "You are a helpful assistant.",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> Optional[str]:
        """
        Generate text completion using LLM.
        
        Args:
            prompt: User prompt
            system_message: System instruction
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        
        Returns:
            Generated text, or None on error
        """
        try:
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens or self.max_tokens,
            )
            
            content = response.choices[0].message.content
            usage = response.usage
            
            logger.info(
                f"Generated completion: {usage.prompt_tokens} prompt + "
                f"{usage.completion_tokens} completion = {usage.total_tokens} total"
            )
            
            return content
            
        except Exception as e:
            logger.error(f"Failed to generate completion: {e}")
            return None
    
    def generate_with_context(
        self,
        query: str,
        context: List[Dict[str, Any]],
        system_message: str = "You are a helpful AI teaching assistant.",
        temperature: float = 0.7,
    ) -> Optional[str]:
        """
        Generate response with retrieved context (RAG).
        
        Args:
            query: User query
            context: List of context dictionaries with 'content' and 'source'
            system_message: System instruction
            temperature: Sampling temperature
        
        Returns:
            Generated response, or None on error
        """
        # Format context
        context_text = "\n\n".join([
            f"[Source: {c.get('source', 'Unknown')}]\n{c['content']}"
            for c in context
        ])
        
        prompt = f"""Context information:
{context_text}

User question: {query}

Please answer based on the context above. If the context doesn't contain the answer, use your knowledge but mention it."""
        
        return self.generate_completion(
            prompt=prompt,
            system_message=system_message,
            temperature=temperature,
        )


# Global service instance
_openai_service: Optional[OpenAIService] = None


def get_openai_service() -> OpenAIService:
    """Get or create OpenAIService instance."""
    global _openai_service
    if _openai_service is None:
        _openai_service = OpenAIService()
    return _openai_service
