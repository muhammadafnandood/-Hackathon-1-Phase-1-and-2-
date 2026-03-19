"""
Intelligent Chatbot Endpoint with RAG (Retrieval-Augmented Generation)
Provides comprehensive answers with textbook content, extended knowledge,
architecture diagrams, and relevant images.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
import os
import json

router = APIRouter(prefix="/api", tags=["chat"])

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", os.getenv("QWEN_API_KEY", ""))
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_EMBEDDING_URL = os.getenv("OPENAI_EMBEDDING_URL", "https://api.openai.com/v1/embeddings")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Qdrant Configuration (for RAG)
QDRANT_URL = os.getenv("QDRANT_URL", "")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "textbook_content")


class ConversationMessage(BaseModel):
    """Previous conversation message for context."""
    role: str  # 'user' or 'bot'
    content: str


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    question: str
    chapter_id: str
    user_level: Optional[str] = "Beginner"  # User's expertise level
    conversation_history: Optional[List[ConversationMessage]] = []


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""
    book_answer: Optional[str]
    extended_knowledge: str
    mermaid_diagram: str  # Mermaid code or "NO_DIAGRAM"
    image_keywords: List[str]
    is_selection_query: bool = False  # Track if this came from text selection
    selected_text: Optional[str] = None  # The original selected text


def get_system_prompt() -> str:
    """Get the base system prompt for the AI assistant."""
    return """You are an expert AI assistant for a Physical AI and Humanoid Robotics textbook.
Your expertise includes:
- ROS 2 (Robot Operating System)
- Humanoid robot design and control
- NVIDIA Isaac Sim and Isaac Lab
- VLA (Vision-Language-Action) models
- SLAM (Simultaneous Localization and Mapping)
- Motion planning and control
- Sensor integration (LiDAR, cameras, IMU)
- Bipedal locomotion
- Machine learning for robotics

You provide clear, educational responses that help students understand complex concepts.
Use simple English and explain technical terms when first introduced.
Use bullet points and structured formatting when helpful."""


async def embed_question(question: str) -> Optional[List[float]]:
    """
    Generate embedding for the question using OpenAI.
    
    Args:
        question: The question text to embed
        
    Returns:
        List of embedding vectors or None if failed
    """
    if not OPENAI_API_KEY:
        return None
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENAI_EMBEDDING_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": EMBEDDING_MODEL,
                    "input": question,
                },
            )
            
            if response.status_code != 200:
                print(f"Embedding API error: {response.status_code}")
                return None
            
            data = response.json()
            return data["data"][0]["embedding"]
            
    except Exception as e:
        print(f"Embedding error: {e}")
        return None


async def search_qdrant(query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Search Qdrant vector database for similar content.
    
    Args:
        query_embedding: The query embedding vector
        top_k: Number of results to return
        
    Returns:
        List of matching documents with scores
    """
    if not QDRANT_URL or not query_embedding:
        return []
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{QDRANT_URL}/collections/{QDRANT_COLLECTION}/points/search",
                headers={
                    "Content-Type": "application/json",
                    **(
                        {"api-key": QDRANT_API_KEY}
                        if QDRANT_API_KEY
                        else {}
                    ),
                },
                json={
                    "vector": query_embedding,
                    "limit": top_k,
                    "with_payload": True,
                },
            )
            
            if response.status_code != 200:
                print(f"Qdrant search error: {response.status_code}")
                return []
            
            data = response.json()
            results = []
            
            for result in data.get("result", []):
                if result.get("score", 0) > 0.5:  # Only include relevant matches
                    results.append({
                        "content": result.get("payload", {}).get("content", ""),
                        "chapter": result.get("payload", {}).get("chapter", ""),
                        "score": result.get("score", 0),
                    })
            
            return results
            
    except Exception as e:
        print(f"Qdrant error: {e}")
        return []


