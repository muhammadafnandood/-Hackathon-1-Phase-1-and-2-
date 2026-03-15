<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0 (Initial constitution)

Added Principles:
- I. Educational Clarity
- II. Step-by-Step Technical Progression
- III. Practical Engineering Focus
- IV. AI-Native Content Structure
- V. RAG-Ready Architecture
- VI. Personalization & Accessibility
- VII. Hardware Awareness
- VIII. Reusable Intelligence
- IX. Documentation Standards
- X. Modular Course Structure

Added Sections:
- Mission Statement
- Book Writing Standards
- Course Module Structure
- AI-Native Requirements
- Hardware Tiers
- Output Style Guidelines

Templates requiring updates:
- ✅ plan-template.md (Constitution Check section aligns)
- ✅ spec-template.md (User story format compatible)
- ✅ tasks-template.md (Phase-based structure compatible)

Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Mission

Produce a production-quality AI-native textbook titled **"Physical AI & Humanoid Robotics"** that teaches students to design, simulate, and deploy humanoid robots using modern AI and robotics tools.

The textbook MUST integrate:
- ROS 2 for robotic nervous system architecture
- Gazebo and Unity for digital twin simulation
- NVIDIA Isaac Sim for AI robot brain development
- Vision-Language-Action models for conversational robotics
- RAG-based chatbot for AI-assisted learning

All content MUST be structured for Docusaurus deployment with GitHub Pages integration and AI RAG assistant capabilities.

---

## Core Principles

### I. Educational Clarity
Every chapter MUST include clear educational explanations with:
- Learning Objectives stated upfront
- Concept Explanations in accessible language
- Architecture Overviews with diagrams
- Code Examples in Python/ROS 2
- Hands-on Labs with step-by-step instructions
- Summaries reinforcing key concepts
- Exercises for skill reinforcement

Writing style MUST be clear, professional, engineering-focused, and beginner-to-advanced friendly. Marketing language is prohibited.

**Rationale:** Students learn best when content follows a predictable, pedagogically sound structure that progresses from theory to practice.

### II. Step-by-Step Technical Progression
All technical tutorials MUST follow incremental progression:
- Start with foundational concepts before advanced topics
- Each tutorial builds on previous knowledge
- Code examples are complete and runnable
- Architecture diagrams illustrate system design
- Exercises reinforce learned concepts

Complex topics MUST be decomposed into digestible steps with clear transitions between difficulty levels.

**Rationale:** Robotics and AI are complex domains; incremental learning prevents cognitive overload and ensures comprehension.

### III. Practical Engineering Focus
The textbook MUST emphasize real-world engineering over theory:
- ROS 2 Python code examples using rclpy
- Simulation workflows in Gazebo and Isaac Sim
- AI perception pipelines with real sensors
- Deployment-ready configurations
- Hardware-in-the-loop testing where applicable

Every chapter MUST answer: "How do I build this in practice?"

**Rationale:** Students need job-ready skills; practical workflows ensure immediate applicability in industry or research.

### IV. AI-Native Content Structure
All content MUST be structured for AI-assisted learning:
- Short sections (500-1000 words max)
- Descriptive headings for semantic search
- Code blocks with language annotations
- Explicit definitions for key terms
- Metadata for chunking into embeddings

Content MUST support RAG-based Q&A, context-aware explanations, and semantic search capabilities.

**Rationale:** AI-native textbooks enable personalized learning at scale through vector search and LLM-powered assistance.

### V. RAG-Ready Architecture
The accompanying chatbot system MUST support:
1. Vector search over textbook content (Qdrant)
2. Metadata queries (Neon PostgreSQL)
3. Context-aware responses from LLM
4. Selected text explanations
5. Multi-turn robotics concept discussions

Embedding flow: Book Content → Chunking → Embeddings → Qdrant → Retrieval → LLM Response

**Rationale:** RAG systems extend learning beyond static content, enabling interactive, context-aware education.

### VI. Personalization & Accessibility
The system MUST adapt to individual learners:

**Onboarding Profile:**
- Programming experience level
- AI/ML experience level
- Robotics experience level
- Hardware availability
- GPU capability

**Chapter Personalization:**
- "Personalize This Chapter" button adapts explanations
- Labs suggested based on available hardware
- Key concepts highlighted for skill level

**Urdu Translation:**
- "Translate to Urdu" button on each chapter
- Technical terms remain in English
- Explanations translated for Pakistani students
- Readability maintained for non-native English speakers

**Rationale:** Diverse learners have diverse needs; personalization increases completion rates and comprehension.

### VII. Hardware Awareness
The textbook MUST acknowledge three hardware tiers:

**Tier 1 — High-end Workstation:**
- RTX 4080 / 4090 GPU
- 64GB RAM
- Ubuntu 22.04

**Tier 2 — Jetson Edge Kit:**
- Jetson Orin Nano
- RealSense Camera
- IMU Sensors

**Tier 3 — Physical Robots:**
- Unitree Go2
- Humanoid platforms
- Robotic arms

All labs MUST specify required hardware AND provide simulation alternatives.

**Rationale:** Students have varying access to hardware; simulation alternatives ensure inclusivity.

