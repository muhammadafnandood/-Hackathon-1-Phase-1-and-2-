# Quickstart Guide: RAG Chatbot

**Feature**: 001-rag-chatbot  
**Date**: 2026-03-14  
**Purpose**: Get the RAG chatbot running in under 30 minutes

---

## Prerequisites

Before starting, ensure you have:

- [ ] Python 3.11 installed
- [ ] Node.js 18+ (for Docusaurus widget)
- [ ] Git installed
- [ ] Qdrant Cloud account (free tier)
- [ ] Neon PostgreSQL account (free tier)
- [ ] OpenAI API key with access to Agents SDK

---

## Step 1: Clone and Setup Repository

```bash
# Navigate to project root
cd "D:\Hackathon 1"

# Ensure you're on the feature branch
git checkout 001-rag-chatbot
```

---

## Step 2: Create Backend Directory Structure

```bash
# Create backend directory
mkdir -p backend
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/Mac:
# source venv/bin/activate
```

---

## Step 3: Install Python Dependencies

Create `requirements.txt`:

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
qdrant-client==1.7.0
openai-agents==0.0.1
openai==1.10.0
sentence-transformers==2.3.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0
httpx==0.26.0
pytest==7.4.4
pytest-asyncio==0.23.3
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Step 4: Create Environment Configuration

Create `.env` file in `backend/` directory:

```bash
# Qdrant Cloud Configuration
QDRANT_URL=https://your-cluster.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=rag-chatbot-chunks

# Neon PostgreSQL Configuration
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4-turbo-preview

# Application Settings
APP_ENV=development
API_KEY=your-secret-ingestion-api-key
LOG_LEVEL=INFO

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**Security Note**: Add `.env` to `.gitignore` - never commit secrets!

---

## Step 5: Create Backend Application Structure

Create the following directory structure:

```bash
mkdir -p src/{api,models,services,core}
mkdir -p scripts
mkdir -p tests/{unit,integration}
```

### Create Main Application File (`src/main.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chat, search, ingest, health
from .core.config import settings

