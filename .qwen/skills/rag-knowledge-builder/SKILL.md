# RAG-Knowledge-Builder Subagent

**Specialized agent for preparing book content and ingesting it into a RAG-ready vector database.**

## Goal
Automatically process textbook markdown files, split them into semantic chunks, generate embeddings, and store them in Qdrant for RAG chatbot consumption.

## Tasks
1. Scan all markdown files in the `/docs` folder
2. Split content into semantic chunks (by headings/sections)
3. Generate embeddings using OpenAI embedding models
4. Store vectors inside Qdrant Cloud vector database
5. Save metadata including:
   - Chapter title
   - Section name
   - Page URL/slug

## Technology Stack
- Python 3.9+
- OpenAI embeddings (`text-embedding-ada-002`)
- Qdrant Cloud vector database
- FastAPI (for optional API endpoints)

## Output
- `ingest_book.py` - Main ingestion script
- Configuration for Qdrant connection
- Chunking strategies for different content types

## Usage
```bash
# Invoke the subagent
skill: "rag-knowledge-builder"
```

## Example Commands
- "Ingest all docs into Qdrant"
- "Rebuild the knowledge base with new chunking strategy"
- "Check ingestion status and vector count"

## Environment Variables Required
```
OPENAI_API_KEY=your_openai_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
```
