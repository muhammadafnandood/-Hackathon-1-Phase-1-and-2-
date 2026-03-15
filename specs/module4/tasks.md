# Tasks: Module 4 - Vision-Language-Action (VLA) Robotics with Enhanced Docusaurus UI

**Input**: Design documents from `specs/module4/`
**Prerequisites**: plan.md (required), spec.md (reference), research.md (optional)

**Tests**: Tests are **OPTIONAL** for this UI-focused feature. Only include functional validation tasks in Phase 5.

**Organization**: Tasks are grouped by **implementation phase** (components → content → styling → RAG → testing → deployment) to enable incremental delivery and validation.

## Format: `[ID] [P?] [Phase] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Phase]**: Which phase this task belongs to (e.g., PH1, PH2, PH3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `physical-ai-book/` (Docusaurus app)
- **Components**: `physical-ai-book/src/components/mdx/`
- **Chapters**: `physical-ai-book/docs/module4/`
- **Styles**: `physical-ai-book/src/css/`

---

## Phase 1: Research & Component Design (2-3 days)

**Purpose**: Understand Docusaurus MDX capabilities and design component API

**⚠️ CRITICAL**: This phase informs all subsequent component implementation

- [X] T001 [P] Research Docusaurus MDX component patterns and best practices
- [X] T002 [P] Design component API (props, children, styling) for tabs, collapsibles, admonitions
- [X] T003 Create component prototypes (minimal viable components)
- [X] T004 [P] Test components in isolation (create test MDX file)
- [X] T005 Document component usage with examples in `specs/module4/component-api.md`

**Checkpoint**: Component API documented and prototypes validated

---

## Phase 2: Component Library Implementation (3-4 days) 🎯 Foundation

**Purpose**: Build complete MDX component library (15+ components)

**⚠️ CRITICAL**: All chapter migrations (Phase 3) depend on this phase

### 2.1 Tab Components

- [X] T006 [P] [PH2] Create `<TabGroup>` wrapper with state persistence in `physical-ai-book/src/components/mdx/Tabs/TabGroup.tsx`
- [X] T007 [P] [PH2] Create `<TabItem>` with icon support in `physical-ai-book/src/components/mdx/Tabs/TabItem.tsx`
- [X] T008 [PH2] Implement tab keyboard navigation (accessibility) in `physical-ai-book/src/components/mdx/Tabs/TabGroup.tsx`
- [X] T009 [PH2] Add tab URL hash synchronization (deep linking) in `physical-ai-book/src/components/mdx/Tabs/TabGroup.tsx`
- [X] T010 [PH2] Style tabs with robotics theme (colors, animations) in `physical-ai-book/src/css/custom.css`

### 2.2 Collapsible Components

- [X] T011 [P] [PH2] Create `<CollapsibleSection>` with smooth animations in `physical-ai-book/src/components/mdx/Collapsible/CollapsibleSection.tsx`
- [X] T012 [P] [PH2] Create `<CodeCollapsible>` for hideable code in `physical-ai-book/src/components/mdx/Collapsible/CodeCollapsible.tsx`
- [X] T013 [PH2] Add "Expand All" / "Collapse All" controls in `physical-ai-book/src/components/mdx/Collapsible/CollapsibleSection.tsx`
- [X] T014 [PH2] Implement collapsible state persistence in `physical-ai-book/src/components/mdx/Collapsible/CollapsibleSection.tsx`
- [X] T015 [PH2] Style with custom icons and hover effects in `physical-ai-book/src/css/custom.css`

### 2.3 Admonition Components

- [X] T016 [P] [PH2] Create `<TipAdmonition>` with lightbulb icon in `physical-ai-book/src/components/mdx/Admonition/TipAdmonition.tsx`
- [X] T017 [P] [PH2] Create `<WarningAdmonition>` with caution icon in `physical-ai-book/src/components/mdx/Admonition/WarningAdmonition.tsx`
- [X] T018 [P] [PH2] Create `<NoteAdmonition>` with info icon in `physical-ai-book/src/components/mdx/Admonition/NoteAdmonition.tsx`
- [X] T019 [P] [PH2] Create `<SafetyAdmonition>` with safety-critical styling in `physical-ai-book/src/components/mdx/Admonition/SafetyAdmonition.tsx`
- [X] T020 [PH2] Add custom admonition types via props in `physical-ai-book/src/components/mdx/Admonition/index.tsx`

