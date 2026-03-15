---
id: 005
title: Urdu Translation Button with English/Urdu Toggle
stage: green
date: 2026-03-15T00:00:00Z
surface: agent
model: qwen-coder
feature: master
branch: main
user: Muhammad Afnan
command: Add Urdu translation feature to chatbot
labels: ["ui", "translation", "urdu", "i18n"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - rag-chatbot/chat-widget.js
  - custom-chat.html
  - text-selection-chat.html
tests:
  - Manual testing of Urdu translation API integration
  - Toggle button functionality verification
---

## Prompt

Add a "Translate to Urdu" button below each AI answer.

When clicked:
- call API /translate
- send text of the answer
- show translated Urdu text below the original answer

Make toggle option:
- English / Urdu

## Response snapshot

Implemented Urdu translation feature across all three chat interfaces:

### Features Added:
1. **Translate to Urdu Button** - Green gradient button below each AI answer
2. **Urdu Text Display** - RTL-formatted text box with light green background
3. **Toggle Button** - Switch between English and Urdu views
4. **Loading State** - Shows "ترجمہ ہو رہا ہے..." (Translating...) during API call
5. **Error Handling** - Shows error message if translation fails

### API Integration:
- Endpoint: `POST /api/translate/urdu`
- Request: `{ content: string, language: 'urdu' }`
- Response: `{ translated: string, fromCache: boolean, language: 'urdu' }`

### Files Modified:
1. `rag-chatbot/chat-widget.js` - Floating chat widget with translation
2. `custom-chat.html` - Custom chat page with translation
3. `text-selection-chat.html` - Text selection popup with translation

### UI Flow:
1. User receives AI answer in English
2. Clicks "Translate to Urdu" button (🌐 icon)
3. Urdu translation appears below with RTL formatting
4. Toggle button shows "Show English" / "Show Urdu" to switch views

## Outcome

- ✅ Impact: Users can now read AI answers in Urdu for better accessibility
- 🧪 Tests: Manual testing required - verify API `/api/translate/urdu` is available
- 📁 Files: 3 files modified (chat-widget.js, custom-chat.html, text-selection-chat.html)
- 🔁 Next prompts: Test with backend to ensure translation API works correctly
- 🧠 Reflection: Used RTL direction for Urdu text, added loading state in Urdu script

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation complete
- Graders run and results (PASS/FAIL): N/A - UI changes, requires backend API
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify backend has `/api/translate/urdu` endpoint implemented