app = FastAPI(
    title="RAG Chatbot API",
    description="API for Physical AI & Humanoid Robotics textbook chatbot",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingestion"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Create Configuration Module (`src/core/config.py`)

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Qdrant
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection: str = "rag-chatbot-chunks"
    
    # Database
    database_url: str
    
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"
    
    # App
    app_env: str = "development"
    api_key: str
    log_level: str = "INFO"
    
    # Embedding
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Step 6: Create Ingestion Script

Create `scripts/ingest.py`:

```python
#!/usr/bin/env python3
"""
Ingest textbook chapters into Qdrant vector database.

Usage:
    python scripts/ingest.py --full           # Full re-ingestion
    python scripts/ingest.py --incremental    # Only changed files
    python scripts/ingest.py --chapter docs/module1/ros2-basics.md
"""

import argparse
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Configuration
DOCS_DIR = Path("../docs")  # Adjust path as needed
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 750  # tokens
CHUNK_OVERLAP = 50  # tokens

def load_model():
    """Load sentence transformer model."""
    return SentenceTransformer(EMBEDDING_MODEL)

def chunk_text(text: str, chapter: str, section: str) -> list:
    """Split text into chunks with overlap."""
    # Simple chunking - replace with sophisticated tokenizer in production
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), CHUNK_SIZE - CHUNK_OVERLAP):
        chunk_words = words[i:i + CHUNK_SIZE]
        chunk_text = " ".join(chunk_words)
        
        if len(chunk_words) >= 100:  # Minimum chunk size
            chunks.append({
                "chapter": chapter,
                "section": section,
                "content": chunk_text,
                "tokens": len(chunk_words)
            })
    
    return chunks

def parse_markdown(file_path: Path) -> dict:
    """Parse markdown file into chapters and sections."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter
    # Simple parsing - use frontmatter library in production
    title = file_path.stem.replace('-', ' ').title()
    chapter_id = file_path.stem
    
    return {
        "id": chapter_id,
        "title": title,
        "file_path": str(file_path),
        "content": content
    }

def ingest_full():
    """Ingest all markdown files."""
    print("Starting full ingestion...")
    
    model = load_model()
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
    # Create collection if not exists
    collection = os.getenv("QDRANT_COLLECTION")
    try:
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print(f"Created collection: {collection}")
    except Exception as e:
        if "already exists" not in str(e):
            raise
    
    chapters_processed = 0
    chunks_created = 0
    
    # Find all markdown files
    md_files = list(DOCS_DIR.rglob("*.md"))
    
    for md_file in md_files:
        print(f"Processing: {md_file}")
        
        chapter_data = parse_markdown(md_file)
        chunks = chunk_text(
            chapter_data["content"],
            chapter_data["id"],
            "Introduction"
        )
        
        points = []
        for idx, chunk in enumerate(chunks):
            embedding = model.encode(chunk["content"])
            
            point = PointStruct(
                id=chunks_created + idx,
                vector=embedding.tolist(),
                payload={
                    "chapter_id": chunk["chapter"],
                    "section": chunk["section"],
                    "content": chunk["content"],
                    "tokens": chunk["tokens"]
                }
            )
            points.append(point)
        
        if points:
            client.upsert(collection_name=collection, points=points)
            chunks_created += len(points)
        
        chapters_processed += 1
    
    print(f"\n✅ Ingestion complete!")
    print(f"   Chapters processed: {chapters_processed}")
    print(f"   Chunks created: {chunks_created}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest textbook content")
    parser.add_argument("--full", action="store_true", help="Full re-ingestion")
    parser.add_argument("--incremental", action="store_true", help="Incremental update")
    parser.add_argument("--chapter", type=str, help="Ingest specific chapter")
    
    args = parser.parse_args()
    
    if args.full:
        ingest_full()
    else:
        print("Use --full, --incremental, or --chapter <path>")
        ingest_full()  # Default to full for now
```

---

## Step 7: Run the Backend

```bash
# From backend/ directory
# Make sure virtual environment is activated
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Verify**: Open http://localhost:8000/docs to see the Swagger UI.

---

## Step 8: Ingest Textbook Content

```bash
# From backend/ directory
python scripts/ingest.py --full
```

**Expected Output**:
```
Starting full ingestion...
Created collection: rag-chatbot-chunks
Processing: ../docs/module1/ros2-basics.md
...
✅ Ingestion complete!
   Chapters processed: 25
   Chunks created: 342
```

---

## Step 9: Test the Chat API

```bash
# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is ROS 2?"
  }'
```

**Expected Response**:
```json
{
  "answer": "ROS 2 is a middleware for robotics systems...",
  "citations": [
    {
      "chapter_id": "module1-ros2-basics",
      "chapter_title": "Module 1: ROS 2 Basics",
      "section": "1.1 What is ROS 2?",
      "content": "ROS 2 is a middleware...",
      "relevance_score": 0.87
    }
  ]
}
```

---

## Step 10: Create Frontend Widget

Navigate to your Docusaurus site directory:

```bash
# If Docusaurus is in a subdirectory
cd ../textbook-site  # Adjust path as needed

