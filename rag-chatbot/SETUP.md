# RAG Chatbot - Complete Setup Guide

## Overview

This RAG (Retrieval-Augmented Generation) chatbot answers questions based on textbook content about Physical AI & Humanoid Robotics.

## Architecture

```
┌─────────────────┐
│  Docusaurus     │
│  Book           │
│                 │
│  [Chat Widget]──┼──────┐
└─────────────────┘      │
                         ▼
                  ┌─────────────┐
                  │  FastAPI    │
                  │  Backend    │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  RAG        │
                  │  Pipeline   │
                  └──────┬──────┘
                         │
            ┌────────────┼────────────┐
            ▼                         ▼
     ┌─────────────┐          ┌─────────────┐
     │  SQLite     │          │  OpenAI     │
     │  Vector DB  │          │  (Optional) │
     └─────────────┘          └─────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
cd rag-chatbot
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file in project root:

```env
# OpenAI API (optional - for advanced features)
OPENAI_API_KEY=your-openai-api-key

# Qdrant Cloud (optional - for production vector search)
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key

# For local development, use:
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Ingest Textbook Content

Choose one of these options:

#### Option A: Simple Local Vector Store (Recommended for Development)

```bash
cd backend
python simple_ingest.py --docs-dir ../book/docs
```

This creates a SQLite-based vector store (`vector_store.db`) that works without external services.

#### Option B: Qdrant Cloud (For Production)

```bash
cd backend
python ingest_book.py --docs-dir ../book/docs
```

Requires valid Qdrant Cloud credentials in `.env`.

#### Option C: Local Qdrant with Docker

```bash
# Start local Qdrant
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant

# Then run ingestion
cd backend
python ingest_book.py --docs-dir ../book/docs
```

### 4. Start the Chatbot Server

#### Simple Version (SQLite-based)

```bash
cd backend
python main_simple.py
```

#### Full Version (Qdrant + OpenAI)

```bash
cd backend
python main.py
```

Server will start at `http://localhost:8000`

### 5. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What is RAG?\", \"top_k\": 3}"
```

## Integrating with Docusaurus

### Step 1: Copy Chat Widget

Copy `chat-widget.js` to your Docusaurus project:

```bash
cp chat-widget.js /path/to/docusaurus-project/static/js/
```

### Step 2: Update Docusaurus Config

Edit `docusaurus.config.js`:

```javascript
module.exports = {
  // ... other config
  scripts: [
    // ... other scripts
    {
      src: '/js/chat-widget.js',
      async: true,
      defer: true,
    },
  ],
};
```

### Step 3: Customize Widget (Optional)

Edit the widget configuration in `chat-widget.js`:

```javascript
const CONFIG = {
  API_URL: 'http://localhost:8000',  // Change to your backend URL
  BOT_NAME: 'Textbook Assistant',
  BOT_AVATAR: '🤖',
  THEME_COLOR: '#2563eb',  // Match your brand color
  POSITION: 'bottom-right',  // or 'bottom-left'
};
```

### Step 4: Build and Deploy Docusaurus

```bash
npm run build
npm run serve
```

## API Endpoints

### POST /chat

Get an answer to a question.

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
      "chapter": "Chapter 5",
      "section": "What is ROS 2?",
      "url": "/docs/chapter5",
      "score": 0.95
    }
  ],
  "confidence": 0.89,
  "query": "What is ROS 2?",
  "chunks_retrieved": 5
}
```

### GET /health

Check service health.

**Response:**
```json
{
  "status": "healthy",
  "vector_store_connected": true,
  "collection_name": "local_vector_store",
  "vector_count": 60
}
```

### GET /sources

Get sources for a query without generating an answer.

**Request:**
```
GET /sources?query=What%20is%20ROS%202&top_k=5
```

## Textbook Content

The chatbot is trained on the following textbook chapters:

1. **Chapter 1**: Introduction to RAG Systems
2. **Chapter 2**: Vector Databases and Embeddings
3. **Chapter 3**: Introduction to Physical AI
4. **Chapter 4**: Humanoid Robotics Fundamentals
5. **Chapter 5**: ROS 2 for Robotics Development
6. **Chapter 6**: Sensors and Perception Systems
7. **Chapter 7**: Motion Planning and Control
8. **Chapter 8**: Machine Learning for Robotics
9. **Chapter 9**: Vision-Language-Action (VLA) Models
10. **Chapter 10**: Digital Twins and Simulation
11. **Chapter 11**: System Integration and Deployment

## Troubleshooting

### "Collection not found"

Run the ingestion script first:
```bash
python simple_ingest.py --docs-dir ../book/docs
```

### "Connection refused" on localhost:8000

Make sure the server is running:
```bash
python main_simple.py
```

### Chat widget not appearing

1. Check browser console for errors
2. Verify the script path in docusaurus.config.js
3. Make sure API_URL is correct

### Poor search results

The simple vector store uses keyword matching. For better semantic search:

1. Install sentence-transformers:
   ```bash
   pip install sentence-transformers
   ```

2. Re-run ingestion:
   ```bash
   python simple_ingest.py --docs-dir ../book/docs
   ```

### Qdrant connection errors

For Qdrant Cloud, verify:
- URL is correct (no port number)
- API key is valid
- Cluster is active

For local Qdrant:
```bash
docker ps  # Check if container is running
docker logs qdrant  # Check logs
```

## Production Deployment

### Environment Variables

```bash
# Use production values
export OPENAI_API_KEY=sk-...
export QDRANT_URL=https://your-cluster.qdrant.io
export QDRANT_API_KEY=your-api-key
export API_HOST=0.0.0.0
export API_PORT=8000
```

### Using Gunicorn

```bash
pip install gunicorn
gunicorn main_simple:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY book/docs/ ./book/docs/
COPY chat-widget.js ./

WORKDIR /app/backend
RUN python simple_ingest.py --docs-dir ../book/docs

EXPOSE 8000

CMD ["python", "main_simple.py"]
```

Build and run:
```bash
docker build -t rag-chatbot .
docker run -p 8000:8000 rag-chatbot
```

## Development Tips

### Hot Reload

```bash
pip install uvicorn[standard]
python main_simple.py --reload
```

### Testing with curl

```bash
# Simple question
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain vector embeddings", "top_k": 3}'

# With sources
curl "http://localhost:8000/sources?query=humanoid%20robotics&top_k=5"

# Health check
curl "http://localhost:8000/health"
```

### Viewing Logs

The server logs to stdout with timestamps:
```
2024-01-15 10:30:45 - main_simple - INFO - Starting RAG Chatbot server...
2024-01-15 10:30:46 - simple_ingest - INFO - Processing query: What is ROS 2?...
```

## Performance Optimization

### For Better Search Quality

1. Use sentence-transformers for semantic search
2. Increase chunk size for more context
3. Use OpenAI embeddings for higher quality

### For Faster Response

1. Use keyword search (default in simple mode)
2. Reduce top_k parameter
3. Cache frequent queries

### For Scalability

1. Use Qdrant Cloud for distributed vector search
2. Add Redis for response caching
3. Use multiple worker processes

## License

MIT License

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs for error messages
3. Verify API endpoints with curl
4. Test with simple queries first
