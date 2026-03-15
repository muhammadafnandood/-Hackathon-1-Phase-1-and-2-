# Tasks: AI-Native Textbook Platform for Physical AI & Humanoid Robotics

**Input**: Design documents from `specs/master/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/openapi.yaml

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification or if user requests TDD approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `physical-ai-book/` (frontend Docusaurus), `backend/` (FastAPI)
- Paths shown below are absolute based on project structure in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan (physical-ai-book/, backend/, docs/)
- [X] T002 [P] Initialize Docusaurus frontend with TypeScript, React 18, TailwindCSS in physical-ai-book/package.json
- [X] T003 [P] Initialize FastAPI backend with Python 3.11 venv in backend/requirements.txt
- [ ] T004 [P] Configure ESLint, Prettier for frontend in physical-ai-book/.eslintrc.js
- [X] T005 [P] Configure Black, Flake8, MyPy for backend in backend/pyproject.toml
- [ ] T006 [P] Setup Git hooks with Husky for frontend and pre-commit for backend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 [P] Setup Neon PostgreSQL database and configure DATABASE_URL in backend/.env
- [X] T008 [P] Initialize BetterAuth with PostgreSQL adapter in backend/src/auth.py
- [X] T009 [P] Create database migration scripts in backend/src/db/migrations/
- [X] T010 [P] Setup Qdrant Cloud connection in backend/src/services/qdrant_service.py
- [X] T011 [P] Configure OpenAI API client in backend/src/services/llm_service.py
- [ ] T012 [P] Implement JWT authentication middleware in physical-ai-book/src/lib/auth.ts
- [X] T013 [P] Setup API routing structure in backend/src/api/__init__.py
- [X] T014 [P] Configure CORS middleware for frontend access in backend/src/main.py
- [X] T015 [P] Create base error handling and logging infrastructure in backend/src/utils/logger.py
- [X] T016 [P] Setup environment configuration management with pydantic-settings in backend/src/config.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Documentation Platform (Priority: P1) 🎯 MVP

**Goal**: Docusaurus-based textbook with modular structure, sidebar navigation, and search functionality

**Independent Test**: User can open the website, browse modules/chapters, and search content

### Implementation for User Story 1

- [ ] T017 [P] [US1] Create Module 1 chapters in physical-ai-book/docs/module1/ (chapter1-5 .md files)
- [ ] T018 [P] [US1] Create Module 2 chapters in physical-ai-book/docs/module2/ (chapter1-3 .md files)
- [ ] T019 [US1] Configure sidebars.ts with module/chapter structure in physical-ai-book/sidebars.ts
- [ ] T020 [US1] Update docusaurus.config.ts with site metadata and theme in physical-ai-book/docusaurus.config.ts
- [ ] T021 [P] [US1] Create ChapterLayout component in physical-ai-book/src/components/chapter/ChapterLayout.tsx
- [ ] T022 [US1] Implement module navigation sidebar in physical-ai-book/src/components/ModuleSidebar.tsx
- [ ] T023 [US1] Add search functionality with Docusaurus search in physical-ai-book/docusaurus.config.ts
- [ ] T024 [US1] Create homepage with feature overview in physical-ai-book/docs/intro.md
- [ ] T025 [US1] Add learning objectives template to all chapters in physical-ai-book/docs/module*/*.md
- [ ] T026 [US1] Implement responsive styling for chapter content in physical-ai-book/src/css/custom.css

**Checkpoint**: At this point, User Story 1 should be fully functional - users can read chapters and navigate the textbook

---

## Phase 4: User Story 2 - Authentication & User Management (Priority: P1)

**Goal**: BetterAuth integration for signup/login, user profiles with programming/AI/hardware levels, session management

**Independent Test**: User can sign up, login, create profile, and access protected routes

### Implementation for User Story 2

- [ ] T027 [P] [US2] Create users table schema (BetterAuth managed) in backend/src/db/migrations/001_users.sql
- [ ] T028 [P] [US2] Create user_profiles table in backend/src/db/migrations/002_user_profiles.sql
- [ ] T029 [P] [US2] Create user_progress table in backend/src/db/migrations/003_user_progress.sql
- [ ] T030 [US2] Implement UserProfile Pydantic model in backend/src/models/user.py
- [ ] T031 [US2] Implement UserProfileService in backend/src/services/user_service.py
- [ ] T032 [P] [US2] Create signup page in physical-ai-book/src/pages/signup.tsx
- [ ] T033 [P] [US2] Create login page in physical-ai-book/src/pages/login.tsx
- [ ] T034 [P] [US2] Create dashboard page in physical-ai-book/src/pages/dashboard.tsx
- [ ] T035 [US2] Implement onboarding flow component in physical-ai-book/src/components/onboarding/OnboardingFlow.tsx
- [ ] T036 [US2] Create profile API endpoints (GET/PUT /api/users/me) in backend/src/api/users.py
- [ ] T037 [US2] Implement progress tracking API (GET /api/users/me/progress) in backend/src/api/users.py
- [ ] T038 [US2] Add session management to frontend in physical-ai-book/src/lib/auth.ts
- [ ] T039 [US2] Create protected route wrapper in physical-ai-book/src/components/ProtectedRoute.tsx

**Checkpoint**: At this point, User Story 2 should be fully functional - users can authenticate and manage profiles

---

## Phase 5: User Story 3 - RAG Chatbot (Priority: P2)

**Goal**: FastAPI backend for chat API, Qdrant vector database, context retrieval, LLM-powered answers with citations

**Independent Test**: User can ask questions about chapter content and receive AI-generated answers with sources

### Implementation for User Story 3

- [ ] T040 [P] [US3] Create chat_messages table in backend/src/db/migrations/004_chat_messages.sql
- [ ] T041 [US3] Implement ChatMessage Pydantic model in backend/src/models/chat.py
- [ ] T042 [P] [US3] Create Qdrant collection for textbook embeddings in backend/src/services/qdrant_service.py
- [ ] T043 [US3] Implement embedding service with OpenAI in backend/src/services/embedding_service.py
- [ ] T044 [US3] Create textbook chunking script in backend/src/scripts/chunk_textbook.py
- [ ] T045 [US3] Implement embedding generation pipeline in backend/src/scripts/embed_textbook.py
- [ ] T046 [US3] Implement RAG service with LangChain in backend/src/services/rag_service.py
- [ ] T047 [US3] Create chat API endpoint (POST /api/chat) in backend/src/api/chat.py
- [ ] T048 [US3] Implement chat history API (GET /api/chat/history/:chapterId) in backend/src/api/chat.py
- [ ] T049 [P] [US3] Create ChapterChatbot component in physical-ai-book/src/components/chat/ChapterChatbot.tsx
- [ ] T050 [US3] Implement chat message UI with typing indicator in physical-ai-book/src/components/chat/ChatMessage.tsx
- [ ] T051 [US3] Add source citation display in physical-ai-book/src/components/chat/SourceCitation.tsx
- [ ] T052 [US3] Integrate chatbot into ChapterLayout in physical-ai-book/src/components/chapter/ChapterLayout.tsx

**Checkpoint**: At this point, User Story 3 should be fully functional - users can ask questions and get AI answers with sources

---

## Phase 6: User Story 4 - Personalization Engine (Priority: P2)

**Goal**: Onboarding questionnaire, "Personalize This Chapter" button, AI-generated beginner/advanced explanations

**Independent Test**: User can click personalize button and receive chapter explanation adapted to their profile level

### Implementation for User Story 4

- [ ] T053 [P] [US4] Create personalized_content table in backend/src/db/migrations/005_personalized_content.sql
- [ ] T054 [US4] Implement PersonalizedContent Pydantic model in backend/src/models/personalized_content.py
- [ ] T055 [US3] Create personalization prompt templates in backend/src/prompts/personalization.py
- [ ] T056 [US4] Implement personalization API (POST /api/chapters/:id/personalize) in backend/src/api/personalize.py
- [ ] T057 [US4] Implement cached content API (GET /api/chapters/:id/personalized) in backend/src/api/personalize.py
- [ ] T058 [P] [US4] Create PersonalizeButton component in physical-ai-book/src/components/chapter/PersonalizeButton.tsx
- [ ] T059 [US4] Implement mode selector (beginner/auto/advanced) in physical-ai-book/src/components/chapter/PersonalizeButton.tsx
- [ ] T060 [US4] Create personalized content display panel in physical-ai-book/src/components/chapter/PersonalizedPanel.tsx
- [ ] T061 [US4] Add onboarding step 1 (account setup) in physical-ai-book/src/components/onboarding/Step1Account.tsx
- [ ] T062 [US4] Add onboarding step 2 (background questions) in physical-ai-book/src/components/onboarding/Step2Background.tsx
- [ ] T063 [US4] Add onboarding step 3 (hardware availability) in physical-ai-book/src/components/onboarding/Step3Hardware.tsx
- [ ] T064 [US4] Implement profile-based content adaptation logic in backend/src/services/personalization_service.py

**Checkpoint**: At this point, User Story 4 should be fully functional - users can get personalized chapter explanations

---

## Phase 7: User Story 5 - Urdu Translation (Priority: P3)

**Goal**: "Translate to Urdu" button per chapter, AI-powered translation preserving code, RTL layout, caching

**Independent Test**: User can click translate button and view Urdu translation with proper RTL layout

### Implementation for User Story 5

- [ ] T065 [P] [US5] Create translation_cache table in backend/src/db/migrations/006_translation_cache.sql
- [ ] T066 [US5] Implement TranslationCache Pydantic model in backend/src/models/translation.py
- [ ] T067 [US5] Create Urdu translation prompt template in backend/src/prompts/translation.py
- [ ] T068 [US5] Implement translation API (POST /api/translate/urdu) in backend/src/api/translate.py
- [ ] T069 [US5] Implement cached translation API (GET /api/translate/:chapterId/urdu) in backend/src/api/translate.py
- [ ] T070 [US5] Add translation caching logic in backend/src/services/translation_service.py
- [ ] T071 [P] [US5] Create UrduTranslateButton component in physical-ai-book/src/components/chapter/UrduTranslateButton.tsx
- [ ] T072 [US5] Implement Urdu translation panel with RTL layout in physical-ai-book/src/components/chapter/UrduPanel.tsx
- [ ] T073 [US5] Add Noto Nastaliq Urdu font to physical-ai-book/src/css/custom.css
- [ ] T074 [US5] Implement copy-to-clipboard functionality in physical-ai-book/src/components/chapter/UrduPanel.tsx
- [ ] T075 [US5] Add Urdu translation loading state in physical-ai-book/src/components/chapter/UrduTranslateButton.tsx

**Checkpoint**: At this point, User Story 5 should be fully functional - users can translate chapters to Urdu

---

## Phase 8: User Story 6 - Content Structure (Priority: P3)

**Goal**: Learning objectives, architecture diagrams, runnable code examples, hands-on labs, exercises

**Independent Test**: All chapters include complete educational structure with diagrams and exercises

### Implementation for User Story 6

- [ ] T076 [US6] Add learning objectives to all Module 1 chapters in physical-ai-book/docs/module1/chapter*.md
- [ ] T077 [US6] Add learning objectives to all Module 2 chapters in physical-ai-book/docs/module2/chapter*.md
- [ ] T078 [US6] Create Mermaid diagram components in physical-ai-book/src/components/MermaidDiagram.tsx
- [ ] T079 [US6] Add architecture diagrams to all chapters in physical-ai-book/docs/module*/*.md
- [ ] T080 [US6] Verify all code examples are complete and runnable in physical-ai-book/docs/module*/*.md
- [ ] T081 [US6] Add hands-on lab sections to all chapters in physical-ai-book/docs/module*/*.md
- [ ] T082 [US6] Add simulation alternatives to all hardware-dependent labs in physical-ai-book/docs/module*/*.md
- [ ] T083 [US6] Add summary sections to all chapters in physical-ai-book/docs/module*/*.md
- [ ] T084 [US6] Add exercise sections to all chapters in physical-ai-book/docs/module*/*.md

**Checkpoint**: At this point, all chapters should have complete educational structure

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T085 [P] Create API documentation in docs/api/ using OpenAPI spec from specs/master/contracts/openapi.yaml
- [ ] T086 [P] Create user guide in docs/guides/quickstart.md based on specs/master/quickstart.md
- [ ] T087 [P] Setup GitHub Pages deployment workflow in .github/workflows/deploy-frontend.yml
- [ ] T088 [P] Setup Docker deployment for backend in backend/Dockerfile and .github/workflows/deploy-backend.yml
- [ ] T089 [P] Implement rate limiting with slowapi in backend/src/middleware/rate_limiter.py
- [ ] T090 [P] Add security headers and HTTPS enforcement in backend/src/main.py
- [ ] T091 [P] Create unit tests for backend services in backend/tests/unit/
- [ ] T092 [P] Create integration tests for API endpoints in backend/tests/integration/
- [ ] T093 [P] Create E2E tests with Playwright in backend/tests/e2e/
- [ ] T094 [P] Add accessibility testing with axe-core in physical-ai-book/tests/accessibility.test.ts
- [ ] T095 [P] Implement analytics tracking in physical-ai-book/src/analytics.ts
- [ ] T096 [P] Add error boundary components in physical-ai-book/src/components/ErrorBoundary.tsx
- [ ] T097 [P] Create health check endpoint in backend/src/api/health.py
- [ ] T098 [P] Setup monitoring and alerting configuration in backend/monitoring/
- [ ] T099 [P] Run quickstart.md validation and fix any issues
- [ ] T100 [P] Final documentation review and cleanup

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Documentation Platform - Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Authentication - Can start after Foundational (Phase 2) - Independent, but used by all other stories
- **User Story 3 (P2)**: RAG Chatbot - Can start after Foundational (Phase 2) - Depends on US2 for auth
- **User Story 4 (P2)**: Personalization - Can start after Foundational (Phase 2) - Depends on US2 for user profile
- **User Story 5 (P3)**: Urdu Translation - Can start after Foundational (Phase 2) - Independent
- **User Story 6 (P3)**: Content Structure - Can start after US1 - Enhances existing content

### Within Each User Story

- Models before services
- Services before endpoints
- Backend before frontend integration
- Core implementation before integration

### Parallel Opportunities

- **Phase 1 (Setup)**: T002-T006 can all run in parallel (different files, no dependencies)
- **Phase 2 (Foundational)**: T007-T016 can mostly run in parallel (different services/files)
- **Phase 3+ (User Stories)**: Once Phase 2 completes, all user stories can start in parallel
- **Within User Stories**: Model creation tasks marked [P] can run in parallel
- **Frontend/Backend**: Backend API and frontend UI can be developed in parallel once contracts are defined

---

## Parallel Example: User Story 1

```bash
# Launch all chapter creation together:
Task: "Create Module 1 chapters in physical-ai-book/docs/module1/"
Task: "Create Module 2 chapters in physical-ai-book/docs/module2/"