### 2.4 Lab Components

- [X] T021 [P] [PH2] Create `<LabBox>` container with lab styling in `physical-ai-book/src/components/mdx/Lab/LabBox.tsx`
- [X] T022 [P] [PH2] Create `<ObjectiveList>` for learning objectives in `physical-ai-book/src/components/mdx/Lab/ObjectiveList.tsx`
- [X] T023 [PH2] Add lab duration and difficulty badges in `physical-ai-book/src/components/mdx/Lab/LabBox.tsx`
- [X] T024 [PH2] Implement lab checklist component in `physical-ai-book/src/components/mdx/Lab/LabBox.tsx`
- [X] T025 [PH2] Add simulation vs hardware toggle in `physical-ai-book/src/components/mdx/Lab/LabBox.tsx`

### 2.5 Diagram Components

- [X] T026 [P] [PH2] Create `<MermaidDiagram>` with auto-rendering in `physical-ai-book/src/components/mdx/Diagram/MermaidDiagram.tsx`
- [X] T027 [P] [PH2] Create `<ArchitectureDiagram>` with zoom/pan in `physical-ai-book/src/components/mdx/Diagram/ArchitectureDiagram.tsx`
- [X] T028 [PH2] Add dark mode support for diagrams in `physical-ai-book/src/components/mdx/Diagram/MermaidDiagram.tsx`
- [X] T029 [PH2] Implement diagram download (PNG/SVG) in `physical-ai-book/src/components/mdx/Diagram/ArchitectureDiagram.tsx`
- [X] T030 [PH2] Add interactive diagram elements in `physical-ai-book/src/components/mdx/Diagram/ArchitectureDiagram.tsx`

### 2.6 Component Exports & Registration

- [X] T031 [P] [PH2] Create component index exports in `physical-ai-book/src/components/mdx/index.ts`
- [X] T032 [PH2] Register custom MDX components in `physical-ai-book/src/theme/MDXComponents.js`
- [X] T033 [PH2] Override default admonitions in `physical-ai-book/src/theme/Admonition.js`
- [X] T034 [PH2] Add component usage documentation in `docs/components/README.md`

**Checkpoint**: All 15+ components implemented, exported, and registered

---

## Phase 3: Chapter Content Migration (4-5 days) 🎯 Core Content

**Purpose**: Convert existing Markdown chapters to MDX with interactive components

**Note**: Each chapter can be migrated **independently** and in **parallel** (different files)

### 3.1 Chapter 1: LLMs in Robotics

- [ ] T035 [P] [PH3] [CH1] Convert chapter1 from `.md` to `.mdx` format: `physical-ai-book/docs/module4/chapter1-llm-robotics.mdx`
- [ ] T036 [PH3] [CH1] Add tab groups for Concept/Example/Lab sections in `chapter1-llm-robotics.mdx`
- [ ] T037 [PH3] [CH1] Add collapsible advanced topics (prompt engineering deep-dive) in `chapter1-llm-robotics.mdx`
- [ ] T038 [PH3] [CH1] Add tip admonitions for best practices in `chapter1-llm-robotics.mdx`
- [ ] T039 [PH3] [CH1] Add architecture diagrams for LLM-robot bridge in `chapter1-llm-robotics.mdx`
- [ ] T040 [PH3] [CH1] Add safety admonitions for LLM reliability in `chapter1-llm-robotics.mdx`

**Interactive Elements Count**: 4+ tab groups, 6+ collapsibles, 8+ admonitions, 1+ lab box, 2+ diagrams

### 3.2 Chapter 2: Voice-to-Action Commands

