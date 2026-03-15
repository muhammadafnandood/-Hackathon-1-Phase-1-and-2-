# Tasks: Module 3 - AI Robot Brain (NVIDIA Isaac)

**Input**: Design documents from `specs/module3/`
**Prerequisites**: plan.md (required), spec.md (not applicable - content project), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - Code testing tasks included for validation of simulation examples.

**Organization**: Tasks are grouped by development phase (Setup → Foundational → Content Testing → RAG → Deployment) to enable incremental delivery.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Not applicable for this content project (phases used instead)
- Include exact file paths in descriptions

## Path Conventions

- **Documentation**: `physical-ai-book/docs/module3/`
- **Code Examples**: `physical-ai-book/docs/module3/code/`
- **Lab Files**: `physical-ai-book/docs/module3/labs/`
- **Backend**: `physical-ai-book/backend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment setup

- [X] T001 [P] Create code examples directory structure in physical-ai-book/docs/module3/code/chapter{1-5}/
- [X] T002 [P] Create lab files directory structure in physical-ai-book/docs/module3/labs/lab{1-5}/
- [ ] T003 [P] Verify NVIDIA GPU availability (CUDA 11.7+)
- [ ] T004 [P] Verify Isaac Sim 4.0+ installation
- [ ] T005 [P] Verify ROS2 Humble with Isaac ROS packages
- [X] T006 [P] Verify PyTorch 2.0+ with CUDA support in physical-ai-book/backend/requirements.txt

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before code testing

**⚠️ CRITICAL**: No code testing can begin until this phase is complete

- [X] T007 [P] Create example code template structure in physical-ai-book/docs/module3/code/README.md
- [X] T008 [P] Create lab template with instructions in physical-ai-book/docs/module3/labs/README.md
- [ ] T009 [P] Setup Isaac Gym environment in ~/isaacgym/
- [ ] T010 [P] Configure Qdrant Cloud connection in physical-ai-book/backend/.env
- [ ] T011 [P] Verify OpenAI API access for RAG embeddings
- [ ] T012 [P] Create content chunking script in physical-ai-book/backend/src/scripts/chunk_content.py

**Checkpoint**: Foundation ready - code testing can now begin

---

## Phase 3: Chapter 1 Code Testing (Priority: P1) 🎯 MVP

**Goal**: Test all code examples from Chapter 1 (NVIDIA Isaac Platform)

**Independent Test**: Isaac Sim launches, robot simulation runs, ROS2 bridge works

### Implementation for Chapter 1

- [ ] T013 [P] [CH1] Create Isaac Sim installation script in physical-ai-book/docs/module3/code/chapter1/install_isaac_sim.sh
- [ ] T014 [P] [CH1] Create isaac_sim_robot.py example in physical-ai-book/docs/module3/code/chapter1/isaac_sim_robot.py
- [ ] T015 [CH1] Test Isaac Sim launches without errors
- [ ] T016 [P] [CH1] Create bridge_config.py in physical-ai-book/docs/module3/code/chapter1/bridge_config.py
- [ ] T017 [CH1] Test ROS2 bridge configuration
- [ ] T018 [P] [CH1] Create isaac_ros2_launch.py in physical-ai-book/docs/module3/code/chapter1/isaac_ros2_launch.py
- [ ] T019 [CH1] Test launch file executes successfully
- [ ] T020 [CH1] Document troubleshooting steps in physical-ai-book/docs/module3/labs/lab1/TROUBLESHOOTING.md

**Checkpoint**: Chapter 1 code tested and verified

---

## Phase 4: Chapter 2 Code Testing (Priority: P2)

**Goal**: Test all code examples from Chapter 2 (Synthetic Data)

**Independent Test**: Synthetic data generation works, COCO export successful

### Implementation for Chapter 2

- [ ] T021 [P] [CH2] Create generate_data.py in physical-ai-book/docs/module3/code/chapter2/generate_data.py
- [ ] T022 [CH2] Test data generation script runs
- [ ] T023 [P] [CH2] Create randomization_config.py in physical-ai-book/docs/module3/code/chapter2/randomization_config.py
- [ ] T024 [CH2] Test domain randomization applies correctly
- [ ] T025 [P] [CH2] Create coco_exporter.py in physical-ai-book/docs/module3/code/chapter2/coco_exporter.py
- [ ] T026 [CH2] Test COCO format export
- [ ] T027 [CH2] Verify exported dataset is valid
- [ ] T028 [CH2] Create lab2 instructions in physical-ai-book/docs/module3/labs/lab2/README.md

**Checkpoint**: Chapter 2 code tested and verified

---

## Phase 5: Chapter 3 Code Testing (Priority: P2)

**Goal**: Test all code examples from Chapter 3 (Visual SLAM)

**Independent Test**: VSLAM runs, trajectory published, map generated

### Implementation for Chapter 3

- [ ] T029 [P] [CH3] Create visual_slam_launch.py in physical-ai-book/docs/module3/code/chapter3/visual_slam_launch.py
- [ ] T030 [CH3] Test Visual SLAM launch file
- [ ] T031 [P] [CH3] Create vslam_integrator.py in physical-ai-book/docs/module3/code/chapter3/vslam_integrator.py
- [ ] T032 [CH3] Test VSLAM integrator node
- [ ] T033 [CH3] Verify trajectory published to /trajectory
- [ ] T034 [P] [CH3] Create sensor_fusion_ekf.py in physical-ai-book/docs/module3/code/chapter3/sensor_fusion_ekf.py
- [ ] T035 [CH3] Test EKF sensor fusion
- [ ] T036 [CH3] Verify state estimation accuracy
- [ ] T037 [CH3] Create lab3 instructions in physical-ai-book/docs/module3/labs/lab3/README.md

**Checkpoint**: Chapter 3 code tested and verified

---

## Phase 6: Chapter 4 Code Testing (Priority: P1)

**Goal**: Test all code examples from Chapter 4 (Nav2 Navigation)

**Independent Test**: Nav2 navigation works, robot reaches goals, obstacles avoided

### Implementation for Chapter 4

- [ ] T038 [P] [CH4] Create nav2_config_humanoid.yaml in physical-ai-book/docs/module3/code/chapter4/nav2_config_humanoid.yaml
- [ ] T039 [CH4] Validate Nav2 configuration
- [ ] T040 [P] [CH4] Create nav2_launch.py in physical-ai-book/docs/module3/code/chapter4/nav2_launch.py
- [ ] T041 [CH4] Test Nav2 launch file
- [ ] T042 [CH4] Verify map server loads correctly
- [ ] T043 [CH4] Verify AMCL localization works
- [ ] T044 [P] [CH4] Create nav2_goal_publisher.py in physical-ai-book/docs/module3/code/chapter4/nav2_goal_publisher.py
- [ ] T045 [CH4] Test goal publisher sends goals
- [ ] T046 [CH4] Test robot navigates to goal
- [ ] T047 [CH4] Test obstacle avoidance
- [ ] T048 [CH4] Create lab4 instructions in physical-ai-book/docs/module3/labs/lab4/README.md

**Checkpoint**: Chapter 4 code tested and verified

---

## Phase 7: Chapter 5 Code Testing (Priority: P3)

**Goal**: Test all code examples from Chapter 5 (Reinforcement Learning)

**Independent Test**: RL training converges, policy walks, sim-to-real works

### Implementation for Chapter 5

- [ ] T049 [P] [CH5] Create train_rl.py in physical-ai-book/docs/module3/code/chapter5/train_rl.py
- [ ] T050 [CH5] Test RL training script starts
- [ ] T051 [CH5] Test PPO training converges (reward > 50)
- [ ] T052 [CH5] Verify policy checkpoint saved
- [ ] T053 [P] [CH5] Create policy_deploy.py in physical-ai-book/docs/module3/code/chapter5/policy_deploy.py
- [ ] T054 [CH5] Test policy deployment script
- [ ] T055 [CH5] Test policy executes on robot
- [ ] T056 [P] [CH5] Create sim_to_real.py in physical-ai-book/docs/module3/code/chapter5/sim_to_real.py
- [ ] T057 [CH5] Test sim-to-real transfer script
- [ ] T058 [CH5] Create lab5 instructions in physical-ai-book/docs/module3/labs/lab5/README.md

**Checkpoint**: Chapter 5 code tested and verified

---

## Phase 8: RAG Integration (Priority: P2)

**Goal**: Integrate Module 3 content with RAG chatbot

**Independent Test**: Chatbot answers Module 3 queries accurately with source citations

### Implementation for RAG

- [ ] T059 [P] [RAG] Run content chunking script on Module 3 chapters
- [ ] T060 [RAG] Verify ~500 chunks created with proper metadata
- [ ] T061 [P] [RAG] Generate embeddings with text-embedding-3-large
- [ ] T062 [RAG] Store embeddings in Qdrant collection
- [ ] T063 [RAG] Verify embedding count in Qdrant dashboard
- [ ] T064 [P] [RAG] Test RAG retrieval with query "What is Isaac Sim?"
- [ ] T065 [RAG] Verify relevant chunks retrieved with scores > 0.7
- [ ] T066 [RAG] Test RAG retrieval with query "How to generate synthetic data?"
- [ ] T067 [RAG] Test RAG retrieval with query "Explain Visual SLAM"
- [ ] T068 [RAG] Test RAG retrieval with query "How to configure Nav2?"
- [ ] T069 [RAG] Test RAG retrieval with query "What is PPO algorithm?"
- [ ] T070 [RAG] Test RAG retrieval with query "How to train walking policy?"
- [ ] T071 [RAG] Measure retrieval accuracy (target: > 90%)
- [ ] T072 [RAG] Document RAG test results in physical-ai-book/backend/tests/rag_test_results.md

**Checkpoint**: RAG integration complete and tested

---

## Phase 9: Deployment (Priority: P1) 🎯 MVP

**Goal**: Deploy textbook with Module 3 content

**Independent Test**: Docusaurus site builds and deploys successfully, all links working

### Implementation for Deployment

- [ ] T073 [P] [DEPLOY] Run Docusaurus build in physical-ai-book/
- [ ] T074 [DEPLOY] Fix any build errors
- [ ] T075 [DEPLOY] Verify all Markdown files render correctly
- [ ] T076 [DEPLOY] Test navigation between chapters
- [ ] T077 [DEPLOY] Verify all code blocks have syntax highlighting
- [ ] T078 [DEPLOY] Test all internal links work
- [ ] T079 [DEPLOY] Test all external links work
- [ ] T080 [P] [DEPLOY] Setup GitHub Pages deployment
- [ ] T081 [DEPLOY] Configure GitHub Actions workflow in .github/workflows/deploy.yml
- [ ] T082 [DEPLOY] Deploy to GitHub Pages
- [ ] T083 [DEPLOY] Verify live site accessible
- [ ] T084 [DEPLOY] Test site on mobile devices
- [ ] T085 [DEPLOY] Test site on different browsers (Chrome, Firefox, Safari)
- [ ] T086 [DEPLOY] Create demo script for hackathon judges in docs/DEMO_SCRIPT.md
- [ ] T087 [DEPLOY] Record demo video (5 minutes)
- [ ] T088 [DEPLOY] Prepare hackathon presentation slides

**Checkpoint**: Module 3 deployed and ready for hackathon demo

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T089 [P] Create Module 3 overview page in physical-ai-book/docs/module3/README.md
- [ ] T090 [P] Create quickstart guide for Module 3 in physical-ai-book/docs/module3/QUICKSTART.md
- [ ] T091 [P] Create troubleshooting guide in physical-ai-book/docs/module3/TROUBLESHOOTING.md
- [ ] T092 [P] Add Mermaid diagrams to all chapters (if missing)
- [ ] T093 [P] Verify all learning objectives have corresponding exercises
- [ ] T094 [P] Add accessibility features (alt text for images, proper headings)
- [ ] T095 [P] Run spell check on all chapters
- [ ] T096 [P] Run grammar check on all chapters
- [ ] T097 [P] Verify RAG chatbot integration in sidebar
- [ ] T098 [P] Test chatbot with Module 3 queries on live site
- [ ] T099 [P] Create instructor guide in physical-ai-book/docs/module3/INSTRUCTOR_GUIDE.md
- [ ] T100 [P] Create student workbook in physical-ai-book/docs/module3/STUDENT_WORKBOOK.md
- [ ] T101 [P] Final review of all chapters
- [ ] T102 [P] Update main README with Module 3 completion status
- [ ] T103 [P] Create hackathon submission document

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
- **Chapter 2 (P2)**: Can start after Phase 2 - Independent
- **Chapter 3 (P2)**: Can start after Phase 2 - Independent
- **Chapter 4 (P1)**: Can start after Phase 2 - Independent (but benefits from CH1)
- **Chapter 5 (P3)**: Can start after Phase 2 - Depends on CH1, CH2 concepts

### Within Each Chapter

- Installation scripts before simulation examples
- Simulation examples before integration nodes
- Core scripts before lab documentation
- Code testing before RAG integration

### Parallel Opportunities

- **Phase 1 (Setup)**: T001-T006 can all run in parallel
- **Phase 2 (Foundational)**: T007-T012 can mostly run in parallel
- **Phase 3-7 (Code Testing)**: All chapters can be tested in parallel by different team members
- **Phase 8 (RAG)**: T059, T061, T064 can run in parallel
- **Phase 9 (Deployment)**: T073-T079 can run in parallel, T080-T085 can run in parallel

---

## Parallel Example: Chapter 1 Testing

```bash
# Launch all installation scripts together:
Task: "Create Isaac Sim installation script"
Task: "Create isaac_sim_robot.py example"

