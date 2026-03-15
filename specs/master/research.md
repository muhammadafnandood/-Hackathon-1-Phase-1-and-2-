# Phase 0: Research & Technical Decisions

**Date**: 2026-03-11 | **Status**: Complete

## Research Tasks Completed

### 1. BetterAuth Integration Pattern

**Decision**: Use BetterAuth with PostgreSQL adapter for authentication

**Rationale**:
- Framework-agnostic (works with Express, Next.js, Docusaurus)
- Built-in session management
- TypeScript support with full type safety
- Active development with 2800+ code snippets available
- Simple PostgreSQL integration via `pg` library

**Alternatives Considered**:
- **NextAuth.js**: Rejected because we're using Docusaurus, not Next.js
- **Auth0**: Rejected due to cost and vendor lock-in
- **Clerk**: Rejected due to limited customization
- **Passport.js**: Rejected due to complexity and manual session management

**Implementation Pattern**:
```typescript
import { Pool } from "pg";
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  baseURL: "http://localhost:3000",
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  emailAndPassword: {
    enabled: true,
  },
});
```

**Best Practices**:
- Store DATABASE_URL in environment variables
- Use HTTPS in production
- Enable rate limiting on auth endpoints
- Implement proper session expiration

---

### 2. RAG Architecture with Qdrant

**Decision**: Use Qdrant Cloud for vector database with LangChain orchestration

**Rationale**:
- Qdrant offers superior performance for semantic search
- Built-in filtering by metadata (chapter, user, etc.)
- Cloud hosting eliminates infrastructure management
- LangChain provides clean abstractions for RAG pipelines
- Supports hybrid search (dense + sparse vectors)

**Alternatives Considered**:
- **Pinecone**: Rejected due to pricing and limited filtering
- **Weaviate**: Rejected due to complexity and resource requirements
- **Chroma**: Rejected due to scalability concerns
- **pgvector**: Rejected due to slower search performance at scale

**Architecture**:
```
Textbook Content → Chunking (500-1000 words) → Embeddings (text-embedding-3-large)
                                               ↓
                                         Qdrant Cloud
                                               ↓
User Query → Embedding → Vector Search → Top-K Results → LLM Context → Answer
```

**Chunking Strategy**:
- Chunk size: 500-1000 words (optimized for educational content)
- Overlap: 100 words (preserves context across chunks)
- Metadata: chapter_id, module_id, section_title, heading_hierarchy
- Index: HNSW with cosine similarity

**Best Practices**:
- Cache frequently accessed embeddings
- Use metadata filtering to scope searches by chapter
- Implement query rewriting for better retrieval
- Add source citations to all responses

---

### 3. OpenAI API for Embeddings & LLM

**Decision**: Use OpenAI text-embedding-3-large and GPT-4-turbo

**Rationale**:
- Best-in-class embedding quality for semantic search
- GPT-4-turbo offers excellent reasoning for educational content
- Consistent API with reliable uptime
- Cost-effective for expected usage (~10k users)

**Alternatives Considered**:
- **Anthropic Claude**: Considered but GPT-4 has better embedding integration
- **Cohere**: Rejected due to smaller context window
- **Open-source (Llama 2, Mistral)**: Rejected due to infrastructure complexity
- **Azure OpenAI**: Considered for enterprise, but direct OpenAI API sufficient

**Cost Optimization**:
- Cache all AI-generated content (translations, personalizations)
- Use streaming for chatbot responses
- Implement rate limiting per user
- Batch embedding generation during off-peak hours

**Expected Costs** (10k users, year 1):
- Embeddings: ~$500/month (100k chunks, one-time + updates)
- LLM (chatbot): ~$2000/month (1M queries @ $0.01/query)
- Translation: ~$300/month (cached, regenerations only)

---

### 4. Docusaurus for Documentation Platform

**Decision**: Use Docusaurus v3 with React 18 and TypeScript

**Rationale**:
- Purpose-built for documentation sites
- Built-in search, versioning, i18n support
- React-based component system for custom features
- GitHub Pages deployment integration
- Strong ecosystem and community support

