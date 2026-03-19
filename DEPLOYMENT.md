# Deployment Guide - Physical AI & Humanoid Robotics Textbook

Complete deployment checklist for production deployment.

---

## 📋 Environment Variables

Create a `.env` file in the `backend/` directory with these variables:

```bash
# ============================================
# REQUIRED: API Keys
# ============================================

# Qwen API (or OpenAI)
QWEN_API_KEY=your-qwen-api-key-here
# OR if using OpenAI:
OPENAI_API_KEY=your-openai-api-key-here

# API Endpoints
QWEN_API_URL=https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
# OR for OpenAI:
# QWEN_API_URL=https://api.openai.com/v1/chat/completions

# Model to use
QWEN_MODEL=qwen-plus
# OR for OpenAI:
# QWEN_MODEL=gpt-4-turbo

# ============================================
# REQUIRED: Database (Neon Postgres)
# ============================================

# Neon Postgres connection string
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require

# ============================================
# OPTIONAL: Qdrant Vector DB (for RAG)
# ============================================

# Qdrant Cloud URL
QDRANT_URL=https://your-cluster.qdrant.io

# Qdrant API Key
QDRANT_API_KEY=your-qdrant-api-key

# ============================================
# OPTIONAL: Better-Auth (for authentication)
# ============================================

# Better-Auth secret key (generate with: openssl rand -hex 32)
BETTER_AUTH_SECRET=your-secret-key-here

# OAuth providers (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# ============================================
# OPTIONAL: Deployment
# ============================================

# Node environment
NODE_ENV=production

# Frontend URL (for CORS)
FRONTEND_URL=https://your-domain.com
```

---

## 🗄️ Neon Database Setup Steps

### Step 1: Create Neon Account

