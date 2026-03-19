# AI Agent Skills for Physical AI Textbook

This project includes 5 specialized AI subagents for creating textbook content. Each agent is designed for a specific task in the content creation workflow.

---

## 📁 File Structure

```
.agents/
├── content-writer.md    # Chapter content generation
├── diagram-generator.md # Mermaid.js diagram creation
├── quiz-generator.md    # Multiple-choice question generation
├── code-explainer.md    # Code walkthrough explanations
└── glossary-builder.md  # Technical term glossary
```

---

## 🚀 Quick Start

### Prerequisites

- Claude Code CLI installed
- Access to Claude Sonnet 4 (claude-sonnet-4-20250514)
- Node.js for Docusaurus (for MDX preview)

### Basic Usage Pattern

```bash
# All agents follow this pattern:
claude -p "<agent-name>" --input '<JSON input>'
```

---

## 📝 Agent Reference

### 1. Content Writer

**File:** `.agents/content-writer.md`

**Purpose:** Generates full textbook chapter content in MDX format from an outline.

**Best For:**
- Writing new chapters from bullet outlines
- Expanding rough notes into full content
- Ensuring consistent tone and structure

**Input:**
```json
{
  "title": "Introduction to ROS 2",
  "outline": [
    "What is ROS 2 and why it matters",
    "ROS 2 vs ROS 1: Key differences",
    "Core concepts: Nodes, Topics, Services, Actions",
    "Setting up ROS 2 Humble on Ubuntu",
    "Your first ROS 2 node in Python"
  ],
  "targetAudience": "Beginner",
  "chapterNumber": 1,
  "estimatedReadingTime": "20 minutes"
}
```

**Command:**
```bash
claude -p "content-writer" --input '{
  "title": "Introduction to ROS 2",
  "outline": ["What is ROS 2", "ROS 2 vs ROS 1", "Core concepts"],
  "targetAudience": "Beginner",
  "chapterNumber": 1
}'
```

**Output:** Complete MDX file with front matter, sections, code blocks, and callouts.

---

### 2. Diagram Generator

**File:** `.agents/diagram-generator.md`

**Purpose:** Creates Mermaid.js diagrams for technical concepts.

**Best For:**
- System architecture diagrams
- Communication flow visualizations
- State machines and sequence diagrams

**Input:**
```json
{
  "concept": "ROS 2 Node Communication",
  "diagramType": "flowchart",
  "entities": ["Publisher", "Subscriber", "Middleware", "Topic"],
  "relationships": [
    "Publisher -> Middleware: publish",
    "Middleware -> Topic: route",
    "Topic -> Subscriber: deliver"
  ],
  "context": "Show complete data flow"
}
```

**Command:**
```bash
claude -p "diagram-generator" --input '{
  "concept": "SLAM Pipeline",
  "diagramType": "flowchart",
  "entities": ["Camera", "Features", "Matching", "Pose", "Map"],
  "relationships": ["Camera->Features", "Features->Matching", "Matching->Pose", "Pose->Map"]
}'
```

**Output:**
```mermaid
flowchart LR
    A[Camera] --> B[Feature Extraction]
    B --> C[Feature Matching]
    C --> D[Pose Estimation]
    D --> E[Map Building]
```

**Supported Diagram Types:**
- `flowchart` - Architecture, data flow
- `sequenceDiagram` - Message sequences
- `classDiagram` - OOP structures
- `stateDiagram` - State machines
- `erDiagram` - Data relationships
- `gantt` - Timelines

---

### 3. Quiz Generator

**File:** `.agents/quiz-generator.md`

**Purpose:** Creates 5 multiple-choice questions from chapter content.

**Best For:**
- End-of-chapter assessments
- Knowledge checks
- Exam preparation

**Input:**
```json
{
  "chapterTitle": "Introduction to ROS 2",
  "chapterContent": "[Paste full chapter content here...]",
  "questionCount": 5,
  "focusAreas": ["DDS middleware", "Communication patterns", "ROS 1 vs ROS 2"],
  "difficulty": "beginner"
}
```

**Command:**
```bash
claude -p "quiz-generator" --input '{
  "chapterTitle": "URDF and Robot Descriptions",
  "chapterContent": "[paste chapter]",
  "questionCount": 5,
  "focusAreas": ["Links and joints", "XACRO"],
  "difficulty": "intermediate"
}'
```

**Output:** MDX Quiz component with questions, answers, explanations, and difficulty levels.

**Question Distribution:**
- 2 Easy (Remember/Understand)
- 2 Medium (Apply/Analyze)
- 1 Hard (Evaluate/Create)

---

### 4. Code Explainer

**File:** `.agents/code-explainer.md`

**Purpose:** Provides line-by-line explanations of Python/ROS 2 code.

**Best For:**
- Tutorial code walkthroughs
- Example code annotations
- Student code reviews

**Input:**
```json
{
  "codeSnippet": "import rclpy\nfrom rclpy.node import Node\n\nclass MinimalNode(Node):\n    def __init__(self):\n        super().__init__('minimal_node')\n        self.get_logger().info('Node started!')",
  "language": "python",
  "context": "ROS 2 Publisher Node",
  "targetAudience": "Beginner",
  "focusAreas": ["Node creation", "Publisher setup", "Timer callbacks"]
}
```

**Command:**
```bash
claude -p "code-explainer" --input '{
  "codeSnippet": "[paste code]",
  "language": "python",
  "context": "SLAM implementation",
  "targetAudience": "Student"
}'
```

**Output:** Detailed MDX section with:
- Code overview
- Section-by-section breakdown
- Line-by-line annotations
- Common pitfalls
- "Try This" exercises

---

### 5. Glossary Builder

**File:** `.agents/glossary-builder.md`