### VIII. Reusable Intelligence
Claude Code Subagents MUST be created for reusable component generation:
1. **Book Writer Agent** — Generates chapter content
2. **Robotics Code Generator** — Produces ROS 2 code
3. **ROS 2 Architecture Designer** — Designs system architecture
4. **RAG Knowledge Indexer** — Embeds content for search
5. **Urdu Translator** — Handles translation workflow
6. **Chapter Personalizer** — Adapts content to user profile

All agents MUST produce reusable, composable components.

**Rationale:** Agent-based workflows enable scalable content generation and consistent quality.

### IX. Documentation Standards
All outputs MUST be:
- Structured Markdown
- Docusaurus compatible
- Include diagrams (Mermaid or images) where possible
- Include code blocks with proper syntax highlighting

**Supported Languages:** python, bash, yaml, ros

**Directory Structure:**
```text
docs/
├── intro.md
├── module1/
│   ├── ros2-basics.md
│   ├── nodes-topics-services.md
│   └── urdf-humanoid.md
├── module2/
│   ├── gazebo-simulation.md
│   ├── unity-visualization.md
│   └── sensor-simulation.md
├── module3/
│   ├── isaac-sim.md
│   ├── visual-slam.md
│   └── nav2-navigation.md
├── module4/
│   ├── vla-models.md
│   ├── voice-to-action.md
│   └── robot-planning.md
└── capstone/
    └── autonomous-humanoid.md
```

**Rationale:** Standardized structure enables automated deployment and consistent user experience.

### X. Modular Course Structure
The textbook MUST strictly follow the four-module structure plus capstone:

**Module 1 — ROS 2 Robotic Nervous System:**
- ROS 2 architecture (nodes, topics, services, actions)
- rclpy Python library
- URDF humanoid modeling

**Module 2 — Digital Twin Simulation:**
- Gazebo simulation and physics engines
- Robot environment building
- Unity visualization
- Sensor simulation (Lidar, Depth Camera, IMU)

**Module 3 — AI Robot Brain:**
- NVIDIA Isaac Sim
- Synthetic data generation
- Visual SLAM and Isaac ROS
- Navigation with Nav2
- Reinforcement learning basics

**Module 4 — Vision Language Action:**
- LLM + robotics integration
- Voice commands using Whisper
- LLM planning for robot actions
- Robot task decomposition
- Conversational robotics

**Final Capstone:**
Autonomous humanoid robot that:
1. Receives voice commands
2. Plans actions using LLM
3. Navigates environment
4. Detects objects
5. Manipulates objects

**Rationale:** Modular structure enables progressive skill building and clear learning pathways.

---

## Book Writing Standards

Each chapter MUST include:
1. **Learning Objectives** — What students will achieve
2. **Concept Explanation** — Theory with practical context
3. **Architecture Overview** — System diagram and component relationships
4. **Code Examples** — Complete, runnable ROS 2 Python code
5. **Hands-on Lab** — Step-by-step practical exercise
6. **Summary** — Key takeaways
7. **Exercises** — Practice problems for reinforcement

**Quality Gates:**
- All code must be tested and runnable
- All diagrams must be clear and labeled
- All labs must have simulation alternatives
- All sections must support Urdu translation
- All content must be RAG-chunkable

---

## Technical Stack Requirements

**Frontend:**
- Docusaurus for documentation site
- ChatKit SDK for RAG chatbot integration

**Backend:**
- FastAPI for chatbot API
- Qdrant for vector database
- Neon PostgreSQL for metadata

**Robotics Stack:**
- ROS 2 (Humble or Jazzy)
- Gazebo Classic / Gazebo Sim
- Unity with ROS 2 Sharp
- NVIDIA Isaac Sim
- Isaac ROS packages

**AI/ML Stack:**
- Vision-Language-Action models
- Whisper for speech-to-text
- LLM for task planning
- Embedding models for RAG

---

## Development Workflow

**Content Generation:**
1. Spec-Kit commands orchestrate agent workflows
2. PHR (Prompt History Records) track all decisions
3. ADRs document architectural decisions
4. Constitution compliance verified per chapter

**Quality Assurance:**
1. All code examples tested in simulation
2. All labs validated on hardware tiers
3. Urdu translations reviewed for accuracy
4. RAG retrieval tested for each chapter

**Deployment:**
1. GitHub Pages for textbook hosting
2. Docker containers for chatbot deployment
3. CI/CD for automated builds and tests

---

## Governance

This constitution supersedes all other development practices. Amendments require:
1. Documentation of proposed change
2. Rationale explaining benefit to mission
3. Impact analysis on existing content
4. Migration plan for affected chapters

**Compliance Verification:**
- All PRs MUST verify constitution compliance
- Constitution Check gate in plan-template.md MUST pass
- Complexity violations MUST be justified in writing

**Versioning Policy:**
- MAJOR: Backward incompatible principle changes
- MINOR: New principles or material expansions
- PATCH: Clarifications, wording, typo fixes

**Review Cadence:**
Constitution reviewed quarterly or upon significant scope changes.

---

**Version**: 1.0.0 | **Ratified**: 2026-03-11 | **Last Amended**: 2026-03-11