1. Go to [https://neon.tech](https://neon.tech)
2. Sign up with GitHub or email
3. Create a new project named `physical-ai-textbook`

### Step 2: Get Connection String

1. In Neon dashboard, click your project
2. Go to **Connection Details** (right sidebar)
3. Copy the **Postgres connection string**
4. Format: `postgresql://user:password@host.neon.tech/dbname?sslmode=require`

### Step 3: Create Database Tables

Run these SQL migrations in order:

```bash
# Connect to Neon via psql or Neon SQL editor
psql "postgresql://user:password@host.neon.tech/dbname?sslmode=require"
```

**Migration 001: Users Table** (if not already created by better-auth)
```sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    password_hash VARCHAR(255),
    experience_level VARCHAR(50) DEFAULT 'beginner',
    software_background TEXT,
    hardware_background TEXT,
    learning_goal TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

**Migration 002: Urdu Translations Cache**
```sql
-- Run the migration file
\i backend/migrations/002_urdu_cache.sql
```

Or manually:
```sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS urdu_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id VARCHAR(255) UNIQUE NOT NULL,
    urdu_content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_urdu_translations_chapter_id 
ON urdu_translations(chapter_id);

CREATE INDEX IF NOT EXISTS idx_urdu_translations_created_at 
ON urdu_translations(created_at);
```

### Step 4: Verify Database

```sql
-- Check tables exist
\dt

-- Should show:
-- users
-- urdu_translations
```

---

## 🎯 Qdrant Cloud Setup Steps

### Step 1: Create Qdrant Account

1. Go to [https://cloud.qdrant.io](https://cloud.qdrant.io)
2. Sign up with GitHub
3. Create a new cluster (free tier available)

### Step 2: Get Cluster Details

1. In Qdrant dashboard, click your cluster
2. Copy **Cluster URL** (e.g., `https://xxx-xxx.aws.cloud.qdrant.io`)
3. Go to **API Keys** tab
4. Create a new API key with **Read/Write** permissions
5. Copy the API key

### Step 3: Create Collections

```python
from qdrant_client import QdrantClient

# Connect to Qdrant Cloud
client = QdrantClient(
    url="https://your-cluster.qdrant.io",
    api_key="your-api-key"
)

# Create collection for textbook content
client.create_collection(
    collection_name="textbook_content",
    vectors_config={
        "size": 1536,  # OpenAI embeddings
        "distance": "Cosine"
    }
)

# Create index for faster search
client.create_payload_index(
    collection_name="textbook_content",
    field_name="chapter",
    field_schema="keyword"
)
```

### Step 4: Populate Vector DB

```bash
# Run the indexing script
cd backend
python scripts/index_content.py
```

---

## 🚀 GitHub Pages Deployment (Frontend)

### Step 1: Build Docusaurus

```bash
cd physical-ai-book

# Install dependencies
npm install

# Build for production
npm run build
```

### Step 2: Deploy to GitHub Pages

**Option A: Using docusaurus deploy**

```bash
# Update docusaurus.config.ts with your repo
# organizationName: 'your-username'
# projectName: 'physical-ai-textbook'

npm run deploy
```

**Option B: Manual deployment**

```bash
# Install Vercel CLI (recommended)
npm install -g vercel

# Deploy
vercel

# Production deploy
vercel --prod
```

**Option C: GitHub Actions**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: |
          cd physical-ai-book
          npm ci
      
      - name: Build
        run: |
          cd physical-ai-book
          npm run build
      
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./physical-ai-book/build
```

---

## ✅ Testing Checklist After Deployment

### 1. Test RAG Chatbot (5 points)

```bash
# Open chat widget
- Click "💬 Ask AI" button
- Ask: "What is ROS 2?"
- Verify: Response includes textbook content
- Verify: Sources are listed below response
- Verify: Diagram is generated if applicable
```

**Expected:** Chatbot responds with relevant textbook content and citations.

### 2. Test Better-Auth Login (5 points)

```bash
# Test registration
- Go to /login page
- Click "Sign Up"
- Fill form with test credentials
- Verify: User created in Neon database

# Test login
- Login with credentials
- Verify: Redirected to textbook
- Verify: User name shown in navbar
```

**Expected:** Users can register and login successfully.

### 3. Test Personalize Chapter Button (5 points)

```bash
# Test personalization
- Login as user with "beginner" level
- Open any chapter
- Click "Personalize for Me"
- Verify: Content is rewritten for beginner level
- Verify: Analogies and examples added
- Click "Restore Original"
- Verify: Original content restored
```

**Expected:** Content is personalized based on user's experience level.

### 4. Test Urdu Translation Button (5 points)

```bash
# Test translation
- Open any chapter
- Click "اردو میں پڑھیں"
- Verify: Content translates to Urdu
- Verify: RTL direction applied
- Verify: Noto Nastaliq Urdu font loaded
- Verify: Code blocks remain in English
- Click "انگریزی میں واپس جائیں"
- Verify: English content restored
```

**Expected:** Chapter translates to Urdu with proper formatting.

### 5. Test Urdu-Aware Chatbot (Bonus)

```bash
# Test Urdu mode chat
- First click "اردو میں پڑھیں" on a chapter
- Open chat widget while in Urdu mode
- Ask: "ROS 2 کیا ہے؟"
- Verify: Chatbot responds in Urdu
- Switch back to English
- Ask same question in English
- Verify: Chatbot responds in English
```

**Expected:** Chatbot detects Urdu mode and responds accordingly.

### 6. Test Combined Toolbar (Integration)

```bash
# Test button interaction
- Login and open chapter
- Click "Personalize for Me"
- Wait for personalization
- Then click "اردو میں پڑھیں"
- Verify: Urdu translation is of PERSONALIZED content
- Click "Restore Original"
- Verify: Both personalization and translation cleared
```

**Expected:** Buttons work together without conflicts.

---

## 🔧 Backend Deployment Options

### Option 1: Railway (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Option 2: Render

1. Go to [https://render.com](https://render.com)
2. Create new **Web Service**
3. Connect GitHub repo
4. Set build command: `pip install -r backend/requirements.txt`
5. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000`
6. Add environment variables

### Option 3: VPS (DigitalOcean, EC2)

```bash
# SSH to server
ssh user@your-server-ip

# Install Python
sudo apt update
sudo apt install python3-pip python3-venv

# Clone repo
git clone https://github.com/your-org/physical-ai.git
cd physical-ai/backend

# Setup virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with systemd
sudo nano /etc/systemd/system/physical-ai.service
```

Systemd service file:
```ini
[Unit]
Description=Physical AI Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/physical-ai/backend
ExecStart=/home/ubuntu/physical-ai/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable physical-ai
sudo systemctl start physical-ai
sudo systemctl status physical-ai
```

---

## 📊 Monitoring & Debugging

### Check Backend Logs

```bash
# Railway
railway logs

# Render
# Dashboard > Logs tab

# Systemd
sudo journalctl -u physical-ai -f
```

### Check Database

```bash
# Connect to Neon
psql "postgresql://user:password@host.neon.tech/dbname?sslmode=require"

# Check recent translations
SELECT chapter_id, created_at FROM urdu_translations ORDER BY created_at DESC LIMIT 10;

# Check user count
SELECT COUNT(*) FROM users;
```

### Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Translation health
curl http://localhost:8000/api/translate-urdu/health

# Personalization health
curl http://localhost:8000/api/personalize-chapter/health

# Chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ROS 2?", "is_urdu_mode": false}'
```

---

## 🎯 Points Breakdown

| Feature | Points | Status |
|---------|--------|--------|
| RAG Chatbot | 5 | ✅ |
| Better-Auth Login | 5 | ✅ |
| Personalize Chapter | 5 | ✅ |
| Urdu Translation | 5 | ✅ |
| Urdu-Aware Chatbot | Bonus | ✅ |
| **Total** | **20 + Bonus** | |

---

## 🆘 Troubleshooting

### Issue: Translation not working

```bash
# Check API key
echo $QWEN_API_KEY

# Check database connection
psql "your-database-url" -c "SELECT 1"

# Check logs
tail -f backend/logs/app.log
```

### Issue: Chatbot not responding

```bash
# Test backend directly
curl http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# Check CORS settings
# Ensure backend allows frontend domain
```

### Issue: Urdu font not loading

```bash
# Check network tab for Google Fonts request
# Verify custom.css is loaded
# Clear browser cache
```

---

<div align="center">

**Deployment Complete! 🎉**

All features tested and working. Ready for production!

</div>
