# RAG-Chatbot-Builder Instructions

## Role
You are an expert backend engineer specializing in RAG (Retrieval-Augmented Generation) systems. Your task is to build a production-ready chatbot for textbook Q&A.

## Architecture

```
User Question
    ↓
[FastAPI Endpoint]
    ↓
[RAG Pipeline]
    ↓
[Qdrant Client] → Retrieve relevant chunks
    ↓
[OpenAI GPT] → Generate answer with context
    ↓
[Response with Sources]
```

## Component Responsibilities

### main.py (FastAPI Server)
- Define REST API endpoints
- Request/response validation with Pydantic
- CORS configuration for frontend
- Error handling and logging
- Health check endpoint

### rag_pipeline.py (RAG Orchestration)
- Embed user query
- Retrieve top-k relevant chunks from Qdrant
- Rank and filter results
- Construct prompt for GPT
- Parse GPT response and extract sources
- Handle conversation history

### qdrant_client.py (Database Wrapper)
- Connection management
- Search with filters
- Batch operations
- Connection pooling
- Retry logic

## RAG Pipeline Flow

### Step 1: Query Embedding
```python
query_vector = openai.embeddings.create(
    model="text-embedding-ada-002",
    input=query
)
```

### Step 2: Vector Search
```python
results = qdrant.search(
    collection_name="textbook_knowledge",
    query_vector=query_vector,
    limit=5,
    score_threshold=0.7
)
```

### Step 3: Context Construction
```python
context = "\n\n".join([chunk.text for chunk in results])
sources = [{
    "chapter": chunk.chapter_title,
    "section": chunk.section_name,
    "url": chunk.page_url
} for chunk in results]
```

### Step 4: Prompt Engineering
```python
prompt = f"""You are a helpful textbook assistant. Answer based on the context below.
If the answer isn't in the context, say "I don't have information about that in the textbook."

Context:
{context}

Question: {query}
Answer:"""
```

### Step 5: Response Generation
```python
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful textbook assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=500
)
```

## API Design

### POST /chat
**Request:**
```json
{
  "query": "What is ROS 2?",
  "top_k": 5,
  "include_sources": true
}
```

**Response:**
```json
{
  "answer": "ROS 2 is a middleware for robotics...",
  "sources": [
    {
      "chapter": "Introduction to ROS 2",
      "section": "Core Concepts",
      "url": "/docs/ros2-basics"
    }
  ],
  "confidence": 0.85
}
```

### POST /chat/stream
**Request:** Same as /chat
**Response:** Server-Sent Events (SSE) stream

### GET /health
**Response:**
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "openai_connected": true,
  "collection_name": "textbook_knowledge",
  "vector_count": 1250
}
```

## Quality Guidelines

### Answer Quality
- Answers must be grounded in retrieved context
- Cite sources for every claim
- Admit uncertainty when context is insufficient
- Keep answers concise (200-500 words typical)

### Retrieval Quality
- Use score threshold to filter low-relevance results
- Implement MMR (Maximal Marginal Relevance) for diversity
- Support metadata filtering (by chapter, section)

### Error Handling
- Handle Qdrant connection failures gracefully
- Handle OpenAI rate limits with retries
- Return helpful error messages to users

## Security Considerations
- Validate all user inputs
- Rate limit API endpoints
- Sanitize context before sending to GPT
- Log queries for analytics (without storing PII)

## Performance Targets
- P95 latency < 2 seconds for /chat
- Support 100 concurrent requests
- Cache frequent queries
- Stream responses for perceived speed

## Testing Requirements
- Unit tests for each component
- Integration tests with mock Qdrant/OpenAI
- End-to-end tests for full pipeline
- Load testing for concurrent users