- [ ] T041 [P] [PH3] [CH2] Convert chapter2 from `.md` to `.mdx` format: `physical-ai-book/docs/module4/chapter2-voice-to-action.mdx`
- [ ] T042 [PH3] [CH2] Add tab groups for Theory/Lab/Sample Scripts in `chapter2-voice-to-action.mdx`
- [ ] T043 [PH3] [CH2] Add collapsible Whisper configuration details in `chapter2-voice-to-action.mdx`
- [ ] T044 [PH3] [CH2] Add tip admonitions for noise cancellation in `chapter2-voice-to-action.mdx`
- [ ] T045 [PH3] [CH2] Add workflow diagrams for voice processing pipeline in `chapter2-voice-to-action.mdx`
- [ ] T046 [PH3] [CH2] Add warning admonitions for speech recognition errors in `chapter2-voice-to-action.mdx`

**Interactive Elements Count**: 4+ tab groups, 6+ collapsibles, 8+ admonitions, 1+ lab box, 2+ diagrams

### 3.3 Chapter 3: Cognitive Planning

- [ ] T047 [P] [PH3] [CH3] Convert chapter3 from `.md` to `.mdx` format: `physical-ai-book/docs/module4/chapter3-cognitive-planning.mdx`
- [ ] T048 [PH3] [CH3] Add tab groups for Theory/Example/Lab/Exercises in `chapter3-cognitive-planning.mdx`
- [ ] T049 [PH3] [CH3] Add collapsible task decomposition algorithms in `chapter3-cognitive-planning.mdx`
- [ ] T050 [PH3] [CH3] Add tip admonitions for planning efficiency in `chapter3-cognitive-planning.mdx`
- [ ] T051 [PH3] [CH3] Add flow diagrams for cognitive architecture in `chapter3-cognitive-planning.mdx`
- [ ] T052 [PH3] [CH3] Add expandable exercises section in `chapter3-cognitive-planning.mdx`

**Interactive Elements Count**: 4+ tab groups, 6+ collapsibles, 8+ admonitions, 1+ lab box, 2+ diagrams

### 3.4 Chapter 4: Multimodal Interaction

- [ ] T053 [P] [PH3] [CH4] Convert chapter4 from `.md` to `.mdx` format: `physical-ai-book/docs/module4/chapter4-multimodal-interaction.mdx`
- [ ] T054 [PH3] [CH4] Add tab groups for Speech/Vision/Gesture in `chapter4-multimodal-interaction.mdx`
- [ ] T055 [PH3] [CH4] Add collapsible sensor fusion algorithms in `chapter4-multimodal-interaction.mdx`
- [ ] T056 [PH3] [CH4] Add tip admonitions for calibration in `chapter4-multimodal-interaction.mdx`
- [ ] T057 [PH3] [CH4] Add architecture diagrams for multimodal system in `chapter4-multimodal-interaction.mdx`
- [ ] T058 [PH3] [CH4] Add safety admonitions for sensor failures in `chapter4-multimodal-interaction.mdx`

**Interactive Elements Count**: 4+ tab groups, 6+ collapsibles, 8+ admonitions, 1+ lab box, 2+ diagrams

### 3.5 Chapter 5: Conversational Robotics

- [ ] T059 [P] [PH3] [CH5] Convert chapter5 from `.md` to `.mdx` format: `physical-ai-book/docs/module4/chapter5-conversational-robotics.mdx`
- [ ] T060 [PH3] [CH5] Add tab groups for Concept/Example/Lab/Exercises in `chapter5-conversational-robotics.mdx`
- [ ] T061 [PH3] [CH5] Add collapsible dialogue state management in `chapter5-conversational-robotics.mdx`
- [ ] T062 [PH3] [CH5] Add tip admonitions for context retention in `chapter5-conversational-robotics.mdx`
- [ ] T063 [PH3] [CH5] Add multi-turn dialogue examples (collapsible) in `chapter5-conversational-robotics.mdx`
- [ ] T064 [PH3] [CH5] Add best practices admonitions in `chapter5-conversational-robotics.mdx`

