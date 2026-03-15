# Implementation Plan: Module 2 - Digital Twin (Gazebo & Unity)

**Branch**: `master` | **Date**: 2026-03-11 | **Spec**: Module 2 Digital Twin Textbook

**Input**: Module 2 specification for robot simulation textbook with Gazebo and Unity

## Summary

Build **Module 2 of the Physical AI & Humanoid Robotics textbook** focusing on robot simulation using Gazebo physics and Unity visualization. The module includes 5 comprehensive chapters with hands-on labs, code examples, and RAG chatbot integration for AI-assisted learning.

## Technical Context

**Language/Version**:
- Content: Markdown (Docusaurus)
- Code: Python 3.11+ (rclpy), C# (Unity), URDF/SDF, YAML, Bash

**Primary Dependencies**:
- Docusaurus v3.x (documentation platform)
- Gazebo Harmonic (physics simulation)
- Unity 2021+ HDRP (visualization)
- ROS2 Humble (robot middleware)
- ROS# (Unity-ROS bridge)
- FastAPI + Qdrant + OpenAI (RAG chatbot)

**Storage**:
- Qdrant Cloud: Vector embeddings (textbook chunks)
- File system: Markdown content, code examples, lab files

**Testing**:
- Simulation testing in Gazebo
- Visualization testing in Unity
- RAG retrieval validation

**Target Platform**:
- Web browser (Docusaurus deployment)
- Ubuntu 22.04 (simulation development)
- Windows/macOS (Unity development)

**Project Type**: Documentation with executable code examples

**Performance Goals**:
- All code examples executable and tested
- Labs completable in 60-120 minutes each
- RAG chatbot response < 3 seconds

**Constraints**:
- Content must be RAG-chunkable (500-1000 words per section)
- Code examples must be complete and runnable
- Labs must have simulation alternatives for students without hardware

**Scale/Scope**:
- 5 chapters, ~50 pages total
- 20+ code examples
- 5 hands-on labs
- 25 exercises

## Constitution Check

*GATE: Must pass before content generation.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Educational Clarity** | ✅ PASS | Each chapter includes learning objectives, explanations, examples, labs, summaries, exercises |
| **II. Step-by-Step Progression** | ✅ PASS | Chapters progress from concepts → Gazebo → sensors → Unity → complete digital twin |
| **III. Practical Engineering Focus** | ✅ PASS | All labs use real robotics tools (Gazebo, Unity, ROS2) |
| **IV. AI-Native Content Structure** | ✅ PASS | Short sections, descriptive headings, RAG-chunkable |
| **V. RAG-Ready Architecture** | ✅ PASS | Content structured for vector embeddings and retrieval |
| **VI. Personalization & Accessibility** | ✅ PASS | Simulation alternatives for all hardware-dependent labs |
| **VII. Hardware Awareness** | ✅ PASS | Three tiers: Gazebo only, Unity visualization, complete digital twin |
| **VIII. Reusable Intelligence** | ✅ PASS | Code examples are modular and reusable |
| **IX. Documentation Standards** | ✅ PASS | Markdown, Docusaurus compatible, Mermaid diagrams |
| **X. Modular Course Structure** | ✅ PASS | Follows 5-chapter module structure |

**Constitution Compliance**: ALL GATES PASSED ✅

## Project Structure

### Documentation Output

```text
physical-ai-book/docs/module2/
├── chapter1-intro-simulation.md       # Chapter 1: Introduction
├── chapter2-gazebo-environment.md     # Chapter 2: Gazebo Setup
├── chapter3-physics-and-sensors.md    # Chapter 3: Sensors
├── chapter4-unity-visualization.md    # Chapter 4: Unity
└── chapter5-building-digital-twin.md  # Chapter 5: Complete Twin
```

### Code Examples Structure

