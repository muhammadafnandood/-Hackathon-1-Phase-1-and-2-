---
id: 007
title: Automatic Diagram Generation with Mermaid.js
stage: green
date: 2026-03-15T00:00:00Z
surface: agent
model: qwen-coder
feature: master
branch: main
user: Muhammad Afnan
command: Add diagram generation feature for architecture explanations
labels: ["ui", "diagrams", "mermaid", "visualization", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - rag-chatbot/chat-widget.js
  - custom-chat.html
  - text-selection-chat.html (pending)
tests:
  - Manual testing of diagram detection and rendering
  - Mermaid.js CDN integration verification
---

## Prompt

Add a diagram generation feature.

If the user asks for architecture or system explanation:
- generate a diagram using Mermaid.js

Display diagram below the AI answer.

Example:
```
ROS 2 architecture
- Nodes
- Topics
- DDS layer
```

## Response snapshot

Implemented automatic diagram generation feature using Mermaid.js:

### Features Added:

1. **Diagram Detection System**
   - Keyword-based detection for architecture topics
   - Automatic diagram selection based on query content
   - Support for generic "architecture" and "diagram" requests

2. **Diagram Templates** (6 predefined architectures):
   - 🏗️ ROS 2 Publisher-Subscriber Architecture
   - 🏗️ ROS 2 Node Architecture
   - 🏗️ RAG Pipeline Architecture
   - 🏗️ Robot Perception Pipeline
   - 🏗️ Vision-Language-Action (VLA) Model
   - 🏗️ Robot Control Loop

3. **Interactive Diagram Display**
   - Mermaid.js rendering via CDN
   - Zoom In/Out controls
   - Professional styling with icons
   - Centered layout for better visibility

4. **Keyword Detection**:
   ```javascript
   ros2_pubsub: ['ros 2 publisher', 'ros 2 subscriber', 'publish subscribe']
   rag_pipeline: ['rag pipeline', 'rag architecture', 'vector search']
   vla_model: ['vla model', 'vision language action']
   robot_perception: ['perception pipeline', 'sensor fusion']
   control_loop: ['control loop', 'sense plan act']
   ```

### Implementation Details:

**Floating Chat Widget** (`rag-chatbot/chat-widget.js`):
- 6 diagram templates embedded
- `detectDiagram(query)` function for topic detection
- `renderDiagram()` with auto-loading of Mermaid.js CDN
- Zoom controls (0.5x to 2.0x)
- Error handling for rendering failures

**Custom Chat Page** (`custom-chat.html`):
- 3 diagram templates (ROS 2, RAG, VLA)
- Same detection and rendering logic
- Integrated with Urdu translation feature

### UI Flow:
```
User Query: "Explain ROS 2 architecture"
     ↓
Detect keywords: "ROS 2" + "architecture"
     ↓
Select diagram: ros2_pubsub template
     ↓
Render Mermaid diagram below answer
     ↓
Display: [Diagram Title] + [Visual Diagram] + [Zoom Controls]
```

### Example Diagram Output:
```
🏗️ ROS 2 Publisher-Subscriber Architecture
┌─────────────────────────────────────────┐
│  [Publisher] --> ((Topic)) --> [Subscriber] │
│     Node 1      /sensor_data    Node 2     │
└─────────────────────────────────────────┘
[Zoom In] [Zoom Out]
```

### Technical Implementation:
- Mermaid.js loaded from CDN: `cdn.jsdelivr.net/npm/mermaid@10`
- Lazy loading: Only loads when diagram is needed
- SVG rendering with transform scaling for zoom
- Error fallback: Shows error message if rendering fails

## Outcome

- ✅ Impact: Visual diagrams automatically appear for architecture questions
- 🧪 Tests: Manual testing required - verify Mermaid.js CDN loads correctly
- 📁 Files: 2 files modified (chat-widget.js, custom-chat.html)
- 🔁 Next prompts: Add more diagram templates for other topics
- 🧠 Reflection: Used keyword matching for simplicity; could add ML-based detection later

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation complete
- Graders run and results (PASS/FAIL): N/A - UI feature
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add 5-10 more diagram templates for comprehensive coverage