**Interactive Elements Count**: 4+ tab groups, 6+ collapsibles, 8+ admonitions, 1+ lab box, 2+ diagrams

### 3.6 Chapter-Specific Components (Optional Enhancements)

- [ ] T065 [P] [PH3] Create VoiceCommandDemo component in `physical-ai-book/docs/module4/_components/VoiceCommandDemo.tsx`
- [ ] T066 [PH3] Create PlanningFlowDiagram component in `physical-ai-book/docs/module4/_components/PlanningFlowDiagram.tsx`
- [ ] T067 [PH3] Create DialogueExample component in `physical-ai-book/docs/module4/_components/DialogueExample.tsx`

**Checkpoint**: All 5 chapters migrated with interactive elements

---

## Phase 4: Styling & Polish (2-3 days)

**Purpose**: Apply consistent, beautiful styling to all interactive elements

### 4.1 CSS Enhancements

- [X] T068 [P] [PH4] Create tab animations (slide, fade) in `physical-ai-book/src/css/custom.css`
- [X] T069 [PH4] Style collapsible headers with hover effects in `physical-ai-book/src/css/custom.css`
- [X] T070 [PH4] Add gradient backgrounds to admonitions in `physical-ai-book/src/css/custom.css`
- [X] T071 [PH4] Create lab box distinctive styling in `physical-ai-book/src/css/custom.css`
- [X] T072 [PH4] Add responsive breakpoints for mobile in `physical-ai-book/src/css/custom.css`
- [X] T073 [PH4] Implement dark mode for all components in `physical-ai-book/src/css/custom.css`
- [X] T074 [PH4] Add loading states for async content in `physical-ai-book/src/css/custom.css`
- [X] T075 [PH4] Create print styles for PDF export in `physical-ai-book/src/css/custom.css`

### 4.2 Accessibility

- [ ] T076 [P] [PH4] Add ARIA labels to all interactive elements in component files
- [ ] T077 [PH4] Implement keyboard navigation for tabs in `physical-ai-book/src/components/mdx/Tabs/TabGroup.tsx`
- [ ] T078 [PH4] Add screen reader announcements for state changes in component files
- [ ] T079 [PH4] Ensure color contrast meets WCAG AA in `physical-ai-book/src/css/custom.css`
- [ ] T080 [PH4] Add focus indicators for all interactive elements in `physical-ai-book/src/css/custom.css`
- [ ] T081 [PH4] Test with NVDA/JAWS screen readers (manual testing)

**Checkpoint**: All components styled and accessible

---

## Phase 5: Testing & Validation (2 days)

**Purpose**: Ensure all components work correctly across browsers and devices

### 5.1 Functional Testing

- [ ] T082 [P] [PH5] Test tab switching in Chrome, Firefox, Safari, Edge
- [ ] T083 [PH5] Test collapsible animations and state persistence
- [ ] T084 [PH5] Test admonition rendering in light/dark mode
- [ ] T085 [PH5] Test lab box checklists functionality
- [ ] T086 [PH5] Test diagram rendering and interactivity
- [ ] T087 [PH5] Test mobile responsiveness (iOS Safari, Android Chrome)

### 5.2 Code Validation

- [ ] T088 [P] [PH5] Verify all Python code examples are runnable (spot check 5+ examples)
- [ ] T089 [PH5] Verify ROS2 node examples have correct imports
- [ ] T090 [PH5] Validate YAML launch file syntax
- [ ] T091 [PH5] Check Python type hints and docstrings

### 5.3 User Testing

- [ ] T092 [P] [PH5] Recruit 3-5 beta testers (students/peers)
- [ ] T093 [PH5] Collect feedback on navigation and usability
- [ ] T094 [PH5] Measure task completion time (find specific content)
- [ ] T095 [PH5] Identify confusing sections and unclear instructions
- [ ] T096 [PH5] Iterate based on feedback (fix top 3 issues)

