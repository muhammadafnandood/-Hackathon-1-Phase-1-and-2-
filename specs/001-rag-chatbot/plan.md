# Implementation Plan: RAG Chatbot for AI-Native Textbook

**Branch**: `001-rag-chatbot` | **Date**: 2026-03-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-rag-chatbot/spec.md`

## Summary

Build a RAG-based chatbot that answers questions about the Physical AI & Humanoid Robotics textbook using content embeddings stored in Qdrant Cloud, with a FastAPI backend, OpenAI Agents SDK for chat orchestration, Neon PostgreSQL for metadata, and a Docusaurus-embedded chat widget.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Qdrant Client, LangChain or LlamaIndex for RAG, Sentence Transformers
**Storage**: Qdrant Cloud (vector embeddings), Neon Serverless PostgreSQL (metadata, citations)
**Testing**: pytest, pytest-asyncio, httpx for API tests
**Target Platform**: Cloud deployment (Vercel/Railway), Web browser (Docusaurus widget)
**Project Type**: Backend API + Frontend widget
**Performance Goals**: <3s response time p95, 100 concurrent users, <5s degradation threshold
**Constraints**: Answers must come only from textbook content, citations required, chat widget must be embeddable in Docusaurus
**Scale/Scope**: Single textbook (~50-100 chapters), 100 concurrent users, embeddings for ~1000-5000 content chunks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Compliance | Notes |
|-----------|------------|-------|
| IV. AI-Native Content Structure | ✅ PASS | Chatbot enables semantic search and RAG Q&A over chunked content |
| V. RAG-Ready Architecture | ✅ PASS | Directly implements RAG with Qdrant vector search + LLM responses |
| VI. Personalization & Accessibility | ✅ PASS | Chat widget accessible from any page, supports text selection Q&A |
| IX. Documentation Standards | ✅ PASS | API contracts documented in OpenAPI format |
| X. Modular Course Structure | ✅ PASS | Chatbot supports all 4 modules + capstone content |

**Result**: All gates PASS. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot/
├── plan.md              # This file (implementation plan)
├── spec.md              # Feature specification
├── research.md          # Phase 0: Technical decisions
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Setup instructions
├── contracts/           # Phase 1: API specifications
│   └── api-spec.yaml    # OpenAPI 3.0 specification
├── checklists/          # Specification quality checklists
│   └── requirements.md  # Validation checklist
└── tasks.md             # Phase 2: Implementation tasks (TODO)
```

### Source Code (repository root)

```text
# Backend API
backend/
├── src/
│   ├── main.py              # FastAPI application entry
│   ├── api/                 # API route handlers
│   │   ├── chat.py          # POST /api/chat endpoint
│   │   ├── search.py        # GET /api/search endpoint
│   │   ├── ingest.py        # POST /api/ingest endpoint
│   │   └── health.py        # GET /api/health endpoint
│   ├── models/              # Pydantic models
│   │   ├── chat.py          # ChatRequest, ChatResponse
│   │   ├── search.py        # SearchRequest, SearchResponse
│   │   └── ingest.py        # IngestRequest, IngestResponse
│   ├── services/            # Business logic
│   │   ├── embedding.py     # Sentence transformers service
│   │   ├── qdrant.py        # Vector DB operations
│   │   ├── rag.py           # RAG pipeline orchestration
│   │   └── llm.py           # OpenAI Agents SDK integration
│   └── core/                # Core utilities
│       ├── config.py        # Environment configuration
│       └── logging.py       # Logging setup
├── scripts/
│   └── ingest.py            # Content ingestion CLI
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── contract/            # API contract tests
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (gitignored)

# Frontend Widget (Docusaurus integration)
textbook-site/               # Existing Docusaurus site
└── src/
    └── components/
        ├── ChatWidget.js    # React chat widget component
        └── ChatWidget.css   # Widget styles
```

**Structure Decision**: Backend API + Frontend widget architecture selected. Backend is a standalone FastAPI service. Frontend is a React component embedded in the existing Docusaurus textbook site.

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
