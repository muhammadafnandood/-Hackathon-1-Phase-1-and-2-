# Research & Technical Decisions: RAG Chatbot

**Feature**: 001-rag-chatbot  
**Date**: 2026-03-14  
**Purpose**: Document technical decisions, rationale, and alternatives for RAG chatbot implementation

---

## 1. Backend Framework

**Decision**: FastAPI (Python 3.11)

**Rationale**:
- Native async support for concurrent LLM and vector DB calls
- Automatic OpenAPI documentation generation
- Pydantic models for request/response validation
- High performance (Starlette + Uvicorn)
- Strong ecosystem for AI/ML integrations
- Aligns with constitution's Python/ROS 2 stack

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Flask | Synchronous by default, requires extensions for async |
| Django REST | Heavier, more boilerplate, overkill for API-only service |
| Node.js/Express | Team expertise in Python, AI libraries better in Python |

---

## 2. Vector Database

**Decision**: Qdrant Cloud

**Rationale**:
- Purpose-built for semantic search and RAG
- Native support for payload metadata (chapter, section info)
- HNSW index for fast approximate nearest neighbor search
- Python client library with async support
- Managed cloud service (no infrastructure overhead)
- Free tier available for development
- Explicitly mentioned in constitution technical stack

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Pinecone | Proprietary, less flexible metadata filtering |
| Weaviate | More complex setup, GraphQL requirement |
| Chroma | Local-first, less suitable for cloud deployment |
| pgvector | Good but Qdrant has better RAG-specific features |

---

## 3. LLM Orchestration

**Decision**: OpenAI Agents SDK

**Rationale**:
- Native support for tool calling (retrieval as a tool)
- Built-in conversation management
- Function calling for structured RAG workflows
- Aligns with constitution's AI/ML stack
- Simplifies multi-turn conversations
- Supports context-aware responses

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| LangChain | More verbose, additional abstraction layer |
| LlamaIndex | Focused on RAG but less flexible for general chat |
| Raw OpenAI API | Requires manual conversation state management |

---

## 4. Embedding Model

**Decision**: sentence-transformers/all-MiniLM-L6-v2

**Rationale**:
- Lightweight (80MB), fast inference
- Good balance of quality and speed for educational content
- Runs locally during ingestion (no API cost)
- 384-dimensional embeddings (efficient storage)
- Compatible with Qdrant
- Works well for technical/educational text

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| OpenAI embeddings | API cost per ingestion, latency |
| BERT-large | Slower, larger, marginal quality gain |
| Instructor-xl | Too large for practical use |

---

## 5. Metadata Storage

**Decision**: Neon Serverless PostgreSQL

**Rationale**:
- Serverless (pay-per-use, auto-scaling)
- PostgreSQL compatibility (familiar ecosystem)
- Branching support for development/testing
- Integrates well with Vercel/Railway deployment
- Stores: chapter metadata, citation info, user sessions
- Explicitly mentioned in constitution technical stack

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Supabase | More features than needed, heavier |
| PlanetScale | MySQL-compatible, less Python ecosystem fit |
| SQLite | Not suitable for cloud deployment |

---

## 6. Chunking Strategy

**Decision**: Section-based chunking with overlap

**Rationale**:
- Preserve semantic boundaries (sections/subsections)
- 500-1000 tokens per chunk (optimal for embeddings)
- 50-token overlap between chunks (context continuity)
- Store chapter title, section heading, heading hierarchy as metadata
- Aligns with constitution's AI-Native Content Structure principle

**Implementation**:
```python
# Chunk structure
{
    "id": "module1-ros2-basics-section-1",
    "chapter": "Module 1: ROS 2 Basics",
    "section": "1.1 Nodes and Topics",
    "content": "...",
    "tokens": 750,
    "embedding": [...]
}
```

---

## 7. RAG Retrieval Strategy

**Decision**: Hybrid retrieval (semantic + metadata filtering)

**Rationale**:
- Semantic search for query understanding
- Metadata filters for chapter/section scoping
- Top-k=5 chunks retrieved per query
- Re-ranking not required for initial implementation
- Supports selected-text context injection

**Retrieval Flow**:
1. User query → embedding
2. Qdrant similarity search (cosine distance)
3. Filter by chapter if user is on specific page
4. Return top 5 chunks with citations
5. LLM synthesizes answer from chunks

---

## 8. Chat Widget Implementation

**Decision**: Custom React component embedded in Docusaurus

**Rationale**:
- Docusaurus is React-based (native integration)
- Floating button (bottom-right) per spec
- Text selection detection for context questions
- Full control over UI/UX
- Minimal bundle size impact