**Checkpoint**: All tests pass, user feedback incorporated

---

## Phase 6: RAG Chatbot Integration (2 days)

**Purpose**: Ensure all tab/section content is retrievable by RAG chatbot

- [ ] T097 [P] [PH6] Add metadata to each tab for embedding in component files (`data-chapter`, `data-section`, `data-type`)
- [ ] T098 [PH6] Create content chunking strategy for MDX in `backend/src/scripts/chunk_mdx_content.py`
- [ ] T099 [PH6] Index tab content separately in Qdrant in `backend/src/services/qdrant_service.py`
- [ ] T100 [PH6] Add chapter context to chatbot queries in `backend/src/api/chat.py`
- [ ] T101 [PH6] Test RAG retrieval with tabbed content (manual testing)
- [ ] T102 [PH6] Verify source citations include tab references in chatbot responses

**Checkpoint**: RAG chatbot can retrieve and cite tabbed content

---

## Phase 7: Deployment & Demo (1-2 days) 🎯 Final

**Purpose**: Deploy Module 4 and prepare demo for hackathon judges

### 7.1 Deployment

- [ ] T103 [P] [PH7] Build Docusaurus site (`npm run build`) in `physical-ai-book/`
- [ ] T104 [PH7] Deploy to GitHub Pages via GitHub Actions
- [ ] T105 [PH7] Verify all links and assets load correctly
- [ ] T106 [PH7] Test production build performance (Lighthouse score)
- [ ] T107 [PH7] Setup analytics tracking (Google Analytics or Vercel Analytics)

### 7.2 Demo Preparation

- [ ] T108 [P] [PH7] Create demo script for judges in `docs/demo/README.md`
- [ ] T109 [PH7] Record demo video (backup) and upload to YouTube/unlisted
- [ ] T110 [PH7] Prepare talking points:
  - Interactive tabs improve learning
  - Collapsible sections handle complexity
  - Admonitions highlight critical info
  - Modern UI engages students
- [ ] T111 [PH7] Test live demo on presentation machine
- [ ] T112 [PH7] Create backup offline version (PDF export)

**Checkpoint**: Module 4 live and demo-ready

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple phases

- [ ] T113 [P] [PH8] Create API documentation for MDX components in `docs/components/api.md`
- [ ] T114 [PH8] Add component Storybook or usage examples in `docs/components/examples.md`
- [ ] T115 [PH8] Code cleanup and refactoring across all components
- [ ] T116 [PH8] Performance optimization (lazy load tab content, optimize animations)
- [ ] T117 [PH8] Security hardening (sanitize MDX content, prevent XSS)
- [ ] T118 [PH8] Run quickstart.md validation and fix any issues
- [ ] T119 [PH8] Final documentation review and cleanup
- [ ] T120 [PH8] Create migration guide for other modules to use MDX components

**Checkpoint**: Production-ready, documented, optimized

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Research)**: No dependencies - can start immediately
- **Phase 2 (Components)**: Depends on Phase 1 research completion - **BLOCKS all chapter migrations**
- **Phase 3 (Content)**: Depends on Phase 2 component completion - chapters can be done in parallel
- **Phase 4 (Styling)**: Can run parallel with Phase 3 (incremental styling as components are ready)
- **Phase 5 (Testing)**: Depends on Phase 3+4 completion
- **Phase 6 (RAG)**: Depends on Phase 3 content completion
- **Phase 7 (Deployment)**: Depends on Phase 5 testing pass
- **Phase 8 (Polish)**: Depends on all previous phases

### Critical Path

```
Phase 1 → Phase 2 → Phase 3 → Phase 5 → Phase 7
              ↓           ↓           ↓
          Phase 4     Phase 6     Phase 8
```

**Total Duration**: 15-19 days (sequential), 12-14 days (with parallel work)

### Parallel Opportunities

