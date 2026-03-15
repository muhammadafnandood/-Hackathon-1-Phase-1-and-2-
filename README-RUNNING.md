# 🚀 How to Run the Hackathon Project

## ✅ Quick Start (Already Running!)

Your project is **currently running**! Here's what's active:

### Backend Server
- **Status**: ✅ Running
- **URL**: `http://localhost:8000`
- **Health**: Healthy
- **PID**: 9960

### Frontend
- **Main Page**: `index.html` (opened in browser)
- **Custom Chat**: `custom-chat.html`
- **Text Selection Demo**: `text-selection-chat.html`

---

## 🎯 Features to Demo

### 1. 💬 Floating Chat Button
**Location**: Bottom-right corner of `index.html`

**How to use**:
1. Look for the purple chat button 💬
2. Click it to open the chat
3. Ask a question like: "Explain ROS 2 architecture"

**What happens**:
- Chat window opens
- AI responds with answer
- **Diagram appears automatically** for architecture questions! 🏗️
- Source citations shown below
- "Translate to Urdu" button available

---

### 2. 📝 Text Selection Popup
**Location**: Any text on the page

**How to use**:
1. Select any text (minimum 10 characters)
2. A purple popup appears: "💬 Ask AI about this"
3. Click the popup
4. Chat opens and automatically asks about selected text

**What happens**:
- Chat widget opens
- Selected text is sent as question
- AI explains the selected concept

---

### 3. 📊 User Level Selector
**Location**: Inside chat window (header)

**Options**:
- 🌱 **Beginner** - Simple language, analogies
- 📚 **Student** - Educational explanation
- ⚙️ **Engineer** - Technical details
- 🔬 **Researcher** - In-depth analysis

**How to use**:
1. Open chat
2. Select your level from dropdown
3. Ask a question
4. AI adapts explanation to your level!

---

### 4. 🌐 Urdu Translation
**Location**: Below every AI answer

**How to use**:
1. Get an answer in English
2. Click "🌐 Translate to Urdu" button
3. Urdu translation appears below
4. Toggle between English/Urdu

---

### 5. 🏗️ Automatic Diagrams
**Trigger keywords**:
- "ROS 2 architecture"
- "RAG pipeline"
- "VLA model"
- "perception pipeline"
- "control loop"

**How to use**:
1. Ask: "Explain ROS 2 architecture"
2. AI answer appears
3. **Diagram renders automatically** below!
4. Use Zoom In/Out buttons

---

### 6. 📚 Source Citations
**Location**: Below AI answer

**Shows**:
- Source: Chapter 5
- Confidence: 82%

**How to use**:
- Click chapter link to open `/docs/chapter5`

---

## 🛠️ Manual Start (If Needed)

### Start Backend Server
```bash
cd D:\Hackathon 1\rag-chatbot\backend
..\..\venv\Scripts\python.exe main.py
```

### Open Frontend
Double-click any of these files:
- `index.html` - Main textbook page
- `custom-chat.html` - Custom chat interface
- `text-selection-chat.html` - Text selection demo

---

## 🧪 Test Scenarios for Judges

### Scenario 1: Architecture Question with Diagram
1. Open chat (click 💬 button)
2. Select level: "Student"
3. Ask: "Explain ROS 2 publisher subscriber architecture"
4. **Watch**: Diagram appears! 🏗️
5. **Watch**: Source citations shown
6. Click "Translate to Urdu"

### Scenario 2: Text Selection
1. Go to main page
2. Select text: "ROS 2 is a robotics middleware..."
3. Click popup: "💬 Ask AI about this"
4. **Watch**: Chat opens with auto-question

### Scenario 3: Personalized Learning
1. Open chat
2. Change level to "Beginner"
3. Ask: "What is RAG?"
4. Note: Simple explanation
5. Change level to "Researcher"
6. Ask same question
7. Note: Technical, detailed answer

### Scenario 4: Multi-language Support
1. Ask any question
2. Click "Translate to Urdu"
3. Toggle between English/Urdu
4. Show Urdu text (RTL formatting)

---

## 🎨 Visual Features

### Color Scheme
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Urdu**: Green gradient (#10b981 → #059669)
- **Diagrams**: Blue accents (#2563eb)

### Animations
- Chat button hover: Scale up + shadow
- Popup hover: Lift effect
- Diagram zoom: Smooth scaling

---

## 📁 File Structure

```
D:\Hackathon 1\
├── index.html                    # Main page (OPEN THIS)
├── custom-chat.html              # Standalone chat
├── text-selection-chat.html      # Text selection demo
│
├── rag-chatbot/
│   ├── chat-widget.js            # Floating chat (865 lines)
│   └── backend/
│       ├── main.py               # FastAPI server (RUNNING)
│       ├── diagram_generator.py  # Mermaid diagrams
│       └── urdu_translator.py    # Urdu translation
│
└── history/prompts/master/       # PHR documentation
    ├── 004-source-citation...
    ├── 005-urdu-translation...
    ├── 006-personalized-level...
    └── 007-diagram-generation...
```

---

## 🔧 Troubleshooting

### Chat button not showing?
- Refresh page (F5)
- Check browser console (F12)
- Verify backend running: `http://localhost:8000/health`

### Text selection popup not appearing?
- Select at least 10 characters
- Make sure mouseup event fires
- Check browser console for errors

### Diagrams not rendering?
- Check internet connection (Mermaid CDN)
- Wait 1-2 seconds for CDN to load
- Try different query: "ROS 2 architecture"

### Urdu translation not working?
- Backend must be running
- Check `/api/translate/urdu` endpoint
- Verify OpenAI API key in `.env`

---

## 🎯 Success Criteria

✅ Floating chat button clickable  
✅ Text selection popup appears  
✅ Level selector changes AI responses  
✅ Diagrams render for architecture questions  
✅ Urdu translation works  
✅ Source citations shown  
✅ All features work together  

---

## 🏆 Hackathon Features Summary

| Feature | Status | Files |
|---------|--------|-------|
| 💬 Floating Chat | ✅ Working | `chat-widget.js` |
| 📝 Text Selection | ✅ Working | `index.html` |
| 📊 User Levels | ✅ Working | All chat files |
| 🌐 Urdu Translation | ✅ Working | All chat files |
| 🏗️ Diagrams | ✅ Working | All chat files |
| 📚 Citations | ✅ Working | All chat files |

**Total**: 6 major features implemented! 🎉

---

## 📞 Quick Commands

### Check Backend Status
```bash
curl http://localhost:8000/health
```

### Stop Backend
```bash
taskkill /F /T /PID 9960
```

### Restart Backend
```bash
cd D:\Hackathon 1\rag-chatbot\backend
..\..\venv\Scripts\python.exe main.py
```

---

**Good luck with your hackathon! 🚀**
