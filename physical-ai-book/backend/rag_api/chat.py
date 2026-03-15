"""
Chat service for RAG-based conversations
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from database import DatabaseSession
from embeddings import EmbeddingService


class ChatService:
    """RAG chat service."""
    
    def __init__(
        self,
        db: DatabaseSession,
        qdrant: QdrantClient,
        embedding_service: EmbeddingService,
        openai_api_key: str
    ):
        self.db = db
        self.qdrant = qdrant
        self.embedding_service = embedding_service
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.collection_name = "textbook_chunks"
        
        # Initialize Qdrant collection
        self._init_collection()
    
    def _init_collection(self):
        """Initialize Qdrant collection if not exists."""
        collections = self.qdrant.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.collection_name not in collection_names:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_service.dimension,
                    distance=Distance.COSINE
                )
            )
    
    async def chat(
        self,
        message: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        Process a chat message with RAG.
        
        Args:
            message: User's message
            session_id: Chat session ID
            user_id: User ID for personalization
            top_k: Number of chunks to retrieve
            
        Returns:
            Chat response with answer and sources
        """
        # Step 1: Generate query embedding
        query_embedding = self.embedding_service.embed_query(message)
        
        # Step 2: Search Qdrant for relevant chunks
        search_results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        
        # Step 3: Format retrieved chunks as context
        context_chunks = []
        sources = []
        
        for result in search_results:
            chunk_data = result.payload
            context_chunks.append(chunk_data.get("content", ""))
            sources.append({
                "chapter_id": chunk_data.get("chapter_id"),
                "heading": chunk_data.get("heading"),
                "score": result.score,
                "content": chunk_data.get("content", "")[:200] + "..."
            })
        
        context = "\n\n".join(context_chunks)
        
        # Step 4: Get user profile for personalization
        user_context = ""
        if user_id:
            profile = await self.get_user_profile(user_id)
            if profile:
                user_context = f"""
User's experience level:
- Programming: {profile.get('programming_experience', 'beginner')}
- AI/ML: {profile.get('ai_experience', 'beginner')}
- Robotics: {profile.get('robotics_experience', 'beginner')}

"""
        
        # Step 5: Generate response with LLM
        system_prompt = f"""You are an AI teaching assistant for the Physical AI & Humanoid Robotics textbook.

{user_context}
Use the following textbook content to answer the user's question. Be clear, educational, and reference the sources.

If the user is a beginner, use simpler language and more examples.
If the user is advanced, you can use more technical terminology.

Always cite which chapter or section your information comes from.

Textbook Content:
{context}
"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        
        # Step 6: Create or use session
        if not session_id:
            session_result = await self.create_session(user_id)
            session_id = session_result["session_id"]
        
        # Step 7: Save messages to database
        await self._save_message(session_id, "user", message)
        await self._save_message(session_id, "assistant", answer, {
            "sources": sources,
            "model": "gpt-4"
        })
        
        return {
            "response": answer,
            "sources": sources,
            "session_id": session_id,
            "model": "gpt-4"
        }
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
        chapter_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search textbook content using vector similarity.
        
        Args:
            query: Search query
            top_k: Number of results
            chapter_id: Optional chapter filter
            
        Returns:
            List of relevant chunks with scores
        """
        query_embedding = self.embedding_service.embed_query(query)
        
        # Build filter if chapter_id provided
        search_filter = None
        if chapter_id:
            from qdrant_client.models import FieldCondition, MatchValue
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="chapter_id",
                        match=MatchValue(value=chapter_id)
                    )
                ]
            )
        
        results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            query_filter=search_filter
        )
        
        return [
            {
                "chapter_id": r.payload.get("chapter_id"),
                "heading": r.payload.get("heading"),
                "content": r.payload.get("content"),
                "score": r.score
            }
            for r in results
        ]
    
    async def add_chunk(
        self,
        chapter_id: str,
        content: str,
        heading: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a text chunk for vector search.
        
        Args:
            chapter_id: Chapter ID
            content: Text content
            heading: Optional section heading
            
        Returns:
            Result with chunk ID
        """
        # Generate embedding
        embedding = self.embedding_service.embed_text(content)
        
        # Create metadata
        metadata = {
            "chapter_id": chapter_id,
            "content": content,
            "heading": heading or "",
            "created_at": datetime.now().isoformat()
        }
        
        # Insert into Qdrant
        from qdrant_client.models import PointStruct
        import uuid
        
        point_id = uuid.uuid4().int >> 64  # Generate UUID compatible with Qdrant
        
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=metadata
                )
            ]
        )
        
        # Also save to PostgreSQL
        self.db.execute(
            """
            INSERT INTO chunks (chapter_id, content, heading, metadata)
            VALUES (%s, %s, %s, %s)
            """,
            (chapter_id, content, heading, json.dumps(metadata))
        )
        
        return {
            "status": "success",
            "chapter_id": chapter_id,
            "heading": heading
        }
    
    async def create_session(self, user_id: Optional[str] = None) -> Dict[str, str]:
        """Create a new chat session."""
        import uuid
        session_id = str(uuid.uuid4())
        
        self.db.execute(
            """
            INSERT INTO chat_sessions (id, user_id, session_name)
            VALUES (%s, %s, %s)
            """,
            (session_id, user_id, f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        )
        
        return {"session_id": session_id}
    
    async def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get chat session message history."""
        messages = self.db.execute(
            """
            SELECT role, content, metadata, created_at
            FROM chat_messages
            WHERE session_id = %s
            ORDER BY created_at ASC
            """,
            (session_id,)
        )
        
        return [
            {
                "role": m["role"],
                "content": m["content"],
                "metadata": m["metadata"],
                "timestamp": m["created_at"]
            }
            for m in messages
        ] if messages else []
    
    async def _save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ):
        """Save a chat message to database."""
        self.db.execute(
            """
            INSERT INTO chat_messages (session_id, role, content, metadata)
            VALUES (%s, %s, %s, %s)
            """,
            (session_id, role, content, json.dumps(metadata or {}))
        )
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile for personalization."""
        profile = self.db.execute_one(
            """
            SELECT * FROM user_profiles
            WHERE user_id = %s
            """,
            (user_id,)
        )
        return dict(profile) if profile else None
    
    async def update_user_profile(
        self,
        user_id: str,
        profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update user profile."""
        # Check if profile exists
        existing = self.db.execute_one(
            "SELECT id FROM user_profiles WHERE user_id = %s",
            (user_id,)
        )
        
        if existing:
            # Update
            self.db.execute(
                """
                UPDATE user_profiles
                SET programming_experience = %s,
                    ai_experience = %s,
                    robotics_experience = %s,
                    hardware_availability = %s,
                    gpu_capability = %s,
                    preferred_language = %s
                WHERE user_id = %s
                """,
                (
                    profile.get("programming_experience"),
                    profile.get("ai_experience"),
                    profile.get("robotics_experience"),
                    profile.get("hardware_availability"),
                    profile.get("gpu_capability"),
                    profile.get("preferred_language"),
                    user_id
                )
            )
        else:
            # Insert
            self.db.execute(
                """
                INSERT INTO user_profiles (user_id, programming_experience, ai_experience, 
                    robotics_experience, hardware_availability, gpu_capability, preferred_language)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    profile.get("programming_experience", "beginner"),
                    profile.get("ai_experience", "beginner"),
                    profile.get("robotics_experience", "beginner"),
                    profile.get("hardware_availability", "none"),
                    profile.get("gpu_capability", "integrated"),
                    profile.get("preferred_language", "en")
                )
            )
        
        return await self.get_user_profile(user_id)
    
    async def get_user_progress(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's learning progress."""
        progress = self.db.execute(
            """
            SELECT c.title, c.slug, up.status, up.progress_percent, 
                   up.time_spent_seconds, up.completed_at
            FROM user_progress up
            JOIN chapters c ON up.chapter_id = c.id
            WHERE up.user_id = %s
            ORDER BY up.created_at DESC
            """,
            (user_id,)
        )
        
        return [dict(p) for p in progress] if progress else []
    
    async def track_event(
        self,
        event_type: str,
        event_data: Dict[str, Any],
        user_id: Optional[str] = None
    ):
        """Track an analytics event."""
        self.db.execute(
            """
            INSERT INTO analytics_events (user_id, event_type, event_data)
            VALUES (%s, %s, %s)
            """,
            (user_id, event_type, json.dumps(event_data))
        )
