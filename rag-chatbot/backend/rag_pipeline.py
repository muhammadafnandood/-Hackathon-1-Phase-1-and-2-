"""
RAG Pipeline for Textbook Chatbot

Orchestrates the retrieval-augmented generation process:
1. Embed user query
2. Retrieve relevant chunks from Qdrant
3. Construct prompt with context
4. Generate answer using OpenAI GPT
5. Return answer with sources

Optionally personalizes responses based on user's technical background.
"""

import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from openai import OpenAI, RateLimitError
import dotenv

from vector_store import QdrantSearchClient, get_qdrant_client
from personalizer import UserProfile, ExperienceLevel, ContentPersonalizer

dotenv.load_dotenv()


@dataclass
class ChatResponse:
    """Structured response from the RAG pipeline."""
    answer: str
    sources: List[Dict[str, str]]
    confidence: float
    query: str
    model_used: str
    chunks_retrieved: int
    user_profile: Optional[Dict[str, str]] = None
    personalization_applied: bool = False


@dataclass
class StreamChunk:
    """A chunk of streamed response."""
    content: str
    is_final: bool
    sources: Optional[List[Dict[str, str]]] = None
    confidence: Optional[float] = None


class RAGPipeline:
    """Main RAG pipeline for textbook Q&A."""

    def __init__(
        self,
        collection_name: str = "textbook_knowledge",
        model: str = "gpt-3.5-turbo",
        top_k: int = 5,
        score_threshold: float = 0.5,
        user_profile: Optional[UserProfile] = None,
    ):
        """
        Initialize the RAG pipeline.
        
        Args:
            collection_name: Qdrant collection name
            model: OpenAI model to use for generation
            top_k: Number of chunks to retrieve
            score_threshold: Minimum similarity score for retrieval
            user_profile: Optional user profile for personalization
        """
        self.collection_name = collection_name
        self.model = model
        self.top_k = top_k
        self.score_threshold = score_threshold
        self.user_profile = user_profile
        self.personalizer = ContentPersonalizer(user_profile) if user_profile else None
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.openai_client = OpenAI(api_key=api_key)
        
        # Initialize Qdrant client
        self.qdrant_client = get_qdrant_client(collection_name)
        
        # System prompt for the assistant
        self.system_prompt = """You are a helpful textbook assistant for a course on Physical AI and Humanoid Robotics. 
Your role is to answer student questions based on the textbook content provided in the context.

GUIDELINES:
1. Answer based ONLY on the provided context. If the answer isn't in the context, say "I don't have information about that in the textbook."
2. Be concise but thorough. Aim for 2-4 paragraphs.
3. Use clear, beginner-friendly language.
4. Include relevant technical details when appropriate.
5. If the context mentions code examples, describe them but don't reproduce full code unless specifically asked.
6. Cite the chapter/section when referencing specific information.
7. If multiple sections are relevant, mention that in your answer.

Remember: You are helping students learn. Be encouraging and educational in your tone."""
        
        # Personalization prompt additions based on user level
        self._update_system_prompt_for_level()
    
    def _update_system_prompt_for_level(self):
        """Add personalization instructions based on user profile."""
        if not self.user_profile:
            return
        
        level = self.user_profile.get_overall_level()
        
        if level == ExperienceLevel.BEGINNER:
            self.system_prompt += """

PERSONALIZATION (Beginner):
- Use simple language and explain technical terms
- Include analogies to everyday concepts
- Break complex ideas into smaller steps
- Provide encouraging explanations"""
        
        elif level == ExperienceLevel.INTERMEDIATE:
            self.system_prompt += """

PERSONALIZATION (Intermediate):
- Assume basic technical knowledge
- Explain domain-specific concepts
- Include best practices and patterns
- Connect to related concepts they may know"""
        
        else:  # Advanced
            self.system_prompt += """

PERSONALIZATION (Advanced):
- Use precise technical language
- Discuss trade-offs and implementation details
- Reference advanced concepts and research
- Focus on practical application insights"""

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for the user query."""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=query
            )
            return response.data[0].embedding
        except Exception as e:
            raise RuntimeError(f"Failed to generate embedding: {e}")

    def retrieve_context(
        self,
        query_vector: List[float],
        use_mmr: bool = True,
    ) -> Tuple[List[Dict[str, Any]], str]:
        """
        Retrieve relevant chunks from Qdrant.
        
        Args:
            query_vector: The embedded query vector
            use_mmr: Whether to use Maximal Marginal Relevance
        
        Returns:
            Tuple of (retrieved chunks, formatted context string)
        """
        # Search with MMR for diversity
        if use_mmr:
            results = self.qdrant_client.search_with_mmr(
                query_vector=query_vector,
                top_k=self.top_k,
                mmr_lambda=0.7,  # Favor relevance but add diversity
                score_threshold=self.score_threshold,
            )
        else:
            results = self.qdrant_client.search(
                query_vector=query_vector,
                top_k=self.top_k,
                score_threshold=self.score_threshold,
            )
        
        if not results:
            return [], ""
        
        # Format context
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Source {i}: {result['chapter_title']} - {result['section_name']}]\n"
                f"{result['text']}\n"
            )
        
        context = "\n---\n".join(context_parts)
        
        return results, context

    def construct_prompt(self, query: str, context: str) -> str:
        """Construct the final prompt for GPT."""
        if not context:
            return f"""{self.system_prompt}