async def call_llm(messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
    """
    Call LLM (OpenAI/Qwen) for text generation.
    
    Args:
        messages: List of message dictionaries
        temperature: Sampling temperature
        
    Returns:
        Generated text response
    """
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API key not configured. Set OPENAI_API_KEY or QWEN_API_KEY."
        )
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                OPENAI_API_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": OPENAI_MODEL,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": 2000,
                },
            )
            
            if response.status_code != 200:
                error_msg = f"LLM API error: {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('error', {})}"
                except:
                    pass
                raise HTTPException(status_code=500, detail=error_msg)
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LLM service timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"LLM service unavailable: {e}")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Intelligent chat endpoint with RAG.
    
    This endpoint:
    1. Searches textbook content using vector similarity (RAG)
    2. Generates extended knowledge using LLM
    3. Creates architecture diagrams with Mermaid.js
    4. Extracts image keywords for visual guide
    5. Adapts response to user's expertise level
    
    Args:
        request: ChatRequest with question, chapter_id, user_level, and conversation history
        
    Returns:
        ChatResponse with book_answer, extended_knowledge, mermaid_diagram, and image_keywords
    """
    question = request.question
    chapter_id = request.chapter_id
    user_level = request.user_level or "Beginner"  # Get user's expertise level

    # STEP 3: Check if this is a text selection query
    is_selection_query = False
    selected_text = None
    
    if question.startswith("Explain this from the book: "):
        is_selection_query = True
        selected_text = question.replace("Explain this from the book: ", "")
    elif question.startswith("Explain this code from the book: "):
        is_selection_query = True
        selected_text = question.replace("Explain this code from the book: ", "")
    
    # STEP A: RAG Search - Find relevant book content
    book_answer = None
    query_embedding = await embed_question(question)
    
    if query_embedding:
        rag_results = await search_qdrant(query_embedding, top_k=3)
        
        if rag_results:
            # Combine top matches into book answer
            book_answer = "\n\n".join([
                f"**From {result['chapter']}:**\n{result['content']}"
                for result in rag_results
            ])
    
    # STEP B: Generate Extended Knowledge
    # Adapt tone and depth to user's expertise level
    
    # STEP 3: Special prompt for text selection queries
    if is_selection_query and selected_text:
        extended_knowledge_prompt = f"""{get_system_prompt()}

You are an expert tutor for a Physical AI and Humanoid Robotics textbook.
The student has highlighted this exact text from the book:

SELECTED TEXT: {selected_text}

Your job is to explain this selected text thoroughly.
Structure your answer in this exact order:

1. SIMPLE EXPLANATION
   Explain what this text means in simple words.
   Assume the student is confused about it.

2. DEEPER CONTEXT  
   Why is this concept important in robotics/AI?
   Where does it fit in the bigger picture?

3. REAL WORLD EXAMPLE
   Give one concrete real-world example of this concept in action.
   Example: how a real robot uses this.

4. COMMON MISTAKES
   What do students usually misunderstand about this?
   Clarify those misconceptions.

5. RELATED CONCEPTS
   List 3 related topics the student should learn next.

Keep each section concise. Use simple English.
If the selected text contains code, explain every line separately.

{"This is CODE from the book - explain each line:" if "code from the book" in question.lower() else ""}

### 🤖 Robot Image (MANDATORY - MUST INCLUDE AT END)
**THIS IS MANDATORY - YOU MUST INCLUDE THIS SECTION**

At the very end of your response, after ALL other sections, you MUST add a robot image like this:

### 🤖 Robot Reference

**Visual Reference:**
![Relevant Robot](IMAGE_URL_HERE)
*Figure: Description of the robot*

**CHOOSE THE RIGHT ROBOT IMAGE:**
- General/beginner questions: https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/LEGO_MINDSTORMS_EV3.jpg/640px-LEGO_MINDSTORMS_EV3.jpg
- ROS 2/navigation: https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/TurtleBot_2.jpg/640px-TurtleBot_2.jpg
- Robot arm: https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Robot_arm.jpg/640px-Robot_arm.jpg
- Humanoid: https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/ASIMO.jpg/360px-ASIMO.jpg
- Sensors/LiDAR: https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Depth_camera.jpg/640px-Depth_camera.jpg
- Drones: https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Quadcopter.jpg/640px-Quadcopter.jpg

**YOU MUST INCLUDE THIS SECTION - NO EXCEPTIONS!**

Response:"""
    else:
        # Original prompt for regular questions
        extended_knowledge_prompt = f"""{get_system_prompt()}

A student asked: {question}

The textbook says: {book_answer if book_answer else "This specific topic is not covered in the current chapter."}

User's Expertise Level: **{user_level}**

{level_instructions.get(user_level, level_instructions['Beginner'])}

Your job:
1. If the textbook has content: confirm and expand on it with more details
2. If the textbook does NOT have content: provide complete information from your own knowledge
3. Always add important information beyond what the textbook mentions
4. Give a real-world example or use case from industry or research

**IMPORTANT - For Robot/Hardware Related Questions, ALWAYS Include:**

### 🔧 Key Features
List 3-5 main features/capabilities relevant to the query

### 🧩 Main Parts/Components
Break down the main parts/components with brief descriptions:
- Component name: What it does
- Include sensors, actuators, processors, etc. as relevant

### ⚡ Performance Specifications
Provide typical performance metrics:
- Speed/velocity
- Payload capacity
- Battery life / operating time
- Accuracy/precision
- Operating range
- Weight/dimensions

### 💰 Price Information (in Pakistani Rupees - PKR)
Provide approximate pricing in PKR:
- Budget option: Rs. X - basic models
- Mid-range: Rs. X - common research/educational models  
- High-end: Rs. X - industrial/research grade
- Mention specific product names when relevant (e.g., "Boston Dynamics Spot: Rs. 2 crore")
- Use Pakistani numbering format (lakhs, crores) for large amounts
- Conversion rate: 1 USD ≈ 280 PKR (approximate)