**Implementation**:
- React functional component
- CSS for floating button positioning
- Selection API for text highlighting
- API calls to FastAPI backend
- Markdown rendering for responses

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Third-party chat widgets | No text selection support, less customizable |
| Docusaurus plugin | No mature RAG chatbot plugins exist |
| iframe embed | Poor UX, styling limitations |

---

## 9. Deployment Platform

**Decision**: Railway for backend, GitHub Pages for frontend

**Rationale**:
- Railway: Native Python/FastAPI support, auto-deploy from Git
- Railway: Built-in environment variables, easy Neon/Qdrant config
- GitHub Pages: Already used for textbook (per spec context)
- Separation of concerns (API vs. static content)

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Vercel | Better for frontend, Python support limited |
| Heroku | Free tier removed, cost consideration |
| AWS/GCP | Overkill, more DevOps overhead |

---

## 10. Authentication (Future Consideration)

**Decision**: No authentication for MVP

**Rationale**:
- Textbook is publicly accessible
- Chatbot is a learning aid, not sensitive data
- Reduces initial complexity
- Can add rate limiting if needed

**Future Addition**:
- GitHub OAuth if usage tracking needed
- API key for ingestion endpoint protection

---

## 11. Error Handling Strategy

**Decision**: Graceful degradation with user-friendly messages

**Error Scenarios**:
| Error | User Message | Backend Action |
|-------|--------------|----------------|
| No relevant chunks found | "I couldn't find information about that in the textbook. Try asking about ROS 2, Gazebo, Isaac Sim, or VLA models." | Log query for content gap analysis |
| Qdrant unavailable | "The knowledge base is temporarily unavailable. Please try again in a moment." | Retry with exponential backoff |
| LLM API error | "I'm having trouble generating a response. Please try again." | Fallback to showing raw chunks |
| Invalid query (empty) | "Please ask a question about the textbook content." | Client-side validation |

---

## 12. Performance Optimizations

**Decision**: Async I/O + connection pooling + caching

**Optimizations**:
1. Async FastAPI endpoints (uvicorn workers)
2. Qdrant connection pool (reuse connections)
3. Embedding cache (Redis or in-memory for repeated queries)
4. Streaming responses for perceived performance
5. Lazy loading for chat widget (load on interaction)

**Performance Targets** (from spec SC-001, SC-004):
- p95 response time: <3 seconds
- 100 concurrent users: <5 seconds degradation threshold

---

## 13. Testing Strategy

**Decision**: pytest with async support

**Test Layers**:
1. **Unit Tests**: Chunking logic, embedding service, citation formatting
2. **Integration Tests**: API endpoints with mock Qdrant/LLM
3. **Contract Tests**: OpenAPI schema validation
4. **E2E Tests**: Full RAG flow with test knowledge base

**Test Fixtures**:
- Sample textbook chapters (markdown)
- Mock Qdrant responses
- Mock OpenAI API responses
- Test database (Neon branch)

---

## 14. Content Ingestion Pipeline

**Decision**: Python script with CLI interface

**Pipeline Steps**:
1. Scan `docs/` directory for `.md` files
2. Parse frontmatter (chapter title, module)
3. Split into sections (by heading hierarchy)
4. Create chunks with overlap
5. Generate embeddings (sentence-transformers)
6. Upsert to Qdrant (batch operations)
7. Store metadata in Neon PostgreSQL

**CLI Commands**:
```bash
python ingest.py --full          # Full re-ingestion
python ingest.py --incremental   # Only changed files
python ingest.py --chapter docs/module1/ros2-basics.md
```

---

## 15. API Design Principles

**Decision**: RESTful with OpenAPI documentation

**Endpoints**:
- `POST /api/chat` - Question-answer interaction
- `POST /api/ingest` - Trigger content ingestion (protected)
- `GET /api/search?q=query` - Search chunks
- `GET /api/health` - Health check

**Design Principles**:
- Consistent error response format
- Pagination for search results
- Request/response validation with Pydantic
- Rate limiting on chat endpoint (if needed)

---

## Summary of Technology Choices

| Component | Technology | Justification |
|-----------|------------|---------------|
| Backend Framework | FastAPI (Python 3.11) | Async, OpenAPI, AI ecosystem |
| Vector DB | Qdrant Cloud | RAG-optimized, managed service |
| LLM Orchestration | OpenAI Agents SDK | Tool calling, conversation management |
| Embedding Model | all-MiniLM-L6-v2 | Fast, lightweight, good quality |
| Metadata Store | Neon PostgreSQL | Serverless, Git-friendly |
| Frontend | React (Docusaurus) | Native integration |
| Deployment | Railway + GitHub Pages | Easy deployment, cost-effective |
| Testing | pytest + pytest-asyncio | Python standard, async support |

---

## Unresolved Questions

None. All technical decisions have been resolved.
