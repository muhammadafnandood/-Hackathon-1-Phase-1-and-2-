# 🤖 AI Tutor for Robotics - Physical AI Textbook

[![Hackathon](https://img.shields.io/badge/Hackathon-Winner-blue)](https://github.com/muhammadafnandood/-Hackathon-1-Phase-1-and-2-)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)](https://fastapi.tiangolo.com)

> **Not just a textbook - An AI-powered learning platform for robotics education!**

An interactive AI textbook that transforms how students learn Physical AI & Humanoid Robotics. Features include AI chat assistance, personalized learning levels, automatic diagram generation, Urdu translation, and source citations.

![AI Tutor Demo](docs/demo-banner.png)

---

## ✨ Features

### 🎯 Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📖 **Interactive Textbook** | 3-column layout with chapters, content, and AI chat | ✅ Complete |
| 💬 **AI Chat Assistant** | Real-time Q&A about textbook content | ✅ Complete |
| 🎓 **Personalized Learning** | 4 levels: Beginner, Student, Engineer, Researcher | ✅ Complete |
| 🏗️ **Automatic Diagrams** | Mermaid.js visualizations for concepts | ✅ Complete |
| 🌐 **Urdu Translation** | Native language support for Urdu speakers | ✅ Complete |
| 📚 **Source Citations** | Chapter references with clickable links | ✅ Complete |
| 📝 **Text Selection Q&A** | Select text → Get AI explanation | ✅ Complete |

### 🎨 User Experience

```
User Opens Platform
        ↓
Selects Expertise Level
        ↓
Reads Interactive Content
        ↓
Asks AI Questions
        ↓
Gets Personalized Answers
        ↓
Sees Source Citations
        ↓
Views Auto-Generated Diagrams
        ↓
Translates to Native Language
        ↓
✅ Learning Complete!
```

---

## 🚀 Quick Start

### Option 1: Frontend Only (No Backend Required)

Most features work **without backend** - perfect for demos!

```bash
# Open main demo page
start "interactive-textbook.html"

# Or open all pages
start "interactive-textbook.html"
start "personalized-learning.html"
start "automatic-diagrams.html"
start "source-citations.html"
```

### Option 2: Full Stack (With Backend)

#### Prerequisites
- Python 3.8+
- Node.js 16+ (optional)
- Qdrant Cloud Account (optional)

#### Installation

```bash
# Clone repository
git clone https://github.com/muhammadafnandood/-Hackathon-1-Phase-1-and-2-.git
cd "-Hackathon-1-Phase-1-and-2-"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
cd rag-chatbot
pip install -r requirements.txt

# Start backend server
cd backend
python main.py
```

#### Access Application

```bash
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Frontend: Open HTML files in browser
```

---

## 📁 Project Structure

```
Hackathon-1/
├── 📖 Interactive Pages/
│   ├── interactive-textbook.html      # ⭐ Main demo page
│   ├── personalized-learning.html     # Level-based learning
│   ├── automatic-diagrams.html        # Mermaid diagrams
│   └── source-citations.html          # Chapter citations
│
├── 💬 Chat Pages/
│   ├── index.html                     # Homepage with chat
│   ├── custom-chat.html               # Standalone chat
│   └── text-selection-chat.html       # Text selection Q&A
│
├── 🔐 Auth Pages/
│   ├── login.html                     # Login UI
│   └── signup.html                    # Signup UI
│
├── 🤖 Backend/
│   └── rag-chatbot/
│       ├── backend/
│       │   ├── main.py                # FastAPI server
│       │   ├── rag_pipeline.py        # RAG logic
│       │   ├── urdu_translator.py     # Translation
│       │   └── diagram_generator.py   # Diagrams
│       ├── chat-widget.js             # Chat widget
│       └── requirements.txt           # Dependencies
│
├── 📚 Documentation/
│   ├── README.md                      # This file
│   ├── HACKATHON_FEATURES.md          # Feature list
│   └── docs/                          # Additional docs
│
└── 🎨 Assets/
    └── docs/
        └── demo-banner.png            # Demo banner
```

---

## 🎯 Demo Flow (5 Minutes)

### Minute 1: First Impression
1. Open `interactive-textbook.html`
2. Show 3-column layout
3. Explain: "This is an AI tutor, not just a textbook"

### Minute 2: AI Interaction
4. Click Chapter 2 (Physical AI)
5. Select text → Click "Ask AI"
6. Show AI explanation

### Minute 3: Personalization
7. Open `personalized-learning.html`
8. Select "Beginner" → Ask "What is SLAM?"
9. Change to "Researcher" → Show technical answer

### Minute 4: Visualizations
10. Open `automatic-diagrams.html`
11. Click "ROS 2 Architecture"
12. Show diagram generates
13. Demo Zoom In/Out

### Minute 5: Citations & Translation
14. Open `source-citations.html`
15. Show sources below answer
16. Click chapter link
17. Click "Translate to Urdu"

---

## 🏆 Competitive Advantages

| Feature | This Project | Traditional |
|---------|--------------|-------------|
| AI Chat Assistance | ✅ | ❌ |
| Personalized Levels | ✅ | ❌ |
| Urdu Translation | ✅ | ❌ |
| Auto Diagrams | ✅ | ❌ |
| Source Citations | ✅ | ❌ |
| Text Selection Q&A | ✅ | ❌ |

---

## 🛠️ Technology Stack

### Frontend
- **HTML5/CSS3** - Modern UI
- **JavaScript (ES6+)** - Interactivity
- **Mermaid.js** - Diagram generation

### Backend
- **FastAPI** - REST API
- **Python 3.8+** - Core logic
- **OpenAI GPT** - AI responses
- **Qdrant** - Vector database
- **RAG Pipeline** - Retrieval-Augmented Generation

### Features
- **Urdu Translation** - Custom translator
- **JWT Auth** - Secure authentication
- **Diagram Generator** - Mermaid.js integration

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Features Implemented | 7/7 ✅ |
| Pages Created | 10+ |
| Lines of Code | 5,000+ |
| Diagram Templates | 6 |
| Learning Levels | 4 |
| Languages Supported | 2 (EN + UR) |
| Chapters | 8 |

---

## 🎓 Use Cases

### For Students
- Ask questions in real-time
- Get explanations at your level
- Read in native language
- See visual diagrams

### For Educators
- Track student progress
- Cite sources transparently
- Adapt to different levels
- Reduce repetitive questions

### For Institutions
- Scalable AI tutoring
- Multi-language support
- Analytics ready
- Easy deployment

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in `rag-chatbot/backend/`:

```env
# OpenAI API
OPENAI_API_KEY=your-api-key-here

# Qdrant Vector DB
QDRANT_URL=https://your-qdrant-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key

# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

---

## 🧪 Testing

### Frontend Testing (No Backend)

```bash
# All these work without backend:
- interactive-textbook.html ✅
- personalized-learning.html ✅
- automatic-diagrams.html ✅
- source-citations.html ✅
```

### Backend Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ROS 2?", "top_k": 5}'

# Test translation endpoint
curl -X POST http://localhost:8000/api/translate/urdu \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello world", "language": "urdu"}'
```

---

## 📝 API Endpoints

### Chat
```http
POST /chat
Content-Type: application/json

{
  "message": "What is SLAM?",
  "level": "Beginner",
  "top_k": 5
}
```

### Translation
```http
POST /api/translate/urdu
Content-Type: application/json

{
  "content": "ROS 2 is a middleware...",
  "language": "urdu"
}
```

### Health Check
```http
GET /health
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
- Project: AI Tutor for Robotics

---

## 🏆 Acknowledgments

- Hackathon Phase 1 & 2
- Physical AI & Humanoid Robotics Course
- OpenAI for GPT API
- Qdrant for Vector Database
- Mermaid.js for Diagrams

---

## 📞 Support

For questions and support:
- Open an issue on GitHub
- Email: [your-email@example.com]

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Built with ❤️ for the future of robotics education**

[Back to Top](#-ai-tutor-for-robotics---physical-ai-textbook)

</div>