**Alternatives Considered**:
- **GitBook**: Rejected due to limited customization
- **MkDocs**: Rejected due to Python-based (team knows React)
- **VuePress**: Rejected due to smaller ecosystem
- **Custom React**: Rejected due to reinventing documentation features

**Custom Components Required**:
- `ChapterChatbot.tsx` - RAG chatbot UI
- `PersonalizeButton.tsx` - AI content adaptation
- `UrduTranslateButton.tsx` - Translation widget
- `OnboardingFlow.tsx` - User profile setup

**Integration Pattern**:
```typescript
// Custom React components in Docusaurus
// src/components/chapter/ChapterLayout.tsx
export function ChapterLayout({ children, chapterId }) {
  return (
    <Layout>
      <PersonalizeButton chapterId={chapterId} />
      <UrduTranslateButton chapterId={chapterId} />
      {children}
      <ChapterChatbot chapterId={chapterId} />
    </Layout>
  );
}
```

---

### 5. FastAPI for RAG Backend

**Decision**: Use FastAPI (Python 3.11) for chatbot API

**Rationale**:
- Native Python support for AI/ML libraries
- Automatic OpenAPI documentation
- Async support for concurrent requests
- Easy integration with LangChain, Qdrant, OpenAI
- Type safety with Pydantic models

**Alternatives Considered**:
- **Express.js**: Rejected due to Python AI ecosystem
- **Flask**: Rejected due to lack of async support
- **Django**: Rejected due to overhead (we need lightweight API)
- **Hono**: Considered but Python ecosystem priority

**API Structure**:
```python
# backend/src/main.py
from fastapi import FastAPI
from api import chat, translate, personalize

app = FastAPI(title="Physical AI Textbook API")

app.include_router(chat.router, prefix="/api/chat")
app.include_router(translate.router, prefix="/api/translate")
app.include_router(personalize.router, prefix="/api/chapters")
```

**Best Practices**:
- Use dependency injection for database sessions
- Implement request validation with Pydantic
- Add CORS middleware for frontend access
- Use background tasks for embedding generation

---

### 6. Neon PostgreSQL for Metadata

**Decision**: Use Neon (serverless PostgreSQL) for metadata storage

**Rationale**:
- Serverless architecture (pay-per-use)
- Built-in connection pooling
- Automatic scaling
- Free tier sufficient for MVP
- Branching support for development

**Alternatives Considered**:
- **Supabase**: Considered but Neon is simpler for our needs
- **PlanetScale**: Rejected (MySQL, we need PostgreSQL for BetterAuth)
- **AWS RDS**: Rejected due to over-provisioning
- **Self-hosted**: Rejected due to operational overhead

**Schema**:
```sql
-- User Profiles
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  programming_level VARCHAR(20),
  ai_knowledge VARCHAR(20),
  hardware_availability JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Chat History
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY,
  user_id UUID,
  chapter_id VARCHAR(100),
  role VARCHAR(10),
  content TEXT,
  sources JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Translation Cache
CREATE TABLE translation_cache (
  id UUID PRIMARY KEY,
  chapter_id VARCHAR(100),
  language VARCHAR(20),
  content TEXT,
  cached_at TIMESTAMP DEFAULT NOW()
);
```

---

### 7. Personalization Engine Architecture

**Decision**: Use LLM-based content adaptation with profile context

**Rationale**:
- Flexible adaptation based on any user profile attribute
- No manual content tagging required
- Can generate infinite variations for different learners
- Improves with better LLM models over time

**Architecture**:
```
User Profile + Chapter Content → Prompt Template → LLM → Personalized Content
         ↓
  programming_level: "beginner"
  ai_knowledge: "none"
  hardware: { simulationOnly: true }
         ↓
  "Explain this chapter for a beginner with no AI knowledge..."
```

**Prompt Template**:
```
You are an educational AI assistant.

User Profile:
- Programming: {programmingLevel}
- AI Knowledge: {aiKnowledge}
- Hardware: {hardwareAvailability}

Chapter Content:
{chapterContent}

Task: Generate a {mode} explanation that:
- For beginners: Use simple language, analogies, step-by-step
- For advanced: Technical depth, optimization tips, trade-offs

Personalized Explanation:
```

