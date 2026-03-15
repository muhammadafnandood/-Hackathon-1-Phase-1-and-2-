# Railway Deployment Configuration for Physical AI RAG API

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new)

## Deployment Steps

### Option 1: Deploy from GitHub

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Connect Railway to GitHub**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure environment variables**
   In Railway dashboard -> Variables, add:
   ```
   OPENAI_API_KEY=your-openai-api-key
   DATABASE_URL=postgresql://user:pass@host:port/db
   QDRANT_URL=your-qdrant-cloud-url
   QDRANT_API_KEY=your-qdrant-api-key
   EMBEDDING_MODEL=text-embedding-ada-002
   PORT=8000
   ```

4. **Deploy**
   Railway will automatically detect and deploy

### Option 2: Deploy with Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   cd backend
   railway init
   ```

4. **Add environment variables**
   ```bash
   railway variables set OPENAI_API_KEY=your-key
   railway variables set DATABASE_URL=your-db-url
   railway variables set QDRANT_URL=your-qdrant-url
   railway variables set QDRANT_API_KEY=your-key
   ```

5. **Deploy**
   ```bash
   railway up
   ```

## Required Services

### 1. PostgreSQL Database
Use one of these:
- **Neon** (recommended): https://neon.tech
- **Supabase**: https://supabase.com
- **Railway PostgreSQL**: Add PostgreSQL plugin in Railway

### 2. Qdrant Vector Database
- **Qdrant Cloud**: https://cloud.qdrant.io
- Free tier available for testing

### 3. OpenAI API
- Get API key from: https://platform.openai.com

## Database Schema

Run these SQL commands to create required tables:

```sql
-- Chapters table
CREATE TABLE chapters (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chunks table for vector search
CREATE TABLE chunks (
    id SERIAL PRIMARY KEY,
    chapter_id INTEGER REFERENCES chapters(id),
    content TEXT NOT NULL,
    heading VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat sessions
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255),
    session_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(id),
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE NOT NULL,
    programming_experience VARCHAR(50) DEFAULT 'beginner',
    ai_experience VARCHAR(50) DEFAULT 'beginner',
    robotics_experience VARCHAR(50) DEFAULT 'beginner',
    hardware_availability VARCHAR(100),
    gpu_capability VARCHAR(100),
    preferred_language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User progress
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    chapter_id INTEGER REFERENCES chapters(id),
    status VARCHAR(50) DEFAULT 'not_started',
    progress_percent INTEGER DEFAULT 0,
    time_spent_seconds INTEGER DEFAULT 0,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, chapter_id)
);

-- Analytics events
CREATE TABLE analytics_events (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_chunks_chapter_id ON chunks(chapter_id);
CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_analytics_user_id ON analytics_events(user_id);
```

## Testing Deployment

After deployment, test your API:

```bash
# Get your Railway URL
RAILWAY_URL=https://your-project.railway.app

# Test health endpoint
curl $RAILWAY_URL/health

# Test chat endpoint
curl -X POST "$RAILWAY_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ROS 2?"}'
```

## Troubleshooting

### Build fails
- Check `requirements.txt` is in the correct location
- Ensure Python version is 3.9+

### Runtime errors
- Verify all environment variables are set
- Check database connection string
- Ensure Qdrant collection exists

### Timeout issues
- Railway has 15min timeout for Pro plan
- Optimize LLM calls for faster responses

## Monitoring

- View logs: `railway logs`
- View metrics in Railway dashboard
- Set up alerts for errors

## Cost Estimation

- **Free tier**: $5/month usage credit
- **Pro plan**: $20/month + usage
- Estimated cost for small project: $5-10/month

## Production Checklist

- [ ] Set strong DATABASE_URL
- [ ] Configure Qdrant Cloud
- [ ] Set OPENAI_API_KEY
- [ ] Enable HTTPS (automatic on Railway)
- [ ] Set up monitoring
- [ ] Configure CORS for production domain
- [ ] Test all endpoints
- [ ] Set up database backups