# Launch component creation in parallel:
Task: "Create ChapterLayout component in physical-ai-book/src/components/chapter/ChapterLayout.tsx"
Task: "Implement module navigation sidebar in physical-ai-book/src/components/ModuleSidebar.tsx"
```

---

## Parallel Example: User Story 2

```bash
# Launch all database migrations together:
Task: "Create users table schema in backend/src/db/migrations/001_users.sql"
Task: "Create user_profiles table in backend/src/db/migrations/002_user_profiles.sql"
Task: "Create user_progress table in backend/src/db/migrations/003_user_progress.sql"

# Launch all page creation together:
Task: "Create signup page in physical-ai-book/src/pages/signup.tsx"
Task: "Create login page in physical-ai-book/src/pages/login.tsx"
Task: "Create dashboard page in physical-ai-book/src/pages/dashboard.tsx"
```

---

## Parallel Example: User Story 3 (RAG Chatbot)

```bash
# Launch all model/service creation together:
Task: "Create chat_messages table in backend/src/db/migrations/004_chat_messages.sql"
Task: "Create Qdrant collection in backend/src/services/qdrant_service.py"
Task: "Implement embedding service in backend/src/services/embedding_service.py"

# Launch frontend components in parallel:
Task: "Create ChapterChatbot component in physical-ai-book/src/components/chat/ChapterChatbot.tsx"
Task: "Implement chat message UI in physical-ai-book/src/components/chat/ChatMessage.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T016) - **CRITICAL BLOCKER**
3. Complete Phase 3: User Story 1 (T017-T026) - Textbook readable
4. Complete Phase 4: User Story 2 (T027-T039) - Authentication working
5. **STOP and VALIDATE**: Test MVP with real users
6. Deploy MVP: Docusaurus site with auth