**Caching Strategy**:
- Cache personalized content per (user_id, chapter_id, mode)
- Invalidate cache when chapter content changes
- Regenerate on profile updates (optional)

---

### 8. Urdu Translation Pipeline

**Decision**: Use LLM-based translation with technical term preservation

**Rationale**:
- High-quality translation for educational content
- Can preserve code blocks and technical terms
- More flexible than rule-based translation
- Improves with better models over time

**Translation Guidelines**:
- Keep code blocks in English (never translate)
- Keep technical terms in English with Urdu explanation
- Use simple, clear Urdu for students
- Preserve formatting (headings, lists)
- Write in Nastaliq style using Unicode

**Prompt Template**:
```
You are a professional translator for technical educational content.

Guidelines:
1. Translate accurately while maintaining meaning
2. Keep technical terms in English with Urdu brackets
3. Use simple, clear Urdu for students
4. Preserve code blocks, commands, syntax (DO NOT translate)
5. Maintain formatting (headings, lists, bold/italic)

Original Content:
{content}

Urdu Translation:
```

**Caching**:
- Cache translations per chapter_id
- Invalidate when source content changes
- Store in PostgreSQL translation_cache table

**Font Requirements**:
- Use 'Noto Nastaliq Urdu' Google Font
- Fallback: 'Jameel Noori Nastaleeq'
- Ensure proper RTL layout with `dir="rtl"`

---

### 9. Deployment Architecture

**Decision**: Multi-service deployment with GitHub Pages + Docker

**Architecture**:
```
┌─────────────────────┐
│   GitHub Pages      │  ← Frontend (Docusaurus)
│   (Static Site)     │
└──────────┬──────────┘
           │ API calls
           ▼
┌─────────────────────┐
│   Docker Container  │  ← Backend (FastAPI)
│   - FastAPI         │
│   - Qdrant client   │
│   - OpenAI SDK      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   External Services │
│   - Qdrant Cloud    │
│   - Neon PostgreSQL │
│   - OpenAI API      │
└─────────────────────┘
```

**Frontend Deployment**:
- GitHub Pages (free, automatic CI/CD)
- Custom domain support
- Automatic HTTPS
- CDN for global distribution

**Backend Deployment**:
- Docker container on Railway/Render/Fly.io
- Auto-scaling based on demand
- Environment variables for secrets
- Health check endpoints

**CI/CD Pipeline**:
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install && npm run build
      - uses: peaceiris/actions-gh-pages@v3
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker build && docker push
      - deploy to Railway/Render
```

---

### 10. Security & Rate Limiting

**Decision**: Implement multi-layer security with BetterAuth + API rate limiting

**Authentication Layer**:
- BetterAuth handles session management
- JWT tokens for API authentication
- Secure cookie storage
- CSRF protection

**Rate Limiting**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/chat")
@limiter.limit("10/minute")  # 10 requests per minute per user
async def chat(request: Request):
    ...
```

**Input Validation**:
- Pydantic models for request validation
- Sanitize user input
- Prevent prompt injection in LLM calls
- Max token limits for chatbot

**API Security**:
- HTTPS only (enforced)
- CORS configuration for frontend domain
- API key rotation for external services
- Audit logging for all API calls

---

## Technical Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| OpenAI API downtime | High | Low | Implement retry logic, cache responses, fallback to smaller models |
| Qdrant search quality | High | Medium | Fine-tune chunking, add metadata filtering, implement query rewriting |
| Urdu translation quality | Medium | Medium | Human review process, iterative improvement, user feedback |
| Cost overruns | Medium | Medium | Monitor usage, implement quotas, optimize caching |
| Performance at scale | High | Low | Load testing, horizontal scaling, CDN for static assets |

---

## Research Summary

All technical decisions have been validated with:
- ✅ Library documentation reviewed (BetterAuth, Qdrant, Docusaurus)
- ✅ Alternative solutions evaluated
- ✅ Best practices identified
- ✅ Architecture patterns documented
- ✅ Security considerations addressed
- ✅ Cost estimates calculated

**Ready for Phase 1**: Data modeling, API contracts, and quickstart guide.
