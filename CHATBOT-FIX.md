# Chatbot Fix - Complete

## Issues Fixed

### 1. Wrong API Endpoint ✅
**Problem:** Frontend was calling `/chat` but backend expects `/api/chat`

**Fix:** Changed endpoint in `chatbot.js`:
```javascript
// Before
const response = await fetch(`${API_URL}/chat`, {

// After
const response = await fetch(`${API_URL}/api/chat`, {
```

### 2. Wrong Request Body Field ✅
**Problem:** Frontend sent `question` but backend expects `message`

**Fix:** Changed request body in `chatbot.js`:
```javascript
// Before
body: JSON.stringify({ question })

// After
body: JSON.stringify({
  message: question,
  level: 'Beginner',
  is_urdu_mode: isUrduMode
})
```

### 3. Wrong Response Field ✅
**Problem:** Frontend looked for `answer` but backend returns `message`

**Fix:** Changed response handling:
```javascript
// Before
addMessage(data.answer || data.response || 'Got your question!', 'bot');

// After
addMessage(data.message || data.answer || data.response || 'Got your question!', 'bot');
```

### 4. sendMessage Not Receiving Input ✅
**Problem:** Event listener wasn't passing the input value

**Fix:** Updated event listeners:
```javascript
// Before
sendButton.addEventListener('click', sendMessage);

// After
sendButton.addEventListener('click', () => {
  sendMessage(chatInput.value);
});
```

### 5. Missing CSS Styles ✅
**Problem:** Chat widget had no styles

**Fix:** Added complete CSS to `custom.css`:
- Chat button (bottom-right)
- Chat window with animations
- Message bubbles (user/bot)
- Typing indicator
- Input field
- Selection popup
- Dark mode support
- Responsive design

---

## Testing Steps

### 1. Start Backend
```bash
cd backend
python main.py
```
Backend should be running on: http://localhost:8000

### 2. Test Backend Directly
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is ROS 2?", "level": "Beginner"}'
```

Expected response:
```json
{
  "status": "success",
  "message": "...",
  "sources": [...],
  ...
}
```

### 3. Start Frontend
```bash
cd physical-ai-book
npm start
```
Frontend should be running on: http://localhost:3000

### 4. Test Chat Widget

1. **Open any chapter page** (e.g., http://localhost:3000/docs/module1/chapter1-ros2-introduction)

2. **Look for chat button** - Should be in bottom-right corner:
   ```
   ┌─────────────────────┐
   │                     │
   │                     │
   │                     │
   │         💬 Ask AI   │  ← Bottom-right
   └─────────────────────┘
   ```

3. **Click "💬 Ask AI"** - Chat window should open

4. **Type a question** - e.g., "What is ROS 2?"

5. **Press Enter or click Send**

6. **Expected behavior:**
   - Your message appears on right (purple bubble)
   - Typing indicator shows (3 dots animating)
   - Bot response appears on left (white bubble)
   - Response contains textbook content

---

## Debug Commands

### Check if chatbot.js is loaded
Open browser console (F12) and type:
```javascript
console.log('Chatbot loaded:', !!document.getElementById('chat-widget-button'));
```

Should print: `Chatbot loaded: true`

### Check backend connection
Open browser console and type:
```javascript
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: 'test', level: 'Beginner'})
}).then(r => r.json()).then(console.log);
```

Should print backend response.

### Check for errors
Open browser console (F12) and look for:
- Red errors in Console tab
- Failed requests in Network tab
- Any CORS errors

---

## Common Issues

### Issue: "Failed to fetch"
**Solution:** Backend is not running. Start it with:
```bash
cd backend
python main.py
```

### Issue: CORS Error
**Solution:** Backend CORS might be misconfigured. Check `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Chat button not visible
**Solution:** 
1. Check if custom.css is loaded
2. Clear browser cache (Ctrl+Shift+R)
3. Check browser console for errors

### Issue: Response shows "Error: ..."
**Solution:** 
1. Check backend logs for errors
2. Verify API key is set in `.env`
3. Test backend directly with curl

---

## Files Modified

| File | Changes |
|------|---------|
| `physical-ai-book/static/chatbot.js` | Fixed endpoint, request body, response handling, event listeners |
| `physical-ai-book/src/css/custom.css` | Added complete chat widget styles |

---

## Quick Test

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend  
cd physical-ai-book
npm start

# Browser - Open http://localhost:3000
# Look for 💬 Ask AI button in bottom-right
# Click it and ask "What is ROS 2?"
```

---

<div align="center">

**Chatbot should now be working! 🎉**

</div>