#### Within Phase 2 (Components)
- **Tab components** (T006-T010): All 5 tasks can run in parallel (different files)
- **Collapsible components** (T011-T015): All 5 tasks can run in parallel
- **Admonition components** (T016-T020): All 5 tasks can run in parallel
- **Lab components** (T021-T025): All 5 tasks can run in parallel
- **Diagram components** (T026-T030): All 5 tasks can run in parallel

#### Within Phase 3 (Content Migration)
- **All 5 chapters** (T035-T067) can be migrated **in parallel** (different files)
- Recommended: Assign each chapter to a different team member

#### Within Phase 4 (Styling)
- **CSS enhancements** (T068-T075): All 8 tasks can run in parallel
- **Accessibility** (T076-T081): Can run parallel with CSS after components are ready

#### Within Phase 5 (Testing)
- **Functional testing** (T082-T087): Can split by browser/device
- **Code validation** (T088-T091): Can split by chapter/example type
- **User testing** (T092-T096): Sequential (recruit → test → iterate)

#### Within Phase 6 (RAG)
- **Metadata + chunking** (T097-T098): Can run in parallel
- **Indexing + queries** (T099-T100): Can run in parallel after T097-T098
- **Testing** (T101-T102): Sequential after implementation

#### Within Phase 7 (Deployment)
- **Deployment** (T103-T107): Mostly sequential
- **Demo prep** (T108-T112): Can run parallel with deployment

---

## Parallel Execution Examples

### Example 1: Component Library (Phase 2)

```bash
# Launch all component types in parallel:
Task: "Create TabGroup in src/components/mdx/Tabs/TabGroup.tsx"
Task: "Create CollapsibleSection in src/components/mdx/Collapsible/CollapsibleSection.tsx"
Task: "Create TipAdmonition in src/components/mdx/Admonition/TipAdmonition.tsx"
Task: "Create LabBox in src/components/mdx/Lab/LabBox.tsx"
Task: "Create MermaidDiagram in src/components/mdx/Diagram/MermaidDiagram.tsx"
```

### Example 2: Chapter Migration (Phase 3)

```bash
# Launch all chapter migrations in parallel:
Task: "Convert chapter1 to MDX in docs/module4/chapter1-llm-robotics.mdx"
Task: "Convert chapter2 to MDX in docs/module4/chapter2-voice-to-action.mdx"
Task: "Convert chapter3 to MDX in docs/module4/chapter3-cognitive-planning.mdx"
Task: "Convert chapter4 to MDX in docs/module4/chapter4-multimodal-interaction.mdx"
Task: "Convert chapter5 to MDX in docs/module4/chapter5-conversational-robotics.mdx"
```

### Example 3: Styling (Phase 4)

```bash
# Launch all styling tasks in parallel:
Task: "Create tab animations in src/css/custom.css"
Task: "Style collapsible headers in src/css/custom.css"
Task: "Add gradient backgrounds to admonitions in src/css/custom.css"
Task: "Create lab box styling in src/css/custom.css"
Task: "Add responsive breakpoints in src/css/custom.css"
```

---

## Implementation Strategy

### MVP First (Core Components + Chapter 1 Only)

1. Complete Phase 1: Research (T001-T005)
2. Complete Phase 2: Components (T006-T034) - **CRITICAL BLOCKER**
3. Complete Phase 3: Chapter 1 ONLY (T035-T040)
4. **STOP and VALIDATE**: Test Chapter 1 with interactive elements
5. Deploy MVP: Single chapter showcasing all MDX components

### Incremental Delivery

1. **Days 1-3**: Phase 1 + Phase 2 → Component library ready
2. **Days 4-5**: Chapter 1 migration → Test/validate → Demo (MVP!)
3. **Days 6-10**: Chapters 2-5 migration (parallel) → All content ready
4. **Days 11-12**: Phase 4 styling → Polish UI
5. **Days 13-14**: Phase 5 testing → Validate functionality
6. **Days 15-16**: Phase 6 RAG → Chatbot integration
7. **Days 17-19**: Phase 7 deployment → Live demo

### Parallel Team Strategy

With multiple developers:

