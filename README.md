# 🤖 Physical AI & Humanoid Robotics Textbook

[![Hackathon](https://img.shields.io/badge/Hackathon-Phase%201%20%26%202-blue)](https://github.com/muhammadafnandood/-Hackathon-1-Phase-1-and-2-)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)](https://fastapi.tiangolo.com)
[![Docusaurus](https://img.shields.io/badge/Docusaurus-3.9-blue)](https://docusaurus.io)
[![Deploy](https://img.shields.io/badge/Deploy-Vercel-black)](https://vercel.com)

> **AI-powered interactive textbook for Physical AI & Humanoid Robotics with Urdu translation support!**

An advanced learning platform that transforms how students learn robotics. Features AI chat assistance, personalized learning levels, automatic Urdu translation, RAG-powered chatbot, and source citations.

---

## 🏆 Features & Points Breakdown

| Feature | Points | Status | Description |
|---------|--------|--------|-------------|
| **RAG Chatbot** | 5 pts | ✅ | OpenAI + FastAPI + Neon + Qdrant powered AI chat |
| **Better-Auth Login** | 5 pts | ✅ | User authentication with background survey |
| **Personalize Chapter** | 5 pts | ✅ | AI rewrites content based on user level |
| **Urdu Translation** | 5 pts | ✅ | Full chapter translation with caching |
| **Urdu-Aware Chatbot** | Bonus ✅ | | Chatbot responds in Urdu when page is in Urdu mode |
| **TOTAL** | **20 + Bonus** | ✅ | All features implemented |

---

## ✨ Key Features

### 🧠 RAG Chatbot (5 points)
- Real-time Q&A about textbook content
- Retrieves relevant chapters using vector search
- Cites sources with chapter references
- Generates diagrams automatically
- Context-aware responses

### 🔐 Better-Auth Login System (5 points)
- Secure user authentication
- User profile with experience level
- Background survey (software/hardware)
- Learning goals tracking
- Session management

### 🎯 Personalize Chapter Button (5 points)
- AI-powered content adaptation
- Three levels: Beginner, Intermediate, Advanced
- Adds analogies for beginners
- Skips basics for advanced users
- Preserves code blocks unchanged

### 🌐 Urdu Translation (5 points)
- Full chapter translation to Urdu
- Neon Postgres caching (no re-translation)
- Noto Nastaliq Urdu font
- RTL layout support
- Code blocks remain in English
- Technical terms preserved

### 🤖 Urdu-Aware Chatbot (Bonus)
- Detects page language mode
- Responds in Urdu when page is translated
- Seamless language switching
- Context-aware responses

---

## 🛠️ Tech Stack

### Frontend
```
- Docusaurus 3.9 (React-based static site generator)
- TypeScript
- React 19
- Mermaid.js (diagrams)
- Google Fonts (Noto Nastaliq Urdu)
```

### Backend
```
- FastAPI 0.104+ (Python 3.8+)
- OpenAI/Qwen API (AI features)
- Neon Postgres (user data + cache)
- Qdrant (vector search for RAG)
- Better-Auth (authentication)
```

### Infrastructure
```
- Vercel (frontend hosting)
- Railway/Render (backend hosting)
- Neon (serverless Postgres)
- Qdrant Cloud (vector DB)
```

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.8+
- Node.js 20+
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/muhammadafnandood/-Hackathon-1-Phase-1-and-2-.git
cd "-Hackathon-1-Phase-1-and-2-"
```

### Step 2: Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API keys:
# - QWEN_API_KEY or OPENAI_API_KEY
# - DATABASE_URL (Neon Postgres)
# - QDRANT_URL (optional, for RAG)
# - QDRANT_API_KEY (optional)

# Start backend server
python main.py
```

Backend runs on: **http://localhost:8000**

### Step 3: Setup Frontend

```bash
# Open new terminal
# Navigate to Docusaurus site
cd physical-ai-book

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on: **http://localhost:3000**

### Step 4: Test Features

1. **Open textbook**: http://localhost:3000
2. **Login/Signup**: Create account or login
3. **Open any chapter**: Navigate to a chapter
4. **Test Personalize**: Click "Personalize for Me"
5. **Test Urdu**: Click "اردو میں پڑھیں"
6. **Test Chatbot**: Click "💬 Ask AI" button

---

## 📁 Project Structure

```
Hackathon-1/
├── 📖 physical-ai-book/       # Docusaurus textbook
│   ├── docs/                  # Chapter content
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── PersonalizeButton.tsx
│   │   │   ├── UrduTranslateButton.tsx
│   │   │   └── ChapterToolbar.tsx
│   │   ├── theme/             # Swizzled components
│   │   │   └── DocItem/
│   │   │       └── Layout/
│   │   │           └── index.tsx
│   │   └── css/
│   │       └── custom.css     # Urdu styles + skeletons
│   └── static/
│       └── chatbot.js         # Chat widget
│
├── 🤖 backend/
│   ├── main.py                # FastAPI app
│   ├── routes/
│   │   ├── personalize.py     # Personalization endpoint
│   │   └── translate.py       # Urdu translation endpoint
│   ├── migrations/
│   │   └── 002_urdu_cache.sql # Database migrations
│   └── requirements.txt       # Python dependencies
│
├── 📚 docs/                   # Additional documentation
├── .agents/                   # AI agent skill files
├── DEPLOYMENT.md              # Deployment guide
└── README.md                  # This file
```

---

## 📸 Screenshots

### Homepage
```
┌─────────────────────────────────────────┐
│  Physical AI & Humanoid Robotics       │
│  Master the art of building intelligent │
│  humanoid robots                        │
│                                         │
│  [Get Started] [View on GitHub]        │
└─────────────────────────────────────────┘
```

### Chapter with Toolbar
```
┌─────────────────────────────────────────┐
│ Chapter 1: Introduction to ROS 2        │
├─────────────────────────────────────────┤
│ [Personalize for Me] [اردو میں پڑھیں]  │
├─────────────────────────────────────────┤
│                                         │
│ ROS 2 is a middleware framework...      │
│                                         │
│ ```python                               │
│ import rclpy                            │
│ from rclpy.node import Node             │
│ ```                                     │
│                                         │
└─────────────────────────────────────────┘
```

### Urdu Translation Mode
```
┌─────────────────────────────────────────┐
│ باب 1: ROS 2 کا تعارف                   │
├─────────────────────────────────────────┤
│ [Personalize for Me] [انگریزی میں واپس]│
├─────────────────────────────────────────┤
│                                         │
│ ROS 2 (روس 2) روبوٹکس کے لیے ایک       │
│ مڈل ویئر فریم ورک ہے۔                  │
│                                         │
│ ```python                               │
│ import rclpy                            │
│ from rclpy.node import Node             │
│ ```                                     │
│                                         │
└─────────────────────────────────────────┘
```

### AI Chatbot
```
┌─────────────────────────────────────────┐
│ 💬 Ask AI                               │
├─────────────────────────────────────────┤
│ 🤖 Physical AI Assistant                │
│                                         │
│ You: What is ROS 2?                     │
│                                         │
│ Bot: ROS 2 is a middleware framework... │
│      Sources: Chapter 1, Chapter 3      │
│                                         │
│ [Type your question...] [Send]          │
└─────────────────────────────────────────┘
```

---

## 📖 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide
- **[AGENTS.md](AGENTS.md)** - AI agent skills documentation
- **[PERSONALIZE-FEATURE-COMPLETE.md](PERSONALIZE-FEATURE-COMPLETE.md)** - Personalization feature docs

---

## 🧪 Testing Each Feature

### 1. RAG Chatbot Test
```bash
# Open chat widget
- Click "💬 Ask AI"
- Ask: "What is ROS 2?"
- Expected: Response with textbook content + sources
```

### 2. Login Test
```bash
# Register new user
- Go to /login
- Click "Sign Up"
- Fill form
- Expected: User created, logged in
```

### 3. Personalize Test
```bash
# Test personalization
- Login as "beginner" level
- Open chapter
- Click "Personalize for Me"
- Expected: Content rewritten for beginners
```

### 4. Urdu Translation Test
```bash
# Test translation
- Open chapter
- Click "اردو میں پڑھیں"
- Expected: Urdu translation with RTL layout
- Expected: Code blocks remain English
```

### 5. Urdu Chatbot Test
```bash
# Test Urdu-aware chat
- Click "اردو میں پڑھیں" first
- Open chat
- Ask question
- Expected: Chatbot responds in Urdu
```

---

## 🎯 API Endpoints

### Authentication
```http
POST /auth/register
POST /auth/login
```

### AI Features
```http
POST /api/chat              # RAG chatbot
POST /api/personalize-chapter  # Personalization
POST /api/translate-urdu    # Urdu translation
GET  /api/translate-urdu/health  # Health check
```

### Health Checks
```http
GET /health
GET /api/personalize-chapter/health
GET /api/translate-urdu/health
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Muhammad Afnan**
- GitHub: [@muhammadafnandood](https://github.com/muhammadafnandood)
- Project: Physical AI & Humanoid Robotics Textbook

---

## 🏆 Acknowledgments

- Hackathon Phase 1 & 2
- Physical AI & Humanoid Robotics Course
- OpenAI for GPT API
- Qwen for translation API
- Docusaurus team
- Neon Database
- Qdrant Vector DB

---

## 📞 Support

For questions and support:
- Open an issue on GitHub
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for troubleshooting

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Built with ❤️ for the future of robotics education**

[Back to Top](#-physical-ai--humanoid-robotics-textbook)

</div>
