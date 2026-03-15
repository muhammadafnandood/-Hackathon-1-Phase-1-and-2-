# RAG Chatbot for Physical AI Textbook

A Retrieval-Augmented Generation (RAG) chatbot that answers questions based on textbook content about Physical AI & Humanoid Robotics.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   User      │────▶│  FastAPI     │────▶│   OpenAI    │
│  Question   │     │   Backend    │     │    GPT      │
└─────────────┘     └──────┬───────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Qdrant     │
                    │  Vector DB   │
                    └──────────────┘
```

## Project Structure

```
rag-chatbot/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── rag_pipeline.py      # RAG orchestration logic
│   ├── qdrant_client.py     # Qdrant database wrapper
│   ├── ingest_book.py       # Document ingestion script
│   ├── database.py          # SQLAlchemy DB session (optional)
│   └── ingest.py            # Legacy ingestion (deprecated)
├── book/
│   └── docs/
│       ├── chapter1.md      # Textbook chapters
│       └── chapter2.md
├── docs/                     # Additional documentation
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Quick Start

### 1. Install Dependencies

```bash
cd rag-chatbot
pip install -r requirements.txt
```

### 2. Configure Environment

Create/update `.env` file in project root:

```env
# OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key

# Optional: Database for feedback
NEON_DB_URL=postgresql://user:pass@host/dbname

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
RAG_COLLECTION=textbook_knowledge
```

### 3. Ingest Textbook Content

```bash
cd backend
python ingest_book.py
```

Options:
```bash
# Full ingestion
python ingest_book.py

# Rebuild from scratch
python ingest_book.py --rebuild

# Preview without ingesting
python ingest_book.py --dry-run

# Show collection stats
python ingest_book.py --stats
```

### 4. Start the Chatbot Server

```bash
python main.py
```

Server will start at `http://localhost:8000`

### 5. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?", "top_k": 5}'
```

## API Endpoints

### POST /chat
Get an answer to a question.

**Request:**
```json
{
  "query": "What is ROS 2?",
  "top_k": 5,
  "include_sources": true,
  "use_mmr": true,
  "programming_experience": "intermediate",
  "robotics_knowledge": "beginner",
  "ai_experience": "intermediate",
  "hardware_experience": "beginner"
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
      "url": "/docs/ros2-basics",
      "score": 0.89
    }
  ],
  "confidence": 0.85,
  "query": "What is ROS 2?",
  "model_used": "gpt-3.5-turbo",
  "chunks_retrieved": 5,
  "user_profile": {
    "programming_experience": "intermediate",
    "robotics_knowledge": "beginner",
    "ai_experience": "intermediate",
    "hardware_experience": "beginner"
  },
  "personalization_applied": true
}
```

### POST /profile/analyze
Get personalized learning recommendations based on user's background.

**Request:**
```json
{
  "programming_experience": "beginner",
  "robotics_knowledge": "beginner",
  "ai_experience": "intermediate",
  "hardware_experience": "beginner",
  "learning_style": "hands-on",
  "goals": "Build a humanoid robot simulation"
}
```

**Response:**
```json
{
  "profile": {
    "programming_experience": "beginner",
    "robotics_knowledge": "beginner",
    "ai_experience": "intermediate",
    "hardware_experience": "beginner",
    "learning_style": "hands-on",
    "goals": "Build a humanoid robot simulation"
  },
  "overall_level": "beginner",
  "recommendations": [
    "Start with Python basics before diving into ROS 2 nodes",
    "Learn fundamental robotics concepts: sensors, actuators, control loops",
    "Focus on simulation first; hardware can be added later",
    "Follow chapters in order - each builds on previous concepts",
    "Run all code examples yourself to build muscle memory",
    "Join the community forum to ask questions"
  ]
}
```

### POST /chat/stream
Stream response in real-time using Server-Sent Events.

### GET /health
Check service health.

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

### POST /feedback
Submit feedback on an answer.

**Request:**
```json
{
  "query": "What is ROS 2?",
  "answer": "ROS 2 is...",
  "rating": 5,
  "feedback_text": "Very helpful!"
}
```

### GET /sources
Get source information for a query.

**Request:**
```
GET /sources?query=What%20is%20ROS%202&top_k=5
```

## Features

### Semantic Search
- Uses OpenAI `text-embedding-ada-002` for embeddings
- Cosine similarity search in Qdrant
- Configurable relevance threshold

### Maximal Marginal Relevance (MMR)
- Balances relevance with diversity
- Prevents redundant results
- Configurable lambda parameter

### Learning Personalization
- Adapts explanations to user's technical background
- Supports 4 domains: programming, robotics, AI, hardware
- Three levels: beginner, intermediate, advanced
- Personalized learning recommendations

### Urdu Translation
- Translates content to Urdu while preserving technical terms
- Maintains markdown formatting and code blocks
- Automated translation pipeline

### Diagram Generation
- Auto-generates Mermaid diagrams for robotics concepts
- Supports ROS 2, RAG, VLA, perception, navigation architectures
- Docusaurus-compatible output

### Source Attribution
- Every answer includes chapter and section references
- Score-based ranking of sources
- Direct links to textbook pages

### Streaming Support
- Real-time response streaming
- Better user experience for long answers
- Server-Sent Events (SSE) protocol

## Chunking Strategy

The ingestion script uses **heading-based semantic chunking**:

1. Splits at `##` (H2) boundaries
2. Each section becomes one chunk
3. Preserves hierarchy in metadata
4. Filters chunks by length (50-2000 chars)