- **Developer A**: Phase 2 components (tabs + collapsibles)
- **Developer B**: Phase 2 components (admonitions + labs + diagrams)
- **Developer C**: Phase 3 chapter migrations (Chapters 1-3)
- **Developer D**: Phase 3 chapter migrations (Chapters 4-5) + Phase 4 styling

Once Phase 2 completes:
- All chapter migrations can proceed in parallel
- Styling can begin incrementally
- Testing can start on completed chapters

---

## Task Summary

| Phase | Description | Task Count | Parallelizable |
|-------|-------------|------------|----------------|
| Phase 1 | Research & Design | 5 | Yes (T001-T004) |
| Phase 2 | Component Library | 29 (T006-T034) | Yes (within subgroups) |
| Phase 3 | Chapter Migration | 33 (T035-T067) | Yes (all chapters) |
| Phase 4 | Styling & A11y | 14 (T068-T081) | Yes |
| Phase 5 | Testing & Validation | 15 (T082-T096) | Partially |
| Phase 6 | RAG Integration | 6 (T097-T102) | Partially |
| Phase 7 | Deployment & Demo | 10 (T103-T112) | Partially |
| Phase 8 | Polish | 8 (T113-T120) | Yes |
| **Total** | | **120 tasks** | **~80% parallelizable** |

### MVP Scope (Minimum for Hackathon Demo)

- Phase 1: Research (5 tasks)
- Phase 2: Component Library (29 tasks) - **CRITICAL**
- Phase 3: Chapter 1 ONLY (6 tasks: T035-T040)
- Phase 4: Basic Styling (8 tasks: T068-T075)
- Phase 7: Deployment (5 tasks: T103-T107)

**MVP Total**: 53 tasks - Single interactive chapter deployed

### Full Scope

All 120 tasks - Complete Module 4 with 5 interactive chapters, RAG integration, and production deployment

---

## Acceptance Criteria per Phase

### Phase 2 (Component Library)
- [ ] All 15+ components implemented and exported
- [ ] Components pass accessibility audit (automated)
- [ ] Component usage docs created
- [ ] Components work in light and dark mode

### Phase 3 (Content Migration)
- [ ] All 5 chapters converted to MDX
- [ ] Each chapter has 4+ tab groups
- [ ] Each chapter has 6+ collapsible sections
- [ ] Each chapter has 8+ admonitions
- [ ] Each chapter has 1+ lab box
- [ ] Each chapter has 2+ architecture diagrams

### Phase 4 (Styling)
- [ ] All components styled consistently
- [ ] Dark mode looks professional
- [ ] Mobile responsive (tested on 2+ devices)
- [ ] Animations smooth at 60fps

### Phase 5 (Testing)
- [ ] All functional tests pass
- [ ] Code examples validated (spot check)
- [ ] Beta tester feedback incorporated

### Phase 6 (RAG)
- [ ] Tab content indexed in Qdrant
- [ ] Chatbot retrieves tab-specific content
- [ ] Source citations include tab references

### Phase 7 (Deployment)
- [ ] Module 4 live on GitHub Pages
- [ ] Demo prepared and rehearsed
- [ ] Lighthouse score > 90

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [PHx] label maps task to specific phase for traceability
- Each phase should be independently completable
- Commit after each task or logical group
- Stop at MVP checkpoint to validate before continuing
- Avoid: vague tasks, same file conflicts, cross-phase dependencies

---

## Format Validation Checklist

✅ ALL tasks follow the checklist format:
- `- [ ] T### [P] [PHx] Description with file path`
- Checkbox: `- [ ]`
- Task ID: `T001`, `T002`, etc.
- [P] marker: Only for parallelizable tasks
- [PHx] label: For implementation phases (PH2-PH7)
- Description: Clear action with exact file path

✅ Task completeness:
- Each phase has all needed tasks
- Dependencies are clear
- File paths are specific
- Parallel opportunities identified

✅ Independent validation:
- Each phase can be tested independently
- MVP scope is clearly defined
- Checkpoints mark completion criteria