### 📚 Related Concepts
Mention 2-3 related concepts the student should also explore

### 🤖 Robot Image (MANDATORY - MUST INCLUDE AT END)
**THIS IS MANDATORY - YOU MUST INCLUDE THIS SECTION**

At the very end of your response, after ALL other sections, you MUST add a robot image like this:

### 🤖 Robot Reference

**Visual Reference:**
![Relevant Robot](IMAGE_URL_HERE)
*Figure: Description of the robot*

**CHOOSE THE RIGHT ROBOT IMAGE:**
- General/beginner questions: https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/LEGO_MINDSTORMS_EV3.jpg/640px-LEGO_MINDSTORMS_EV3.jpg
- ROS 2/navigation: https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/TurtleBot_2.jpg/640px-TurtleBot_2.jpg
- Robot arm: https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Robot_arm.jpg/640px-Robot_arm.jpg
- Humanoid: https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/ASIMO.jpg/360px-ASIMO.jpg
- Sensors/LiDAR: https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Depth_camera.jpg/640px-Depth_camera.jpg
- Drones: https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Quadcopter.jpg/640px-Quadcopter.jpg

**YOU MUST INCLUDE THIS SECTION - NO EXCEPTIONS!**

Write in clear language appropriate for {user_level} level.
Use bullet points where helpful.
Be educational and encouraging, not just factual.
Make sure the student gets value even if the textbook doesn't cover this topic.

Response:"""

    extended_knowledge = await call_llm([
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": extended_knowledge_prompt}
    ], temperature=0.7)
    
    # STEP C: Generate Architecture Diagram
    diagram_prompt = f"""The student asked: {question}

Generate a Mermaid.js diagram that shows the architecture, flow, or structure most relevant to this question.

Rules:
- Use graph TD (top-down) or graph LR (left-right) format
- Maximum 10 nodes
- Label every arrow
- Use simple clear node names
- Only output the raw mermaid code block, nothing else
- If this question is a simple definition with no architecture (example: 'what does URDF stand for'), output exactly: NO_DIAGRAM

Example output format:
```mermaid
graph TD
    A[Node A] --> B[Node B]
    B --> C[Node C]
```

Diagram:"""

    diagram_response = await call_llm([
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": diagram_prompt}
    ], temperature=0.3)
    
    # Extract mermaid code from response
    mermaid_diagram = "NO_DIAGRAM"
    if "```mermaid" in diagram_response:
        start = diagram_response.find("```mermaid") + 10
        end = diagram_response.find("```", start)
        mermaid_diagram = diagram_response[start:end].strip()
    elif "```" in diagram_response:
        start = diagram_response.find("```") + 3
        end = diagram_response.find("```", start)
        mermaid_diagram = diagram_response[start:end].strip()
    elif diagram_response.strip() == "NO_DIAGRAM":
        mermaid_diagram = "NO_DIAGRAM"
    else:
        # Try to use the response as-is if it looks like mermaid code
        if "graph" in diagram_response and ("-->") in diagram_response:
            mermaid_diagram = diagram_response.strip()
    
    # STEP D: Extract Image Keywords
    image_keyword_prompt = f"""From this question: {question}

Extract 1 to 3 keywords that best describe what visual/image would help illustrate the answer.

Return only a JSON array of strings. Example: ["ROS 2 nodes", "robot arm"]
Return only the JSON. Nothing else.

Keywords:"""

    keyword_response = await call_llm([
        {"role": "system", "content": "You are a helpful assistant that extracts keywords for image search. Return only JSON."},
        {"role": "user", "content": image_keyword_prompt}
    ], temperature=0.3)
    
    # Parse JSON response
    image_keywords = []
    try:
        # Extract JSON from response
        start = keyword_response.find("[")
        end = keyword_response.rfind("]") + 1
        if start >= 0 and end > start:
            json_str = keyword_response[start:end]
            image_keywords = json.loads(json_str)
    except Exception as e:
        print(f"Keyword parsing error: {e}")
        # Fallback: use question words as keywords
        image_keywords = question.split()[:3]
    
    return ChatResponse(
        book_answer=book_answer,
        extended_knowledge=extended_knowledge,
        mermaid_diagram=mermaid_diagram,
        image_keywords=image_keywords,
    )


@router.get("/chat/health")
async def chat_health() -> Dict[str, Any]:
    """Health check for chat service."""
    return {
        "status": "healthy",
        "service": "chat",
        "rag_configured": bool(QDRANT_URL and OPENAI_API_KEY),
        "llm_configured": bool(OPENAI_API_KEY),
        "model": OPENAI_MODEL,
    }