```text
physical-ai-book/docs/module2/code/
├── chapter1/
│   ├── install_gazebo.sh
│   └── simple_world.sdf
├── chapter2/
│   ├── simple_robot.urdf
│   ├── gazebo_launch.py
│   └── simple_controller.py
├── chapter3/
│   ├── biped_humanoid.urdf
│   ├── walking_controller.py
│   └── sensor_fusion.py
├── chapter4/
│   ├── RobotController.cs
│   ├── CameraController.cs
│   └── unity_streamer.py
└── chapter5/
    ├── digital_twin_launch.py
    ├── synchronizer.py
    └── sensor_fusion_ekf.py
```

### Lab Files

```text
physical-ai-book/docs/module2/labs/
├── lab1-simulation-setup/
├── lab2-gazebo-robot/
├── lab3-sensor-data/
├── lab4-unity-viz/
└── lab5-digital-twin/
```

## Content Generation Plan

### Chapter 1: Introduction to Robot Simulation

**Topics**:
- Why simulate robots? (safety, cost, speed)
- Digital Twin concept
- Physics engines (ODE, Bullet, DART, PhysX)
- Sim-to-Real transfer
- High-fidelity rendering

**Code Examples**:
- Gazebo installation script
- Unity installation guide
- Simple world SDF file
- Python launch script

**Lab**: Install and run first simulation

**Length**: 8-10 pages

### Chapter 2: Gazebo Simulation Environment

**Topics**:
- Gazebo architecture (Sim vs Classic)
- URDF vs SDF formats
- Physics simulation parameters
- Sensor plugins (LiDAR, camera, IMU)
- ROS2 integration (ros_gz bridge)

**Code Examples**:
- Complete URDF robot model
- Gazebo world file with sensors
- ROS2 launch file
- Python controller node

**Lab**: Simulate mobile robot with obstacle avoidance

**Length**: 10-12 pages

### Chapter 3: Physics and Sensors

**Topics**:
- Rigid body dynamics
- Contact physics and friction
- Sensor calibration and noise
- Depth camera processing
- IMU data interpretation
- LiDAR scanning

**Code Examples**:
- Biped humanoid URDF
- Walking gait controller
- Sensor fusion node
- Point cloud generation

**Lab**: Record sensor data during biped walking

**Length**: 10-12 pages

### Chapter 4: Unity Robot Visualization

**Topics**:
- Unity rendering pipelines (HDRP, URP)
- ROS# integration
- Camera systems for HRI
- Scene building
- Gazebo-Unity bridge

**Code Examples**:
- Unity C# ROS# subscriber
- Camera controller script
- Python data streamer
- LiDAR visualization

**Lab**: Visualize Gazebo robot in Unity

**Length**: 10-12 pages

### Chapter 5: Building the Digital Twin

**Topics**:
- Complete digital twin architecture
- Robot model integration
- Sensor fusion (Kalman Filter)
- AI perception testing
- Best practices

**Code Examples**:
- Complete launch file
- Digital twin synchronizer
- EKF sensor fusion
- Humanoid digital twin

**Lab**: Build complete humanoid digital twin

**Length**: 10-12 pages

## RAG Chatbot Integration

### Content Chunking Strategy

```python
# Chunking parameters
chunk_size = 800  # characters
chunk_overlap = 100  # characters

# Metadata per chunk
{
    "chapter_id": "module2/chapter1",
    "section": "Learning Objectives",
    "heading_hierarchy": ["Chapter 1", "Learning Objectives"],
    "module": "module2",
    "difficulty": "beginner"
}
```

### Embedding Pipeline

```bash
# Generate embeddings for all chapters
python backend/src/scripts/embed_textbook.py \
  --input docs/module2/ \
  --output qdrant \
  --collection physical-ai-textbook
```

### Expected Embeddings

- **Total chunks**: ~500 (5 chapters × 10 sections × 10 chunks)
- **Embedding size**: 3072 (text-embedding-3-large)
- **Storage**: ~6 MB in Qdrant

### RAG Test Queries

```python
test_queries = [
    "What is a Digital Twin?",
    "How do I install Gazebo?",
    "Explain URDF vs SDF",
    "How to add LiDAR sensor in Gazebo?",
    "What is ROS#?",
    "How to integrate Gazebo with Unity?",
    "Explain sensor fusion with Kalman Filter",
    "What are best practices for digital twins?"
]
```

