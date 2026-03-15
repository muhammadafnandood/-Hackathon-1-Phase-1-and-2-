# 🏆 Hackathon Features - RAG Chatbot

## ✅ Implemented Features

### 1. 💬 Floating Chat Button
- **Location**: Bottom-right corner of every page
- **Design**: Beautiful gradient button with smooth animations
- **Functionality**: Opens chat window on click
- **Auto-load**: Automatically loaded via `docusaurus.config.js`

### 2. 📝 Text Selection Q&A (NEW!)
- **How it works**: 
  1. User selects any text on the page (min 10 characters)
  2. A popup appears above the selection: "💬 Ask AI about this"
  3. Clicking opens chat with pre-filled question
- **Smart detection**: Only triggers outside chat widget
- **Auto-hide**: Popup disappears after 5 seconds if not used

### 3. 📚 Chapter Citations (NEW!)
- **Display**: Shows source chapters at bottom of every AI answer
- **Format**: `Source: Chapter 1 – What is RAG?`
- **Sources Panel**: Shows all referenced chapters with relevance scores
- **Example**:
  ```
  📚 Source:
  📖 Chapter1 – What is RAG?
  📖 Chapter3 – Humanoid Robot Locomotion
  ```

### 4. 🎨 Custom "Ask AI" Buttons
- **Simple integration**: Just add `onclick="openChat()"`
- **Example**:
  ```html
  <button onclick="openChat()">Ask AI</button>
  ```
- **Multiple styles**: Small, regular, large, outline, colored variants

### 5. 🔌 API Integration
- **Endpoint**: `POST http://localhost:8000/chat`
- **Request format**:
  ```javascript
  fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question: userQuestion,
      top_k: 5,
      include_sources: true
    })
  })
  ```

## 📁 Files Modified/Created

### Modified:
1. **`website/static/js/chat-widget.js`**
   - Added `window.openChat()` global function
   - Added text selection detection and popup
   - Added chapter citation display in messages
   - Updated API call to use `question` parameter
   - Added new CSS styles for popup and citations

2. **`website/docusaurus.config.js`**
   - Added script reference to load chat widget

### Created:
3. **`website/static/chatbot-demo.html`**
   - Demo page showcasing all features
   - Multiple button style examples
   - Feature documentation
   - Backend status checker

## 🚀 How to Test

### 1. Start Backend
```bash
cd rag-chatbot/backend
python main.py
# or
uvicorn main:app --reload
```

### 2. Start Docusaurus
```bash
cd physical-ai-book/website
npm start
```

### 3. Test Features

#### Floating Chat
- Look for 💬 button in bottom-right corner
- Click to open chat window
- Ask a question

#### Text Selection Q&A
- Go to any page with text content
- Select a paragraph (10+ characters)
- Wait for popup to appear
- Click "Ask AI about this"

#### Chapter Citations
- Ask any question in chat
- Look for "📚 Source:" section below answer
- Check sources panel for details

#### Custom Buttons
- Visit `/chatbot-demo.html`
- Try different button styles
- All use `onclick="openChat()"`

## 🎯 Backend Status Check

Test API health:
```bash
curl http://127.0.0.1:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "vector_store_connected": true,
  "collection_name": "local_vector_store",
  "vector_count": 60
}
```

## 🎨 Customization Options

### Change Theme Color
Edit `chat-widget.js`:
```javascript
const CONFIG = {
  THEME_COLOR: '#2563eb', // Your color here
  // ...
};
```

### Change Position
```javascript
const CONFIG = {
  POSITION: 'bottom-left', // or 'bottom-right'
  // ...
};
```

### Custom API URL
```javascript
// Before widget loads:
window.CHATBOT_API_URL = 'https://your-api.com';
```

## 📊 Feature Comparison

| Feature | Status | Description |
|---------|--------|-------------|
| Floating Chat | ✅ | Bottom-right chat button |
| Text Selection Q&A | ✅ | Select text → Ask AI popup |
| Chapter Citations | ✅ | Show sources in answers |
| Custom Buttons | ✅ | `onclick="openChat()"` |
| API Integration | ✅ | POST /chat endpoint |
| Sources Panel | ✅ | Relevance scores display |

## 🎁 Bonus Points

All hackathon requirements completed:
- ✅ Text selection Q&A
- ✅ Chapter citation display
- ✅ Floating chatbot with 💬 icon
- ✅ Backend integration at `http://127.0.0.1:8000/health`

## 📝 Notes

- Text selection requires minimum 10 characters
- Popup auto-hides after 5 seconds
- Citations show unique chapters only (no duplicates)
- All features work on mobile with responsive design