**Metadata stored per chunk:**
- `text`: Chunk content
- `chapter_title`: Parent chapter name
- `section_name`: Section heading
- `page_url`: Docusaurus-compatible URL
- `heading_level`: H2 or H3
- `chunk_index`: Position in document
- `source_file`: Original file path

## Qdrant Collection Schema

```
Collection: textbook_knowledge
Vector Size: 1536 (text-embedding-ada-002)
Distance: Cosine

Payload Fields:
- text: string
- chapter_title: string
- section_name: string
- page_url: string
- heading_level: integer
- chunk_index: integer
- total_chunks: integer
- source_file: string
- ingested_at: timestamp
```

## Configuration

### RAG Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `top_k` | 5 | Chunks to retrieve |
| `score_threshold` | 0.5 | Minimum similarity score |
| `mmr_lambda` | 0.7 | Relevance vs diversity balance |
| `max_tokens` | 600 | Max response length |
| `temperature` | 0.3 | GPT creativity (lower = more focused) |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `QDRANT_URL` | Yes | Qdrant Cloud URL |
| `QDRANT_API_KEY` | Yes | Qdrant API key |
| `API_HOST` | No | Server host (default: 0.0.0.0) |
| `API_PORT` | No | Server port (default: 8000) |
| `RAG_COLLECTION` | No | Collection name (default: textbook_knowledge) |

## Development

### Run in Development Mode

```bash
# Auto-reload on code changes
python main.py --reload

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain vector embeddings", "top_k": 3}'

# Test streaming
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a humanoid robot?"}'
```

### Logging

Logs are output to stdout with format:
```
2024-01-15 10:30:45 - main - INFO - Starting RAG Chatbot server...
2024-01-15 10:30:46 - rag_pipeline - INFO - Processing query: What is ROS 2?...
```

## Production Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY docs/ ./docs/

EXPOSE 8000

CMD ["python", "backend/main.py"]
```

### Environment Variables for Production

```bash
# Use secure values
export OPENAI_API_KEY=sk-...
export QDRANT_URL=https://...
export QDRANT_API_KEY=...
export API_HOST=0.0.0.0
export API_PORT=8000
export API_RELOAD=false
```

### Performance Tuning

For high-traffic deployments:

1. **Increase Qdrant connection pool:**
   ```python
   QdrantClient(..., grpc_options={"keepalive_timeout_ms": 30000})
   ```

2. **Use Gunicorn with Uvicorn workers:**
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Enable response caching:**
   ```python
   from fastapi_cache import FastAPICache
   from fastapi_cache.backends.redis import RedisBackend
   ```

## Troubleshooting

### "Collection not found"
Run `python ingest_book.py` to create the collection.

### "Rate limit exceeded"
OpenAI has rate limits. The pipeline includes exponential backoff retry logic.

### "Low confidence scores"
- Check if textbook content covers the query topic
- Lower `score_threshold` in `rag_pipeline.py`
- Increase `top_k` to retrieve more context

### "Connection timeout to Qdrant"
- Verify `QDRANT_URL` is correct
- Check network connectivity
- Increase timeout in `qdrant_client.py`

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request
