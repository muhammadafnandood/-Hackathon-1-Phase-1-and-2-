# Tasks: Module 2 - Digital Twin (Gazebo & Unity)

**Input**: Design documents from `specs/module2/`
**Prerequisites**: plan.md (required), spec.md (not applicable - content project), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - Code testing tasks included for validation of simulation examples.

**Organization**: Tasks are grouped by development phase (Setup → Foundational → Content Testing → RAG → Deployment) to enable incremental delivery.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Not applicable for this content project (phases used instead)
- Include exact file paths in descriptions

## Path Conventions

- **Documentation**: `physical-ai-book/docs/module2/`
- **Code Examples**: `physical-ai-book/docs/module2/code/`
- **Lab Files**: `physical-ai-book/docs/module2/labs/`
- **Backend**: `physical-ai-book/backend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment setup

- [X] T001 [P] Create code examples directory structure in physical-ai-book/docs/module2/code/chapter{1-5}/
- [X] T002 [P] Create lab files directory structure in physical-ai-book/docs/module2/labs/lab{1-5}/
- [ ] T003 [P] Verify Gazebo Harmonic installation on Ubuntu 22.04
- [ ] T004 [P] Verify Unity 2021+ HDRP installation
- [ ] T005 [P] Verify ROS2 Humble installation with ros_gz packages
- [X] T006 [P] Install Python dependencies (rclpy, numpy, filterpy) in physical-ai-book/backend/requirements.txt

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before code testing

**⚠️ CRITICAL**: No code testing can begin until this phase is complete

- [X] T007 [P] Create example code template structure in physical-ai-book/docs/module2/code/README.md
- [X] T008 [P] Create lab template with instructions in physical-ai-book/docs/module2/labs/README.md
- [ ] T009 [P] Setup ROS2 workspace for testing in ~/ros2_ws/
- [ ] T010 [P] Configure Qdrant Cloud connection in physical-ai-book/backend/.env
- [ ] T011 [P] Verify OpenAI API access for RAG embeddings
- [ ] T012 [P] Create content chunking script in physical-ai-book/backend/src/scripts/chunk_content.py

**Checkpoint**: Foundation ready - code testing can now begin

---

## Phase 3: Chapter 1 Code Testing (Priority: P1) 🎯 MVP

**Goal**: Test all code examples from Chapter 1 (Introduction to Simulation)

**Independent Test**: All installation scripts run successfully, simple world loads in Gazebo

### Implementation for Chapter 1

- [X] T013 [P] [CH1] Create Gazebo installation script in physical-ai-book/docs/module2/code/chapter1/install_gazebo.sh
- [X] T014 [P] [CH1] Create Unity installation guide in physical-ai-book/docs/module2/code/chapter1/install_unity.md
- [X] T015 [P] [CH1] Create simple_world.sdf in physical-ai-book/docs/module2/code/chapter1/simple_world.sdf
- [ ] T016 [CH1] Test simple_world.sdf loads in Gazebo without errors
- [X] T017 [CH1] Create Python launch script in physical-ai-book/docs/module2/code/chapter1/launch_simulation.py
- [ ] T018 [CH1] Test launch script executes successfully
- [ ] T019 [CH1] Document troubleshooting steps in physical-ai-book/docs/module2/labs/lab1/TROUBLESHOOTING.md

**Checkpoint**: Chapter 1 code tested and verified

---

## Phase 4: Chapter 2 Code Testing (Priority: P1)

**Goal**: Test all code examples from Chapter 2 (Gazebo Simulation Environment)

**Independent Test**: Mobile robot simulates in Gazebo with working LiDAR obstacle avoidance

### Implementation for Chapter 2

- [ ] T020 [P] [CH2] Create simple_robot.urdf in physical-ai-book/docs/module2/code/chapter2/simple_robot.urdf
- [ ] T021 [P] [CH2] Validate URDF with check_urdf tool
- [ ] T022 [CH2] Create gazebo_world.sdf with sensors in physical-ai-book/docs/module2/code/chapter2/gazebo_world.sdf
- [ ] T023 [CH2] Create gazebo_launch.py in physical-ai-book/docs/module2/code/chapter2/gazebo_launch.py
- [ ] T024 [CH2] Test launch file spawns robot in Gazebo
- [ ] T025 [P] [CH2] Create simple_controller.py in physical-ai-book/docs/module2/code/chapter2/simple_controller.py
- [ ] T026 [CH2] Test controller publishes to /cmd_vel topic
- [ ] T027 [CH2] Verify LiDAR data published to /scan topic
- [ ] T028 [CH2] Test obstacle avoidance behavior in simulation
- [ ] T029 [CH2] Create lab2 instructions in physical-ai-book/docs/module2/labs/lab2/README.md

**Checkpoint**: Chapter 2 code tested and verified

---

## Phase 5: Chapter 3 Code Testing (Priority: P2)

**Goal**: Test all code examples from Chapter 3 (Physics and Sensors)

**Independent Test**: Biped robot walks in Gazebo, sensor data recorded and visualized

### Implementation for Chapter 3

- [ ] T030 [P] [CH3] Create biped_humanoid.urdf in physical-ai-book/docs/module2/code/chapter3/biped_humanoid.urdf
- [ ] T031 [CH3] Validate biped URDF structure and joint limits
- [ ] T032 [P] [CH3] Create walking_controller.py in physical-ai-book/docs/module2/code/chapter3/walking_controller.py
- [ ] T033 [CH3] Test walking gait pattern generation
- [ ] T034 [CH3] Verify biped walks forward in Gazebo
- [ ] T035 [P] [CH3] Create sensor_fusion.py in physical-ai-book/docs/module2/code/chapter3/sensor_fusion.py
- [ ] T036 [CH3] Test sensor fusion node subscribes to /scan and /imu/data
- [ ] T037 [CH3] Verify fused state published to /robot_state
- [ ] T038 [CH3] Create data recording script in physical-ai-book/docs/module2/code/chapter3/record_data.py
- [ ] T039 [CH3] Test rosbag recording of sensor data
- [ ] T040 [CH3] Create data analysis script in physical-ai-book/docs/module2/code/chapter3/analyze_data.py
- [ ] T041 [CH3] Test data visualization with matplotlib
- [ ] T042 [CH3] Create lab3 instructions in physical-ai-book/docs/module2/labs/lab3/README.md

**Checkpoint**: Chapter 3 code tested and verified

---

## Phase 6: Chapter 4 Code Testing (Priority: P2)

**Goal**: Test all code examples from Chapter 4 (Unity Visualization)

**Independent Test**: Unity scene displays robot with ROS# communication working

### Implementation for Chapter 4

- [ ] T043 [P] [CH4] Create Unity project structure in physical-ai-book/docs/module2/code/chapter4/UnityProject/
- [ ] T044 [P] [CH4] Create RobotController.cs in physical-ai-book/docs/module2/code/chapter4/UnityProject/Assets/Scripts/RobotController.cs
- [ ] T045 [CH4] Test RobotController subscribes to /cmd_vel via ROS#
- [ ] T046 [CH4] Verify robot moves in Unity when velocity published
- [ ] T047 [P] [CH4] Create CameraController.cs in physical-ai-book/docs/module2/code/chapter4/UnityProject/Assets/Scripts/CameraController.cs
- [ ] T048 [CH4] Test camera follow behavior
- [ ] T049 [CH4] Test orbital camera rotation
- [ ] T050 [P] [CH4] Create unity_streamer.py in physical-ai-book/docs/module2/code/chapter4/unity_streamer.py
- [ ] T051 [CH4] Test WebSocket server starts on port 8765
- [ ] T052 [CH4] Verify data streaming from ROS2 to Unity
- [ ] T053 [P] [CH4] Create LidarVisualizer.cs in physical-ai-book/docs/module2/code/chapter4/UnityProject/Assets/Scripts/LidarVisualizer.cs
- [ ] T054 [CH4] Test LiDAR point visualization in Unity
- [ ] T055 [CH4] Create ROS# bridge setup guide in physical-ai-book/docs/module2/code/chapter4/ROS_BRIDGE_SETUP.md
- [ ] T056 [CH4] Create lab4 instructions in physical-ai-book/docs/module2/labs/lab4/README.md

**Checkpoint**: Chapter 4 code tested and verified

---

## Phase 7: Chapter 5 Code Testing (Priority: P3)

**Goal**: Test all code examples from Chapter 5 (Building the Digital Twin)

**Independent Test**: Complete digital twin with Gazebo-Unity synchronization working

### Implementation for Chapter 5

- [ ] T057 [P] [CH5] Create digital_twin_launch.py in physical-ai-book/docs/module2/code/chapter5/digital_twin_launch.py
- [ ] T058 [CH5] Test launch file starts Gazebo, ROS2 nodes, and Unity bridge
- [ ] T059 [P] [CH5] Create synchronizer.py in physical-ai-book/docs/module2/code/chapter5/synchronizer.py
- [ ] T060 [CH5] Test state synchronization between physical and digital
- [ ] T061 [CH5] Verify Unity mirrors Gazebo robot motion
- [ ] T062 [P] [CH5] Create sensor_fusion_ekf.py in physical-ai-book/docs/module2/code/chapter5/sensor_fusion_ekf.py
- [ ] T063 [CH5] Test EKF implementation with simulated data
- [ ] T064 [CH5] Verify state estimation accuracy
- [ ] T065 [CH5] Create humanoid_digital_twin.urdf in physical-ai-book/docs/module2/code/chapter5/humanoid_digital_twin.urdf
- [ ] T066 [CH5] Test complete humanoid model in Gazebo
- [ ] T067 [CH5] Create digital twin validation script in physical-ai-book/docs/module2/code/chapter5/validate_twin.py
- [ ] T068 [CH5] Test synchronization latency measurement
- [ ] T069 [CH5] Create lab5 instructions in physical-ai-book/docs/module2/labs/lab5/README.md

**Checkpoint**: Chapter 5 code tested and verified

---

## Phase 8: RAG Integration (Priority: P2)

**Goal**: Integrate Module 2 content with RAG chatbot

**Independent Test**: Chatbot answers Module 2 queries accurately with source citations

### Implementation for RAG

- [ ] T070 [P] [RAG] Run content chunking script on Module 2 chapters
- [ ] T071 [RAG] Verify ~500 chunks created with proper metadata
- [ ] T072 [P] [RAG] Generate embeddings with text-embedding-3-large
- [ ] T073 [RAG] Store embeddings in Qdrant collection
- [ ] T074 [RAG] Verify embedding count in Qdrant dashboard
- [ ] T075 [P] [RAG] Test RAG retrieval with query "What is a Digital Twin?"
- [ ] T076 [RAG] Verify relevant chunks retrieved with scores > 0.7
- [ ] T077 [RAG] Test RAG retrieval with query "How to install Gazebo?"
- [ ] T078 [RAG] Test RAG retrieval with query "Explain URDF vs SDF"
- [ ] T079 [RAG] Test RAG retrieval with query "How to add LiDAR sensor?"
- [ ] T080 [RAG] Test RAG retrieval with query "What is ROS#?"
- [ ] T081 [RAG] Test RAG retrieval with query "Sensor fusion with Kalman Filter"
- [ ] T082 [RAG] Measure retrieval accuracy (target: > 90%)
- [ ] T083 [RAG] Document RAG test results in physical-ai-book/backend/tests/rag_test_results.md

**Checkpoint**: RAG integration complete and tested

---

## Phase 9: Deployment (Priority: P1) 🎯 MVP

**Goal**: Deploy textbook with Module 2 content

**Independent Test**: Docusaurus site builds and deploys successfully, all links working

### Implementation for Deployment

- [ ] T084 [P] [DEPLOY] Run Docusaurus build in physical-ai-book/
- [ ] T085 [DEPLOY] Fix any build errors
- [ ] T086 [DEPLOY] Verify all Markdown files render correctly
- [ ] T087 [DEPLOY] Test navigation between chapters
- [ ] T088 [DEPLOY] Verify all code blocks have syntax highlighting
- [ ] T089 [DEPLOY] Test all internal links work
- [ ] T090 [DEPLOY] Test all external links work
- [ ] T091 [P] [DEPLOY] Setup GitHub Pages deployment
- [ ] T092 [DEPLOY] Configure GitHub Actions workflow in .github/workflows/deploy.yml
- [ ] T093 [DEPLOY] Deploy to GitHub Pages
- [ ] T094 [DEPLOY] Verify live site accessible
- [ ] T095 [DEPLOY] Test site on mobile devices
- [ ] T096 [DEPLOY] Test site on different browsers (Chrome, Firefox, Safari)
- [ ] T097 [DEPLOY] Create demo script for hackathon judges in docs/DEMO_SCRIPT.md
- [ ] T098 [DEPLOY] Record demo video (5 minutes)
- [ ] T099 [DEPLOY] Prepare hackathon presentation slides

**Checkpoint**: Module 2 deployed and ready for hackathon demo

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T100 [P] Create Module 2 overview page in physical-ai-book/docs/module2/README.md
- [ ] T101 [P] Create quickstart guide for Module 2 in physical-ai-book/docs/module2/QUICKSTART.md
- [ ] T102 [P] Create troubleshooting guide in physical-ai-book/docs/module2/TROUBLESHOOTING.md
- [ ] T103 [P] Add Mermaid diagrams to all chapters (if missing)
- [ ] T104 [P] Verify all learning objectives have corresponding exercises
- [ ] T105 [P] Add accessibility features (alt text for images, proper headings)
- [ ] T106 [P] Run spell check on all chapters
- [ ] T107 [P] Run grammar check on all chapters
- [ ] T108 [P] Verify RAG chatbot integration in sidebar
- [ ] T109 [P] Test chatbot with Module 2 queries on live site
- [ ] T110 [P] Create instructor guide in physical-ai-book/docs/module2/INSTRUCTOR_GUIDE.md
- [ ] T111 [P] Create student workbook in physical-ai-book/docs/module2/STUDENT_WORKBOOK.md
- [ ] T112 [P] Final review of all chapters
- [ ] T113 [P] Update main README with Module 2 completion status
- [ ] T114 [P] Create hackathon submission document

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS all code testing
- **Phase 3-7 (Code Testing)**: All depend on Phase 2 completion
  - Chapters can be tested in parallel (different code files)
  - Or sequentially in order (CH1 → CH2 → CH3 → CH4 → CH5)
- **Phase 8 (RAG)**: Depends on Phase 3-7 (content must be finalized)
- **Phase 9 (Deployment)**: Depends on Phase 7-8 (content + RAG ready)
- **Phase 10 (Polish)**: Depends on Phase 9 (deployment complete)

### Chapter Testing Dependencies

- **Chapter 1 (P1)**: Can start after Phase 2 - No dependencies on other chapters
- **Chapter 2 (P1)**: Can start after Phase 2 - Independent
- **Chapter 3 (P2)**: Can start after Phase 2 - Independent
- **Chapter 4 (P2)**: Can start after Phase 2 - Independent (but benefits from CH2)
- **Chapter 5 (P3)**: Can start after Phase 2 - Depends on CH2, CH3, CH4 concepts

### Within Each Chapter

- URDF/SDF creation before launch files
- Launch files before controller nodes
- Core scripts before integration tests
- Code testing before lab documentation

### Parallel Opportunities

- **Phase 1 (Setup)**: T001-T006 can all run in parallel
- **Phase 2 (Foundational)**: T007-T012 can mostly run in parallel
- **Phase 3-7 (Code Testing)**: All chapters can be tested in parallel by different team members
- **Phase 8 (RAG)**: T070, T072, T075 can run in parallel
- **Phase 9 (Deployment)**: T084-T090 can run in parallel, T091-T096 can run in parallel

---

## Parallel Example: Chapter 2 Testing

```bash
# Launch all URDF validation together:
Task: "Create simple_robot.urdf in physical-ai-book/docs/module2/code/chapter2/"
Task: "Validate URDF with check_urdf tool"

