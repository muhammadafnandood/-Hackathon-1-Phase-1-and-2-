# 🔧 Debugging Chat Widget Issues

## Problem
Floating chat button and text selection popup are not clickable/not appearing.

## Quick Fixes

### Fix 1: Check Browser Console
1. Press **F12** to open Developer Tools
2. Click **Console** tab
3. Look for errors (red text)
4. Screenshot any errors you see

### Fix 2: Check if Widget Loaded
1. Press **F12** → **Console**
2. Type: `document.getElementById('rag-chatbot-toggle')`
3. Press Enter
4. If it shows `null` → Widget didn't load
5. If it shows `<button>` → Widget loaded, check event listeners

### Fix 3: Manual Widget Test
1. Press **F12** → **Console**
2. Paste this code:
```javascript
console.log('Widget test:', document.getElementById('rag-chatbot-toggle'));
```
3. Press Enter
4. Check output

### Fix 4: Check Script Loading
1. Press **F12** → **Network** tab
2. Refresh page (F5)
3. Look for `chat-widget.js`
4. Check if status is `200` (loaded) or `404` (not found)

---

## Common Issues & Solutions

### Issue 1: Widget Not Appearing
**Cause**: Script not loading

**Solution**:
```html
<!-- Make sure this line exists in index.html -->
<script src="rag-chatbot/chat-widget.js"></script>
```

### Issue 2: Button Visible But Not Clickable
**Cause**: Event listeners not attached

**Solution**: Add this to console:
```javascript
const btn = document.getElementById('rag-chatbot-toggle');
btn.click(); // Should open chat
```

### Issue 3: Text Selection Not Working
**Cause**: Popup not created

**Solution**: Check if this exists in index.html:
```html
<div id="text-selection-popup">💬 Ask AI about this</div>
```

---

## Manual Test Commands

### Open Chat Manually
```javascript
document.getElementById('rag-chatbot-toggle').click();
```

### Check Widget Status
```javascript
console.log({
    widget: document.getElementById('rag-chatbot-widget'),
    button: document.getElementById('rag-chatbot-toggle'),
    window: document.getElementById('rag-chatbot-window'),
    input: document.getElementById('rag-chatbot-input')
});
```

### Force Widget Creation
```javascript
// Run in console to recreate widget
location.reload();
```

---

## Alternative: Use Test Page

Open: `test-chat.html`

This minimal page loads ONLY the chat widget without other distractions.

---

## Backend Check

Make sure backend is running:
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy"}`

---

## Quick Reload Steps

1. **Stop backend** (if running):
   ```
   taskkill /F /T /PID 9960
   ```

2. **Restart backend**:
   ```bash
   cd D:\Hackathon 1\rag-chatbot\backend
   ..\..\venv\Scripts\python.exe main.py
   ```

3. **Refresh browser**:
   - Press `Ctrl + Shift + R` (hard refresh)
   - Or press `F5`

4. **Open console** (F12) and check for errors

---

## Expected Behavior

### What You Should See:
1. ✅ Purple chat button (💬) in bottom-right corner
2. ✅ Button has shadow and hover effect
3. ✅ Click button → Chat window opens
4. ✅ Select text → Purple popup appears
5. ✅ Click popup → Chat opens with selected text

### What Should NOT Happen:
- ❌ No console errors
- ❌ Button not appearing
- ❌ Button visible but not clickable
- ❌ Popup not appearing on text selection

---

## Still Not Working?

### Try This:
1. Open `test-chat.html` instead of `index.html`
2. Check if widget appears there
3. If YES → Problem is with `index.html`
4. If NO → Problem is with `chat-widget.js`

### Last Resort:
1. Clear browser cache: `Ctrl + Shift + Delete`
2. Close all browser windows
3. Reopen browser
4. Go to `index.html`

---

## Success Indicators

You'll know it's working when:
- ✅ Chat button visible in bottom-right
- ✅ Hover effect on button (scales up)
- ✅ Click opens chat window
- ✅ Text selection shows popup
- ✅ No console errors

---

## Contact Info (For Hackathon Team)

If still stuck:
1. Take screenshot of browser
2. Take screenshot of console (F12)
3. Take screenshot of network tab
4. Share with team for debugging

---

**Good luck! 🚀**
