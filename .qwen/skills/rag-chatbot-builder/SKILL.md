# RAG-Chatbot-Builder Subagent

**Specialized agent for building Retrieval-Augmented Generation chatbots for textbook websites.**

## Goal
Develop a production-ready RAG chatbot that answers questions based on textbook content using Qdrant for retrieval and OpenAI GPT for generation.

## Requirements
- Backend using FastAPI
- Query Qdrant vector database
- Retrieve relevant book content
- Send retrieved context to OpenAI GPT model
- Return final answer to user

## Features
- Answer questions based on entire book knowledge
- Answer questions based on selected/custom text
- Provide source references (chapter + section)
- Support follow-up questions (conversation history)
- Stream responses for better UX

## Technology Stack
- FastAPI for REST API
- OpenAI GPT-3.5-turbo or GPT-4
- Qdrant Cloud for vector search
- Python with async support

## Output Files
- `main.py` - FastAPI server with chat endpoints
- `rag_pipeline.py` - RAG orchestration logic
- `qdrant_client.py` - Qdrant database client wrapper

## Usage
```bash
# Invoke the subagent
skill: "rag-chatbot-builder"
```

## API Endpoints
- `POST /chat` - Send a question, get an answer
- `POST /chat/stream` - Stream response in real-time
- `GET /sources` - Get sources for a specific answer
- `POST /feedback` - Submit feedback on answer quality

## Environment Variables Required
```
OPENAI_API_KEY=your_openai_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
```