# Launch bridge testing in parallel:
Task: "Create bridge_config.py"
Task: "Test ROS2 bridge configuration"

# Launch launch file testing in parallel:
Task: "Create isaac_ros2_launch.py"
Task: "Test launch file executes successfully"
```

---

## Parallel Example: RAG Integration

```bash
# Run chunking and embedding generation together:
Task: "Run content chunking script on Module 3 chapters"
Task: "Generate embeddings with text-embedding-3-large"

# Launch retrieval tests in parallel:
Task: "Test RAG retrieval with query 'What is Isaac Sim?'"
Task: "Test RAG retrieval with query 'How to generate synthetic data?'"
Task: "Test RAG retrieval with query 'Explain Visual SLAM'"
```

---

## Implementation Strategy

### MVP First (Phases 1-4 + Phase 9)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T012) - **CRITICAL BLOCKER**
3. Complete Phase 3: Chapter 1 Testing (T013-T020) - Isaac Sim working
4. Complete Phase 4: Chapter 4 Testing (T038-T048) - Nav2 navigation working
5. Complete Phase 9: Deployment (T073-T088) - Deploy with Chapters 1 & 4
6. **STOP and VALIDATE**: Test deployment with real users
7. Deploy MVP: Docusaurus site with Isaac Sim + Nav2 content

### Incremental Delivery

1. **Day 1-2**: Setup + Foundational → Foundation ready
2. **Day 3-4**: Chapter 1 Testing → Deploy Chapter 1 (MVP Part 1!)
3. **Day 5-6**: Chapter 4 Testing → Deploy Chapter 4 (MVP Part 2!)
4. **Day 7-8**: Chapter 2 Testing → Deploy Chapter 2
5. **Day 9-10**: Chapter 3 Testing → Deploy Chapter 3
6. **Day 11-12**: Chapter 5 Testing → Deploy Chapter 5
7. **Day 13**: RAG Integration → Deploy with chatbot
8. **Day 14**: Polish + Hackathon Demo Prep

### Parallel Team Strategy

With multiple team members after Phase 2:

- **Developer A**: Chapter 1 + Chapter 2 testing
- **Developer B**: Chapter 3 + Chapter 4 testing
- **Developer C**: Chapter 5 + RAG Integration
- **All**: Phase 9 Deployment + Phase 10 Polish

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
| Phase 3 | Chapter 1 Testing | 8 | P1 🎯 |
| Phase 4 | Chapter 2 Testing | 8 | P2 |
| Phase 5 | Chapter 3 Testing | 9 | P2 |
| Phase 6 | Chapter 4 Testing | 11 | P1 🎯 |
| Phase 7 | Chapter 5 Testing | 10 | P3 |
| Phase 8 | RAG Integration | 14 | P2 |
| Phase 9 | Deployment | 16 | P1 🎯 |
| Phase 10 | Polish | 15 | N/A |
| **Total** | | **103 tasks** | |

### MVP Scope (Minimum for Hackathon Demo)

- Phase 1: Setup (6 tasks)
- Phase 2: Foundational (6 tasks)
- Phase 3: Chapter 1 Testing (8 tasks) - Isaac Sim working
- Phase 6: Chapter 4 Testing (11 tasks) - Nav2 working
- Phase 9: Deployment (16 tasks) - Site deployed

**MVP Total**: 47 tasks - Deployable textbook with Isaac Sim + Nav2 content

### Full Scope

All 103 tasks - Complete Module 3 with all chapters tested, RAG integrated, and deployed

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

# Test Isaac Sim
python3 docs/module3/code/chapter1/isaac_sim_robot.py

# Test Nav2
ros2 launch chapter4 nav2_launch.py

# Generate embeddings
python backend/src/scripts/embed_textbook.py --input docs/module3/

# Test RAG retrieval
python backend/src/scripts/test_rag.py --queries test_queries.json
```

### Key Files

- **Chapters**: `physical-ai-book/docs/module3/chapter*.md`
- **Code**: `physical-ai-book/docs/module3/code/chapter*/`
- **Labs**: `physical-ai-book/docs/module3/labs/lab*/`
- **Backend**: `physical-ai-book/backend/src/`

### Key Contacts

- **Content Lead**: [Assign team member]
- **Testing Lead**: [Assign team member]
- **RAG Lead**: [Assign team member]
- **Deployment Lead**: [Assign team member]