**Purpose:** Extracts technical terms and creates glossary entries.

**Best For:**
- Chapter glossaries
- Quick reference guides
- Terminology standardization

**Input:**
```json
{
  "chapterTitle": "Introduction to ROS 2",
  "chapterContent": "[Paste full chapter content...]",
  "chapterNumber": 1,
  "includeAcronyms": true,
  "includeExamples": true,
  "maxTerms": 30
}
```

**Command:**
```bash
claude -p "glossary-builder" --input '{
  "chapterTitle": "Robot Kinematics",
  "chapterContent": "[paste chapter]",
  "chapterNumber": 4,
  "includeAcronyms": true
}'
```

**Output:** MDX glossary with:
- Alphabetical term list
- Categorized quick reference
- Definitions with examples
- Cross-references

**Categories:**
- Concepts
- Software
- Hardware
- Algorithms
- Mathematics
- Standards

---

## 🔄 Complete Workflow Example

Here's how to use all agents together to create a chapter:

### Step 1: Generate Chapter Content

```bash
# Create chapter from outline
claude -p "content-writer" --input '{
  "title": "URDF and Robot Descriptions",
  "outline": [
    "What is URDF and why it matters",
    "Links: defining robot parts",
    "Joints: connecting links",
    "Visual vs Collision meshes",
    "XACRO for parametric robots",
    "Complete example: Simple arm"
  ],
  "targetAudience": "Student",
  "chapterNumber": 3
}' > docs/chapters/03-urdf.mdx
```

### Step 2: Generate Diagrams

```bash
# Create URDF tree diagram
claude -p "diagram-generator" --input '{
  "concept": "URDF Kinematic Chain",
  "diagramType": "flowchart",
  "entities": ["Base Link", "Joint 1", "Link 1", "Joint 2", "Link 2", "End Effector"],
  "relationships": [
    "Base Link -> Joint 1: parent",
    "Joint 1 -> Link 1: connects",
    "Link 1 -> Joint 2: parent",
    "Joint 2 -> Link 2: connects",
    "Link 2 -> End Effector: terminal"
  ],
  "context": "Show parent-child tree structure"
}' >> docs/chapters/03-urdf.mdx
```

### Step 3: Explain Example Code

```bash
# Explain URDF parsing code
claude -p "code-explainer" --input '{
  "codeSnippet": "import urdf_parser_py.urdf as urdf\n\nrobot = urdf.URDF.from_xml_file(\"robot.urdf\")\nprint(f\"Robot has {len(robot.links)} links\")\nfor joint in robot.joints:\n    print(f\"Joint {joint.name}: {joint.type}\")",
  "language": "python",
  "context": "URDF parsing example",
  "targetAudience": "Beginner"
}' >> docs/chapters/03-urdf.mdx
```

### Step 4: Generate Quiz

```bash
# Create chapter quiz
claude -p "quiz-generator" --input '{
  "chapterTitle": "URDF and Robot Descriptions",
  "chapterContent": "[paste generated chapter]",
  "questionCount": 5,
  "focusAreas": ["Links", "Joints", "XACRO"],
  "difficulty": "intermediate"
}' >> docs/chapters/03-urdf.mdx
```

### Step 5: Build Glossary

```bash
# Extract glossary terms
claude -p "glossary-builder" --input '{
  "chapterTitle": "URDF and Robot Descriptions",
  "chapterContent": "[paste generated chapter]",
  "chapterNumber": 3,
  "includeAcronyms": true
}' > docs/glossary/chapter-03-glossary.mdx
```

---

## 📋 Agent Comparison Table

| Agent | Input Type | Output Type | Best Used When |
|-------|-----------|-------------|----------------|
| Content Writer | Outline | Full chapter MDX | Starting new chapter |
| Diagram Generator | Concept + entities | Mermaid code block | Need visual explanation |
| Quiz Generator | Chapter content | MCQ component | Chapter complete |
| Code Explainer | Code snippet | Annotated walkthrough | Have example code |
| Glossary Builder | Chapter content | Glossary entries | Finalizing chapter |

---

## 💡 Tips for Best Results

### Content Writer
- Provide detailed outlines (5-7 bullet points minimum)
- Specify target audience for appropriate technical depth
- Include estimated reading time for pacing guidance

### Diagram Generator
- Be specific about diagram type
- List all entities that should appear
- Describe relationships clearly with direction

### Quiz Generator
- Include full chapter content for context
- Specify focus areas to emphasize important topics
- Adjust difficulty based on audience

### Code Explainer
- Include complete, runnable code snippets
- Specify the learning objective
- Note any ROS 2 or Python concepts to emphasize

### Glossary Builder
- Include full chapter for comprehensive term extraction
- Set appropriate maxTerms (20-40 typical)
- Always include acronyms for technical content

---

## 🔧 Customization

Each agent file can be customized for your specific needs:

1. **Modify system prompts** in each `.agents/*.md` file
2. **Adjust output formats** to match your Docusaurus components
3. **Add domain-specific knowledge** for your textbook focus
4. **Change difficulty defaults** based on your audience

---

## 📚 Example Outputs

See the `docs/examples/` folder for complete examples of each agent's output.

---

## 🤝 Contributing

When adding new agents:
1. Create `.agents/<agent-name>.md`
2. Follow the same structure (Purpose, System Prompt, Input/Output, Examples)
3. Update this documentation
4. Add example outputs to `docs/examples/`

---

## 📞 Support

For questions about agent usage:
- Check individual agent files for detailed prompts
- Review example outputs in `docs/examples/`
- Experiment with different input parameters

---

<div align="center">

**Built for the Physical AI & Humanoid Robotics Textbook**

[Back to Top](#ai-agent-skills-for-physical-ai-textbook)

</div>
