---
id: 004
title: Source Citation UI Enhancement with Chapter Links and Confidence
stage: green
date: 2026-03-15T00:00:00Z
surface: agent
model: qwen-coder
feature: master
branch: main
user: Muhammad Afnan
command: UI modification for source citations
labels: ["ui", "chatbot", "citations", "sources"]
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
  - Manual testing of chat widget source display
---

## Prompt

Modify the chatbot UI so that it displays sources returned by the API.

Sources format:
"sources":[{"chapter":"Chapter5"}]

Make each source clickable:
link should open
/docs/chapter5

Display confidence percentage as well.

## Response snapshot

Updated three chat interface files to display source citations with:
1. Clickable chapter links pointing to `/docs/chapter{number}`
2. Confidence percentage badges displayed next to each source
3. Improved styling with hover effects and visual separation

Files modified:
- `rag-chatbot/chat-widget.js` - Main floating chat widget
- `custom-chat.html` - Custom chat page
- `text-selection-chat.html` - Text selection popup chat

## Outcome

- ✅ Impact: Judges can now see source chapters with clickable links and confidence scores for better transparency
- 🧪 Tests: Manual testing required - verify sources display below answers with working links
- 📁 Files: 3 files modified (chat-widget.js, custom-chat.html, text-selection-chat.html)
- 🔁 Next prompts: Test with backend API to verify sources and confidence are displayed correctly
- 🧠 Reflection: Extracted chapter number from various formats (Chapter5, Chapter 5) using regex for flexible URL generation

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation straightforward
- Graders run and results (PASS/FAIL): N/A - UI changes only
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify backend returns `confidence` field in API response; if not, add it
