# Implementation Plan: AI-Native Textbook Platform for Physical AI & Humanoid Robotics

**Branch**: `master` | **Date**: 2026-03-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification for AI-native textbook with RAG chatbot

## Summary

Build an **AI-native textbook platform** using Docusaurus that teaches Physical AI & Humanoid Robotics with an integrated **RAG chatbot** (FastAPI + Qdrant + OpenAI) for interactive learning. The platform provides personalized content adaptation, Urdu translation, and BetterAuth authentication to create an accessible, AI-assisted learning experience for robotics students.

## Technical Context

**Language/Version**: 
- Frontend: TypeScript 5.x, React 18, Docusaurus 3.x
- Backend: Python 3.11, FastAPI 0.109+

**Primary Dependencies**: 
- BetterAuth (authentication)
- Qdrant (vector database)
- Neon PostgreSQL (metadata storage)
- OpenAI API (embeddings: text-embedding-3-large, LLM: GPT-4-turbo)
- LangChain (RAG orchestration)
- pg (PostgreSQL client for Node.js)

**Storage**: 
- Qdrant Cloud: Vector embeddings (textbook chunks)
- Neon PostgreSQL: User profiles, sessions, chat history, translations cache
- File system: Markdown content (Docusaurus docs/)

**Testing**: 
- Frontend: Jest, React Testing Library
- Backend: pytest, httpx for API tests
- E2E: Playwright

**Target Platform**: 
- Web browser (Chrome, Firefox, Safari, Edge)
- Server: Linux (Ubuntu 22.04) for backend services

**Project Type**: Web application (frontend: Docusaurus/React, backend: FastAPI)

**Performance Goals**: 
- Page load < 2 seconds
- Chatbot response < 3 seconds (p95)
- RAG retrieval < 500ms
- Translation generation < 10 seconds
- Support 1000 concurrent users

**Constraints**: 
- API response time < 200ms p95 (excluding LLM)
- Vector DB: < 100ms search latency
- Memory: < 512MB for backend services
- Offline-capable: No (requires API for AI features)

**Scale/Scope**: 
- 4 modules + capstone = ~25 chapters
- 100k+ vector embeddings
- 10k+ users (year 1 target)
- ~50 API endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Educational Clarity** | ✅ PASS | All chapters include learning objectives, explanations, code examples, labs, summaries, exercises |
| **II. Step-by-Step Progression** | ✅ PASS | Content structured from basics to advanced, incremental tutorials |
| **III. Practical Engineering Focus** | ✅ PASS | ROS 2 Python code, simulation workflows, deployment-ready configs |
| **IV. AI-Native Content Structure** | ✅ PASS | Short sections, descriptive headings, RAG-chunkable content |
| **V. RAG-Ready Architecture** | ✅ PASS | Qdrant vector search, Neon metadata, context-aware LLM responses |
| **VI. Personalization & Accessibility** | ✅ PASS | Onboarding profile, personalize button, Urdu translation |
| **VII. Hardware Awareness** | ✅ PASS | Three tiers defined (workstation, Jetson, physical robots), simulation alternatives |
| **VIII. Reusable Intelligence** | ✅ PASS | Agent-based workflows for content generation |
| **IX. Documentation Standards** | ✅ PASS | Markdown, Docusaurus compatible, Mermaid diagrams |
| **X. Modular Course Structure** | ✅ PASS | Four-module structure + capstone strictly followed |

**Constitution Compliance**: ALL GATES PASSED ✅

No violations. No complexity tracking justification needed.

## Project Structure

### Documentation (this feature)

```text
specs/master/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── openapi.yaml
│   └── graphql-schema.graphql
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web Application Structure
physical-ai-book/          # Docusaurus frontend
├── docs/
│   ├── module1/           # ROS 2 Robotic Nervous System
│   │   ├── chapter1-ros2-introduction.md
│   │   ├── chapter2-ros2-communication.md
│   │   ├── chapter3-python-agents-ros2.md
│   │   ├── chapter4-urdf-humanoid.md
│   │   └── chapter5-robot-nervous-system.md
│   ├── module2/           # RAG System with BetterAuth
│   │   ├── chapter1-betterauth-setup.md
│   │   ├── chapter2-user-personalization.md
│   │   └── chapter3-urdu-chatbot.md
│   ├── module3/           # Digital Twin Simulation (future)
│   ├── module4/           # AI Robot Brain (future)
│   └── capstone/          # Autonomous Humanoid (future)
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   └── ChapterChatbot.tsx
│   │   ├── chapter/
│   │   │   ├── PersonalizeButton.tsx
│   │   │   └── UrduTranslateButton.tsx
│   │   └── onboarding/
│   │       └── OnboardingFlow.tsx
│   ├── pages/
│   │   ├── signup.tsx
│   │   ├── login.tsx
│   │   └── dashboard.tsx
│   └── lib/
│       ├── auth.ts
│       ├── api.ts
│       └── db.ts
├── sidebars.ts
├── docusaurus.config.ts
└── package.json

backend/                   # FastAPI RAG Chatbot
├── src/
│   ├── main.py
│   ├── api/
│   │   ├── chat.py
│   │   ├── translate.py
│   │   └── personalize.py
│   ├── services/
│   │   ├── qdrant_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   └── rag_service.py
│   ├── models/
│   │   ├── user.py
│   │   ├── chat.py
│   │   └── translation.py
│   └── db/
│       ├── postgres.py
│       └── session.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── requirements.txt
└── Dockerfile

docs/                      # Additional documentation
├── api/                   # API documentation
└── guides/                # User guides
```

**Structure Decision**: Web application with separate frontend (Docusaurus/React) and backend (FastAPI) repositories co-located in same monorepo. This enables:
- Shared types/interfaces via TypeScript
- Unified deployment pipeline
- Clear separation of concerns
- Independent scaling of frontend/backend

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations. All constitution principles satisfied.*