## Development Phases

### Phase 1: Content Generation (COMPLETED ✅)

**Tasks**:
- [x] Chapter 1: Introduction to Robot Simulation
- [x] Chapter 2: Gazebo Simulation Environment
- [x] Chapter 3: Physics and Sensors
- [x] Chapter 4: Unity Robot Visualization
- [x] Chapter 5: Building the Digital Twin

**Deliverables**:
- 5 Markdown files in `docs/module2/`
- 20+ code examples
- 5 hands-on labs
- 25 exercises

**Status**: ✅ COMPLETE

### Phase 2: Sidebar Configuration (COMPLETED ✅)

**Tasks**:
- [x] Update `sidebars.ts` with Module 2 chapters
- [x] Organize chapters in correct order
- [x] Add chapter labels

**Status**: ✅ COMPLETE

### Phase 3: Code Testing (PENDING)

**Tasks**:
- [ ] Test all Python code examples in Gazebo
- [ ] Test all Unity C# scripts
- [ ] Verify URDF/SDF files in simulation
- [ ] Test ROS2 launch files

**Environment Setup**:
```bash
# Ubuntu 22.04 with ROS2 Humble
sudo apt install ros-humble-gazebo-ros-pkg
pip install rclpy numpy filterpy
```

### Phase 4: RAG Integration (PENDING)

**Tasks**:
- [ ] Chunk Module 2 content
- [ ] Generate embeddings
- [ ] Store in Qdrant
- [ ] Test RAG retrieval with test queries
- [ ] Validate chatbot answers

**Backend Setup**:
```bash
cd backend
python src/scripts/embed_textbook.py --input docs/module2/
```

### Phase 5: Deployment (PENDING)

**Tasks**:
- [ ] Build Docusaurus site
- [ ] Deploy to GitHub Pages
- [ ] Test live site
- [ ] Demo for hackathon judges

**Deployment Command**:
```bash
cd physical-ai-book
npm run build
npm run deploy
```

## Success Criteria

### Content Quality
- [x] All 5 chapters completed
- [x] Learning objectives clear for each chapter
- [x] Code examples complete and commented
- [x] Labs have step-by-step instructions
- [x] Exercises test comprehension

### Technical Accuracy
- [ ] All code examples tested and runnable
- [ ] URDF/SDF files valid
- [ ] ROS2 launch files functional
- [ ] Unity scripts compile

### RAG Chatbot
- [ ] Content chunked correctly
- [ ] Embeddings generated
- [ ] Retrieval accuracy > 90%
- [ ] Chatbot answers relevant

### Deployment
- [ ] Docusaurus builds without errors
- [ ] Site deployed successfully
- [ ] All links working
- [ ] Navigation functional

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Phase 1: Content Generation | 2 days | ✅ COMPLETE |
| Phase 2: Sidebar Config | 1 hour | ✅ COMPLETE |
| Phase 3: Code Testing | 2 days | ⏳ PENDING |
| Phase 4: RAG Integration | 1 day | ⏳ PENDING |
| Phase 5: Deployment | 1 day | ⏳ PENDING |

**Total Estimated Time**: 6-7 days

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Code examples don't run | High | Medium | Test in clean environment, provide Docker containers |
| Unity-Gazebo integration fails | Medium | Medium | Provide alternative (Gazebo-only) workflow |
| RAG retrieval inaccurate | High | Low | Fine-tune chunking, add metadata filtering |
| Deployment issues | Medium | Low | Test deployment early, use GitHub Actions |

## Next Steps

1. **Immediate**: Test code examples in simulation
2. **Short-term**: Integrate RAG chatbot
3. **Long-term**: Deploy and demo for hackathon

---

**Plan Status**: Phase 1 & 2 COMPLETE ✅

**Next Command**: `/sp.tasks` to generate implementation tasks for Phases 3-5