Note: No relevant textbook content was found for this query. Please inform the user that you don't have information about this topic in the textbook.

Question: {query}"""

        return f"""{self.system_prompt}

CONTEXT FROM TEXTBOOK:
{context}

QUESTION: {query}

ANSWER:"""

    def generate_answer(
        self,
        prompt: str,
        max_tokens: int = 600,
        temperature: float = 0.3,
    ) -> str:
        """Generate answer using OpenAI GPT."""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except RateLimitError:
            # Retry with exponential backoff
            import time
            for attempt in range(3):
                time.sleep(2 ** attempt)
                try:
                    response = self.openai_client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=max_tokens,
                        temperature=temperature,
                    )
                    return response.choices[0].message.content
                except RateLimitError:
                    if attempt == 2:
                        raise
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to generate answer: {e}")

    def calculate_confidence(self, retrieval_results: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score based on retrieval quality.
        
        Args:
            retrieval_results: List of retrieved chunks with scores
        
        Returns:
            Confidence score between 0 and 1
        """
        if not retrieval_results:
            return 0.0
        
        # Average score of top 3 results (or fewer if less available)
        top_scores = [r["score"] for r in retrieval_results[:3]]
        avg_score = sum(top_scores) / len(top_scores)
        
        # Normalize to 0-1 range (scores are typically 0.5-1.0)
        normalized_confidence = min(1.0, (avg_score - 0.5) * 2)
        
        return round(normalized_confidence, 2)

    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        use_mmr: bool = True,
        user_profile: Optional[UserProfile] = None,
    ) -> ChatResponse:
        """
        Process a user question through the full RAG pipeline.
        
        Args:
            question: The user's question
            top_k: Override default number of chunks to retrieve
            use_mmr: Whether to use MMR for retrieval
            user_profile: Optional profile to override instance profile
        
        Returns:
            ChatResponse with answer, sources, and metadata
        """
        # Use provided profile or instance profile
        effective_profile = user_profile if user_profile else self.user_profile
        
        # Use provided top_k or default
        effective_top_k = top_k if top_k else self.top_k
        
        # Step 1: Embed the query
        query_vector = self.embed_query(question)
        
        # Step 2: Retrieve relevant context
        retrieval_results, context = self.retrieve_context(
            query_vector=query_vector,
            use_mmr=use_mmr,
        )
        
        # Step 3: Construct prompt
        prompt = self.construct_prompt(question, context)
        
        # Step 4: Generate answer
        answer = self.generate_answer(prompt)
        
        # Step 5: Extract sources
        sources = [
            {
                "chapter": r["chapter_title"],
                "section": r["section_name"],
                "url": r["page_url"],
                "score": r["score"],
            }
            for r in retrieval_results
        ]
        
        # Calculate confidence
        confidence = self.calculate_confidence(retrieval_results)
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            query=question,
            model_used=self.model,
            chunks_retrieved=len(retrieval_results),
            user_profile=effective_profile.to_dict() if effective_profile else None,
            personalization_applied=effective_profile is not None,
        )

    def query_stream(
        self,
        question: str,
        top_k: Optional[int] = None,
    ):
        """
        Stream the RAG response for better UX.
        
        Yields:
            StreamChunk objects with incremental content
        """
        effective_top_k = top_k if top_k else self.top_k
        
        # First, retrieve context (non-streaming)
        query_vector = self.embed_query(question)
        retrieval_results, context = self.retrieve_context(query_vector)
        
        # Extract sources early
        sources = [
            {
                "chapter": r["chapter_title"],
                "section": r["section_name"],
                "url": r["page_url"],
            }
            for r in retrieval_results
        ]
        
        # Construct prompt
        prompt = self.construct_prompt(question, context)
        
        # Stream the GPT response
        try:
            stream = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.3,
                stream=True,
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield StreamChunk(content=content, is_final=False)
            
            # Final chunk with sources
            confidence = self.calculate_confidence(retrieval_results)
            yield StreamChunk(
                content="",
                is_final=True,
                sources=sources,
                confidence=confidence,
            )
            
        except Exception as e:
            yield StreamChunk(
                content=f"Error: {str(e)}",
                is_final=True,
                sources=[],
                confidence=0.0,
            )

    def health_check(self) -> Dict[str, Any]:
        """Check health of all pipeline components."""
        qdrant_stats = self.qdrant_client.get_collection_stats()
        
        return {
            "status": "healthy" if qdrant_stats.get("connected") else "unhealthy",
            "qdrant": qdrant_stats,
            "openai": "connected" if self.openai_client else "disconnected",
            "model": self.model,
            "collection": self.collection_name,
        }


# Convenience function for simple usage
def ask_question(
    question: str,
    collection_name: str = "textbook_knowledge",
    top_k: int = 5,
) -> ChatResponse:
    """
    Ask a question and get an answer.
    
    Simple convenience function for quick usage.
    
    Args:
        question: The user's question
        collection_name: Qdrant collection name
        top_k: Number of chunks to retrieve
    
    Returns:
        ChatResponse with answer and sources
    """
    pipeline = RAGPipeline(collection_name=collection_name, top_k=top_k)
    return pipeline.query(question)
