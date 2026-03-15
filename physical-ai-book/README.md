# Physical AI & Humanoid Robotics Textbook

A comprehensive AI-native textbook for learning physical AI and humanoid robotics with ROS 2, simulation tools, and AI integration.

## 📚 Project Structure

```
physical-ai-book/
│
├── website/                     # Docusaurus website
│   ├── docs/                    # All textbook content
│   │   ├── module1/             # ROS 2 (✅ Complete)
│   │   ├── module2/             # Digital Twin Simulation
│   │   ├── module3/             # AI Robot Brain
│   │   ├── module4/             # Vision Language Action
│   │   └── capstone/            # Autonomous Humanoid Project
│   ├── src/                     # React components
│   ├── static/                  # Static assets
│   ├── docusaurus.config.js     # Site configuration
│   └── package.json
│
├── backend/
│   ├── rag_api/                 # FastAPI RAG chatbot
│   │   ├── main.py              # API endpoints
│   │   ├── database.py          # PostgreSQL connection
│   │   ├── embeddings.py        # Embedding service
│   │   ├── chat.py              # Chat service
│   │   └── requirements.txt
│   │
│   └── embeddings/              # Embedding generator
│       └── generate.py
│
├── agents/
│   ├── book_writer_agent/       # Content generation
│   │   └── main.py
│   ├── urdu_translator_agent/   # Translation to Urdu
│   │   └── main.py
│   └── chapter_personalizer_agent/  # Personalization
│       └── main.py
│
├── database/
│   └── neon_schema.sql          # PostgreSQL schema with pgvector
│
└── README.md
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd physical-ai-book
```

### 2. Install Backend Dependencies

```bash
cd backend/rag_api
pip install -r requirements.txt
```

### 3. Setup Database

```bash
# Set your Neon PostgreSQL connection string
export DATABASE_URL="postgresql://..."

# Run schema
psql $DATABASE_URL < database/neon_schema.sql
```

### 4. Start RAG API

```bash
cd backend/rag_api
uvicorn main:app --reload
```

### 5. Start Website

```bash
cd website
npm install
npm run start
```

## 📖 Modules

| Module | Topic | Status |
|--------|-------|--------|
| Module 1 | ROS 2 Robotic Nervous System | ✅ Complete (5 chapters) |
| Module 2 | Digital Twin Simulation | 📋 Planned |
| Module 3 | AI Robot Brain | 📋 Planned |
| Module 4 | Vision Language Action | 📋 Planned |
| Capstone | Autonomous Humanoid | 📋 Planned |

### Module 1 Contents

- **Chapter 1**: Introduction to ROS 2
- **Chapter 2**: ROS 2 Communication System
- **Chapter 3**: Python AI Agents with ROS 2
- **Chapter 4**: Robot Description using URDF
- **Chapter 5**: Building the Robot Nervous System

## 🛠️ Tech Stack

**Frontend:**
- Docusaurus v3
- React 18
- Beige Theme CSS

**Backend:**
- FastAPI
- Qdrant (Vector DB)
- Neon PostgreSQL (with pgvector)
- LangChain

**AI/ML:**
- OpenAI GPT-4
- text-embedding-ada-002
- Whisper (Speech-to-Text)

**Robotics:**
- ROS 2 Humble
- Gazebo Sim
- NVIDIA Isaac Sim
- URDF

## 🤖 AI Agents

### Book Writer Agent
Generates textbook content using AI with proper structure:
- Learning objectives
- Concept explanations
- Code examples
- Hands-on labs

### Urdu Translator Agent
Translates content to Urdu while preserving technical terms in English.

### Chapter Personalizer Agent
Adapts content to user's:
- Programming experience
- AI/ML background
- Hardware availability
- Learning preferences

## 📡 RAG Chatbot

The RAG (Retrieval-Augmented Generation) chatbot:

1. **Embeds** user questions
2. **Searches** textbook content using vector similarity
3. **Generates** responses with retrieved context
4. **Cites** sources from specific chapters

### API Endpoints

```bash
# Chat
POST /chat
{
  "message": "What is ROS 2?",
  "top_k": 3
}

# Search
POST /search
{
  "query": "robot navigation",
  "top_k": 5
}

# Add chunk
POST /embeddings/chunks
{
  "chapter_id": "module1/chapter1",
  "content": "ROS 2 is...",
  "heading": "Introduction"
}
```

## 🗄️ Database Schema

The Neon PostgreSQL database includes:

- **users** - User accounts
- **user_profiles** - Personalization data
- **modules** - Course modules
- **chapters** - Chapter content
- **chunks** - Text chunks for RAG
- **embeddings** - Vector embeddings (pgvector)
- **chat_sessions** - Chat history
- **user_progress** - Learning progress
- **translations** - Urdu translations
- **analytics_events** - Usage analytics

## 📝 Development

### Adding New Content

1. Create chapter in `docs/moduleX/`
2. Run embeddings generator:
   ```bash
   cd backend/embeddings
   python generate.py
   ```
3. Test in RAG chatbot
4. Deploy website

### Running Agents

```bash
# Book Writer Agent
cd agents/book_writer_agent
python main.py

# Urdu Translator Agent
cd agents/urdu_translator_agent
python main.py

# Chapter Personalizer Agent
cd agents/chapter_personalizer_agent
python main.py
```

## 🔧 Configuration

### Environment Variables

Create `.env` files in each service directory:

**backend/rag_api/.env:**
```bash
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
```

**agents/.env:**
```bash
OPENAI_API_KEY=sk-...
OUTPUT_DIR=../../../docs
```

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Contact

- **GitHub**: [physical-ai-book/textbook](https://github.com/physical-ai-book/textbook)
- **Discord**: [Coming Soon]
- **Email**: [Coming Soon]

---

**Built with ❤️ for the robotics community**

*Last updated: March 2026*