# Launch controller testing in parallel:
Task: "Create simple_controller.py"
Task: "Test controller publishes to /cmd_vel"

# Launch world testing in parallel:
Task: "Create gazebo_world.sdf with sensors"
Task: "Test launch file spawns robot in Gazebo"
```

---

## Parallel Example: RAG Integration

```bash
# Run chunking and embedding generation together:
Task: "Run content chunking script on Module 2 chapters"
Task: "Generate embeddings with text-embedding-3-large"

# Launch retrieval tests in parallel:
Task: "Test RAG retrieval with query 'What is a Digital Twin?'"
Task: "Test RAG retrieval with query 'How to install Gazebo?'"
Task: "Test RAG retrieval with query 'Explain URDF vs SDF'"
```

---

## Implementation Strategy

### MVP First (Phases 1-3 + Phase 9)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T012) - **CRITICAL BLOCKER**
3. Complete Phase 3: Chapter 1 Testing (T013-T019) - Basic simulation working
4. Complete Phase 9: Deployment (T084-T099) - Deploy with Chapter 1 only
5. **STOP and VALIDATE**: Test deployment with real users
6. Deploy MVP: Docusaurus site with Chapter 1

### Incremental Delivery

1. **Day 1-2**: Setup + Foundational → Foundation ready
2. **Day 3-4**: Chapter 1 Testing → Deploy Chapter 1 (MVP Part 1!)
3. **Day 5-6**: Chapter 2 Testing → Deploy Chapter 2
4. **Day 7-8**: Chapter 3 Testing → Deploy Chapter 3
5. **Day 9-10**: Chapter 4 Testing → Deploy Chapter 4
6. **Day 11-12**: Chapter 5 Testing → Deploy Chapter 5
7. **Day 13**: RAG Integration → Deploy with chatbot
8. **Day 14**: Polish + Hackathon Demo Prep

### Parallel Team Strategy

With multiple team members after Phase 2:

- **Developer A**: Chapter 2 + Chapter 3 testing
- **Developer B**: Chapter 4 + Chapter 5 testing
- **Developer C**: RAG Integration + Deployment
- **All**: Phase 10 Polish tasks

Once Foundational phase completes:
- All chapter testing can be worked on in parallel
- Each chapter is independently testable
- Merge and deploy chapters incrementally

---

## Task Summary

| Phase | Description | Task Count | Priority |
|-------|-------------|------------|----------|
| Phase 1 | Setup | 6 | N/A |
| Phase 2 | Foundational | 6 | N/A |
| Phase 3 | Chapter 1 Testing | 7 | P1 🎯 |
| Phase 4 | Chapter 2 Testing | 10 | P1 🎯 |
| Phase 5 | Chapter 3 Testing | 13 | P2 |
| Phase 6 | Chapter 4 Testing | 14 | P2 |
| Phase 7 | Chapter 5 Testing | 13 | P3 |
| Phase 8 | RAG Integration | 14 | P2 |
| Phase 9 | Deployment | 16 | P1 🎯 |
| Phase 10 | Polish | 15 | N/A |
| **Total** | | **114 tasks** | |

### MVP Scope (Minimum for Hackathon Demo)

- Phase 1: Setup (6 tasks)
- Phase 2: Foundational (6 tasks)
- Phase 3: Chapter 1 Testing (7 tasks) - Basic simulation working
- Phase 9: Deployment (16 tasks) - Site deployed

**MVP Total**: 35 tasks - Deployable textbook with Chapter 1

### Full Scope

All 114 tasks - Complete Module 2 with all chapters tested, RAG integrated, and deployed

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [CH1], [CH2], etc. = Chapter testing tasks for traceability
- [RAG] = RAG integration tasks
- [DEPLOY] = Deployment tasks
- Each chapter should be independently testable
- Commit after each task or logical group
- Stop at any checkpoint to validate chapter independently
- Avoid: vague tasks, same file conflicts, cross-chapter dependencies that break independence

---

## Quick Reference

### Key Commands

```bash
# Build Docusaurus
cd physical-ai-book && npm run build

# Test Gazebo simulation
gz sim chapter2/gazebo_world.sdf

# Test ROS2 launch
ros2 launch chapter2 gazebo_launch.py

# Generate embeddings
python backend/src/scripts/embed_textbook.py --input docs/module2/

# Test RAG retrieval
python backend/src/scripts/test_rag.py --queries test_queries.json
```

### Key Files

- **Chapters**: `physical-ai-book/docs/module2/chapter*.md`
- **Code**: `physical-ai-book/docs/module2/code/chapter*/`
- **Labs**: `physical-ai-book/docs/module2/labs/lab*/`
- **Backend**: `physical-ai-book/backend/src/`

### Key Contacts

- **Content Lead**: [Assign team member]
- **Testing Lead**: [Assign team member]
- **RAG Lead**: [Assign team member]
- **Deployment Lead**: [Assign team member]