# Install chat widget dependencies
npm install axios react-markdown
```

Create `src/components/ChatWidget.js`:

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './ChatWidget.css';

const API_BASE_URL = process.env.RAG_CHATBOT_API_URL || 'http://localhost:8000';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  const sendMessage = async (query, selectedText = null) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat`, {
        query,
        session_id: sessionId,
        selected_text: selectedText
      });

      const { answer, citations, session_id } = response.data;
      
      if (!sessionId) {
        setSessionId(session_id);
      }

      setMessages(prev => [
        ...prev,
        { role: 'user', content: query },
        { role: 'assistant', content: answer, citations }
      ]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [
        ...prev,
        { role: 'user', content: query },
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      sendMessage(input.trim());
      setInput('');
    }
  };

  return (
    <>
      {/* Floating Button */}
      <button className="chat-widget-button" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-widget-window">
          <div className="chat-widget-header">
            <h3>Textbook Assistant</h3>
          </div>
          
          <div className="chat-widget-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                {msg.role === 'assistant' ? (
                  <>
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                    {msg.citations && msg.citations.length > 0 && (
                      <div className="citations">
                        <h4>Sources:</h4>
                        {msg.citations.map((cite, i) => (
                          <div key={i} className="citation">
                            <strong>{cite.chapter_title}</strong> - {cite.section}
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                ) : (
                  msg.content
                )}
              </div>
            ))}
            {loading && <div className="message assistant">Thinking...</div>}
          </div>

          <form className="chat-widget-input" onSubmit={handleSubmit}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about the textbook..."
              disabled={loading}
            />
            <button type="submit" disabled={loading || !input.trim()}>
              Send
            </button>
          </form>
        </div>
      )}
    </>
  );
}
```

Create `src/components/ChatWidget.css`:

```css
.chat-widget-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #007bff;
  color: white;
  border: none;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 1000;
}

.chat-widget-window {
  position: fixed;
  bottom: 90px;
  right: 20px;
  width: 380px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

.chat-widget-header {
  background: #007bff;
  color: white;
  padding: 16px;
  border-radius: 12px 12px 0 0;
}

.chat-widget-header h3 {
  margin: 0;
  font-size: 16px;
}

.chat-widget-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.message {
  margin-bottom: 12px;
  padding: 12px;
  border-radius: 8px;
  max-width: 85%;
}

.message.user {
  background: #007bff;
  color: white;
  margin-left: auto;
}

.message.assistant {
  background: #f0f0f0;
  color: #333;
}

.citations {
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px solid #ddd;
  font-size: 12px;
}

.citation {
  margin: 4px 0;
  padding: 4px;
  background: #e8e8e8;
  border-radius: 4px;
}

.chat-widget-input {
  display: flex;
  padding: 12px;
  border-top: 1px solid #eee;
}

.chat-widget-input input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.chat-widget-input button {
  margin-left: 8px;
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.chat-widget-input button:disabled {
  background: #ccc;
}
```

---

## Step 11: Integrate Widget into Docusaurus

Edit `docusaurus.config.js`:

```javascript
// Add to clientModules
clientModules: [
  require.resolve('./src/components/ChatWidget.js'),
],

// Or add to a layout component
```

Or create a custom layout in `src/theme/Layout.js`:

```jsx
import React from 'react';
import Layout from '@theme/Layout';
import ChatWidget from '../components/ChatWidget';

export default function CustomLayout(props) {
  return (
    <Layout {...props}>
      {props.children}
      <ChatWidget />
    </Layout>
  );
}
```

---

## Step 12: Test the Full System

1. **Backend running**: http://localhost:8000/docs
2. **Docusaurus running**: http://localhost:3000
3. **Open textbook**: Click the chat widget button
4. **Ask a question**: "What is ROS 2?"
5. **Verify response**: Answer with citations appears

---

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11.x

# Check virtual environment
which python  # Should point to venv/bin/python or venv\Scripts\python

# Reinstall dependencies
pip install -r requirements.txt
```

### Qdrant connection error
- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Check Qdrant Cloud dashboard for cluster status
- Ensure firewall allows outbound connections

### No results from chat
- Verify ingestion completed: check Qdrant dashboard for points
- Test search endpoint: `GET /api/search?q=ROS%202`
- Check embedding model is downloading correctly

### Widget not appearing
- Check browser console for errors
- Verify CSS is loading
- Ensure component is imported in Docusaurus layout

---

## Next Steps

After completing quickstart:

1. **Customize widget styling** to match textbook theme
2. **Add text selection** feature for context questions
3. **Configure rate limiting** for production
4. **Set up monitoring** with health check endpoint
5. **Deploy to Railway** for production access

---

## Commands Reference

```bash
# Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload

# Ingestion
python scripts/ingest.py --full
python scripts/ingest.py --chapter docs/module1/ros2-basics.md

# Testing
pytest tests/
pytest tests/integration/test_chat.py

# Frontend (Docusaurus)
npm start
npm run build
```
