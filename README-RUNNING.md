# 🚀 How to Run the Physical AI Textbook

## Quick Start (Recommended)

### Windows - Double Click Method:
1. **Double-click** `start.bat` file
2. Server starts automatically
3. Interactive textbook opens in your browser at: **http://localhost:3000/interactive-textbook.html**

---

## Alternative Methods

### Method 1: Using npm (Cross-platform)

```bash
# Install dependencies (only needed once)
npm install

# Start server and open textbook
npm start
```

This will:
- Start Python HTTP server on port 3000
- Automatically open http://localhost:3000/interactive-textbook.html in your default browser

### Method 2: Manual Python Command

```bash
# Navigate to project folder
cd "D:\Hackathon 1"

# Start server
python -m http.server 3000

# Open browser and go to:
http://localhost:3000/interactive-textbook.html
```

### Method 3: Using npm dev command

```bash
npm run dev
```

---

## 📖 What Opens?

When you run any of the above commands, you'll get:

**Main Page:** http://localhost:3000/interactive-textbook.html

This page includes:
- ✅ **Complete Textbook** - All chapters on the left sidebar
- ✅ **Reading Area** - Main content in the center
- ✅ **AI Chatbot** - Right sidebar with AI assistant
- ✅ **User Login** - Top-right profile button
- ✅ **Level Selector** - Choose Beginner/Student/Engineer/Researcher

---

## 🎯 Features Available

### In the Interactive Textbook:

1. **Chapter Navigation** (Left Sidebar)
   - Module 1: ROS 2 Basics
   - Module 2: Simulation
   - Module 3: AI Brain (Isaac)
   - Module 4: VLA Robotics
   - Module 5: RAG System

2. **AI Chatbot** (Right Sidebar)
   - Ask questions about any topic
   - Get answers based on your level
   - See robot pictures in every response
   - Urdu translation available

3. **User Profile** (Top Right)
   - Login/Signup
   - Set your experience level
   - Personalize learning

4. **Level Selector** (In Chat Sidebar)
   - 🌱 Beginner
   - 📚 Student
   - ⚙️ Engineer
   - 🔬 Researcher

---

## 🔧 Troubleshooting

### Server Won't Start?

**Check if Python is installed:**
```bash
python --version
```

Should show: `Python 3.x.x`

If not installed, download from: https://python.org

### Port 3000 Already in Use?

**Stop other servers or use different port:**
```bash
# Edit start.bat and change 3000 to 3001
python -m http.server 3001

# Then open: http://localhost:3001/interactive-textbook.html
```

### Browser Doesn't Open Automatically?

**Manual open:**
1. Start server: `python -m http.server 3000`
2. Open browser
3. Go to: http://localhost:3000/interactive-textbook.html

### Chatbot Not Working?

**Start the backend server:**
```bash
cd backend
python main.py
```

Backend runs on: http://localhost:8000

---

## 📁 Project Structure

```
Hackathon-1/
├── interactive-textbook.html    ← MAIN PAGE (opens automatically)
├── index.html                   ← Redirects to interactive-textbook.html
├── start.bat                    ← Windows startup script
├── package.json                 ← npm configuration
├── backend/
│   └── main.py                  ← FastAPI backend (for chatbot)
└── README-RUNNING.md            ← This file
```

---

## 🎨 What You'll See

### Homepage Layout:

```
┌─────────────────────────────────────────────────────┐
│ 👤 User Profile          [Level Selector]           │
├──────────┬──────────────────────────┬───────────────┤
│          │                          │               │
│ Chapters │   Reading Content        │  AI Chatbot   │
│          │                          │               │
│ • ROS 2  │   Chapter Title          │  💬 Ask AI    │
│ • URDF   │                          │               │
│ • SLAM   │   Chapter content...     │  [Messages]   │
│ • etc.   │                          │               │
│          │   [Code examples]        │  [Input] [➤]  │
│          │                          │               │
└──────────┴──────────────────────────┴───────────────┘
```

---

## ✅ Quick Checklist

Before running:
- [ ] Python 3.x installed
- [ ] Port 3000 is free
- [ ] Backend running (for chatbot features)

After running:
- [ ] Server started on port 3000
- [ ] Browser opened automatically
- [ ] Page shows: http://localhost:3000/interactive-textbook.html
- [ ] Textbook content is visible
- [ ] Chatbot sidebar is on the right

---

## 🆘 Need Help?

### Common Issues:

**1. "Address already in use"**
- Close other servers or use different port
- Run: `netstat -ano | findstr :3000` to find what's using port 3000

**2. "Python not found"**
- Install Python from https://python.org
- Add Python to PATH during installation

**3. "Page not found"**
- Make sure server is running
- Check URL: http://localhost:3000/interactive-textbook.html
- Not: http://localhost:3000/index.html

---

## 🎯 Default Page Configuration

**Main Entry Point:**
```
http://localhost:3000/interactive-textbook.html
```

**Why this page?**
- ✅ Complete textbook with all chapters
- ✅ Built-in AI chatbot (right sidebar)
- ✅ User authentication
- ✅ Level selector
- ✅ All features in one place

**Other Pages (Optional):**
- `index.html` - Redirects to interactive-textbook.html
- `login.html` - Standalone login page
- `personalized-learning.html` - Personalization demo

---

## 🚀 Quick Commands Reference

| Command | What it does |
|---------|--------------|
| `start.bat` | Starts server + opens textbook (Windows) |
| `npm start` | Starts server + opens textbook |
| `npm run dev` | Same as npm start |
| `npm run open` | Opens textbook (server must be running) |
| `python -m http.server 3000` | Starts server only |

---

<div align="center">

**Ready to Start! 🎉**

Just double-click `start.bat` or run `npm start`

Main Page: **http://localhost:3000/interactive-textbook.html**

</div>