### Incremental Delivery

1. **Week 1-2**: Setup + Foundational → Foundation ready
2. **Week 3-4**: User Story 1 → Textbook live → Deploy/Demo (MVP Part 1!)
3. **Week 5-6**: User Story 2 → Auth + Profiles → Deploy/Demo (MVP Part 2!)
4. **Week 7-8**: User Story 3 → RAG Chatbot → Deploy/Demo
5. **Week 9-10**: User Story 4 → Personalization → Deploy/Demo
6. **Week 11-12**: User Story 5 + 6 → Urdu + Polish → Final Release

### Parallel Team Strategy

With multiple developers after Phase 2:

- **Developer A**: User Story 1 (Documentation Platform)
- **Developer B**: User Story 2 (Authentication)
- **Developer C**: User Story 3 (RAG Chatbot) - starts after US2 auth is ready
- **Developer D**: User Story 4 (Personalization) - starts after US2 profile is ready

Once Foundational phase completes:
- All user stories can be worked on in parallel
- Each story is independently testable
- Merge and deploy stories incrementally

---

## Task Summary

| Phase | Description | Task Count | Story |
|-------|-------------|------------|-------|
| Phase 1 | Setup | 6 | N/A |
| Phase 2 | Foundational | 10 | N/A |
| Phase 3 | User Story 1 | 10 | US1 - Documentation |
| Phase 4 | User Story 2 | 13 | US2 - Authentication |
| Phase 5 | User Story 3 | 16 | US3 - RAG Chatbot |
| Phase 6 | User Story 4 | 12 | US4 - Personalization |
| Phase 7 | User Story 5 | 11 | US5 - Urdu Translation |
| Phase 8 | User Story 6 | 9 | US6 - Content Structure |
| Phase 9 | Polish | 16 | N/A |
| **Total** | | **103 tasks** | |

### MVP Scope (Minimum)

- Phase 1: Setup (6 tasks)
- Phase 2: Foundational (10 tasks)
- Phase 3: User Story 1 (10 tasks) - Textbook readable
- Phase 4: User Story 2 (13 tasks) - Authentication

**MVP Total**: 39 tasks - Deployable textbook with auth

### Full Scope

All 103 tasks - Complete AI-native textbook platform with RAG, personalization, and Urdu translation

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
