# Quickstart Guide: Physical AI Textbook Platform

**Version**: 1.0.0 | **Last Updated**: 2026-03-11

Get up and running with the AI-native textbook platform in under 30 minutes.

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** database (Neon recommended)
- **OpenAI API** key
- **Qdrant Cloud** account (free tier OK)

## Quick Start (30 minutes)

### Step 1: Clone Repository (2 minutes)

```bash
git clone https://github.com/your-org/physical-ai-book.git
cd physical-ai-book
```

### Step 2: Frontend Setup - Docusaurus (8 minutes)

```bash
# Install dependencies
cd physical-ai-book
npm install

# Copy environment template
cp .env.example .env.local

# Edit .env.local with your settings
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Start Development Server**:

```bash
npm run start
```

Visit `http://localhost:3000` - you should see the Docusaurus homepage.

### Step 3: Backend Setup - FastAPI (10 minutes)

```bash
# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your settings
```

**Environment Variables** (`backend/.env`):

```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Qdrant
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=physical-ai-textbook

# BetterAuth
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:8000
```

**Initialize Database**:

```bash
# Run migrations
python src/db/migrate.py
```

**Start Backend Server**:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` - you should see the FastAPI Swagger UI.

### Step 4: Configure BetterAuth (5 minutes)

**Update `physical-ai-book/src/lib/auth.ts`**:

```typescript
import { createAuthClient } from 'better-auth/react';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
});
```

**Update `backend/src/main.py`**:

```python
from better_auth import BetterAuth
from pg import Pool

auth = BetterAuth(
    database=Pool(connection_string=os.getenv("DATABASE_URL")),
    email_and_password=True,
)
```

### Step 5: Test Authentication (5 minutes)

**Create Test User**:

```bash
# Using curl
curl -X POST http://localhost:8000/api/auth/sign-up/email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "name": "Test User"
  }'
```

**Expected Response**:

```json
{
  "user": {
    "id": "uuid-here",
    "email": "test@example.com",
    "name": "Test User"
  },
  "session": {
    "id": "session-uuid",
    "expiresAt": "2026-03-12T00:00:00Z"
  }
}
```

### Step 6: Create User Profile (Optional)

```bash
curl -X PUT http://localhost:8000/api/users/me \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "programmingLevel": "beginner",
    "aiKnowledge": "none",
    "hardwareAvailability": {
      "hasRobot": false,
      "hasROS2": false,
      "hasGPU": false,
      "simulationOnly": true
    }
  }'
```

## Verify Installation

### Frontend Checklist

- [ ] Docusaurus homepage loads at `http://localhost:3000`
- [ ] Sidebar shows Module 1 and Module 2
- [ ] Chapter 1 content displays correctly
- [ ] Navigation between chapters works

### Backend Checklist

- [ ] FastAPI docs available at `http://localhost:8000/docs`
- [ ] Health check returns OK: `GET http://localhost:8000/health`
- [ ] Authentication endpoints respond
- [ ] Database connection successful

### Integration Checklist

- [ ] Frontend can call backend API
- [ ] Authentication flow works (signup → login → session)
- [ ] User profile creation succeeds
- [ ] CORS configured correctly

## Next Steps

### 1. Add Content (Chapter 1)

Your first chapter is already created in `docs/module1/chapter1-ros2-introduction.md`. Customize it:

```markdown
---
sidebar_label: '1. ROS2 Introduction'
---

# Chapter 1: ROS2 Introduction

## Learning Objectives
- Understand what ROS2 is
- Install ROS2 Humble
- Create your first ROS2 node
```

### 2. Configure RAG Pipeline

**Create Qdrant Collection**:

```python
from qdrant_client import QdrantClient

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

client.create_collection(
    collection_name="physical-ai-textbook",
    vectors_config=models.VectorParams(
        size=3072,  # text-embedding-3-large
        distance=models.Distance.COSINE
    )
)
```

**Embed Textbook Content**:

```bash
cd backend
python src/scripts/embed_textbook.py
```

### 3. Test Chatbot

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "chapterId": "chapter-uuid",
    "message": "What is a ROS2 node?"
  }'
```

### 4. Test Personalization

```bash
curl -X POST http://localhost:8000/api/chapters/chapter-uuid/personalize \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "mode": "beginner"
  }'
```

### 5. Test Urdu Translation

```bash
curl -X POST http://localhost:8000/api/translate/urdu \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "content": "ROS2 is a robotics framework...",
    "language": "urdu"
  }'
```

## Troubleshooting

### Frontend Issues

**Problem**: Docusaurus won't start

```bash
# Clear cache
rm -rf .docusaurus
npm run start
```

**Problem**: API calls fail with CORS error

```typescript
// Update docusaurus.config.ts
module.exports = {
  // ...
  headers: {
    'Access-Control-Allow-Origin': '*',
  },
};
```

### Backend Issues

**Problem**: Database connection fails

```bash
# Check connection string
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

**Problem**: OpenAI API errors

```bash
# Verify API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

**Problem**: Qdrant connection timeout

```python
# Test connection
from qdrant_client import QdrantClient
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
print(client.get_collections())
```

## Development Workflow

### Frontend Development

```bash
# Start dev server with hot reload
npm run start

# Run tests
npm run test

# Build for production
npm run build

# Preview production build
npm run serve
```

### Backend Development

```bash
# Activate virtual environment
source venv/bin/activate

# Start dev server with auto-reload
uvicorn src.main:app --reload

# Run tests
pytest

# Run linter
flake8 src/

# Type checking
mypy src/
```

### Database Migrations

```bash
# Create new migration
python src/db/migrate.py create add_user_preferences

# Apply all migrations
python src/db/migrate.py up

# Rollback last migration
python src/db/migrate.py down
```

## Production Deployment

### Frontend (GitHub Pages)

```yaml
# .github/workflows/deploy-frontend.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install && npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

### Backend (Railway/Render)

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# railway.toml
[build]
builder = "DOCKERFILE"

[deploy]
startCommand = "uvicorn src.main:app --host 0.0.0.0 --port 8000"
```

## Resources

- **Docusaurus Docs**: https://docusaurus.io/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **BetterAuth Docs**: https://better-auth.com
- **Qdrant Docs**: https://qdrant.tech/documentation
- **OpenAI API**: https://platform.openai.com/docs

## Getting Help

- **GitHub Issues**: Report bugs and feature requests
- **Discord**: Join our community server
- **Email**: support@physicalai-book.com

---

**Congratulations!** 🎉 You now have a fully functional AI-native textbook platform with authentication, RAG chatbot, personalization, and Urdu translation capabilities.

Next: Read the [Architecture Overview](./architecture.md) to understand the system design.
