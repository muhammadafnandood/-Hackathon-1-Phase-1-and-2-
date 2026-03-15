# MDX Component Library Documentation

This document describes all custom MDX components available for use in Module 4 chapters.

## Quick Start

All components are **automatically available** in MDX files without explicit imports thanks to global registration in `src/theme/MDXComponents.js`.

```mdx
---
sidebar_label: 'My Chapter'
---

# Chapter Title

<TabGroup groupId="my-tabs" persist>
  <TabItem value="tab1" label="Tab 1" icon="📚">
    Content here...
  </TabItem>
</TabGroup>
```

---

## Tab Components

### `<TabGroup>`

Container for tabbed content with state persistence.

**Props:**
- `groupId` (required): Unique identifier for state persistence
- `persist` (optional, default: `true`): Remember selected tab across sessions
- `lazy` (optional, default: `false`): Only render default tab initially
- `className` (optional): Custom CSS class

**Example:**
```mdx
<TabGroup groupId="llm-architecture" persist lazy>
  <TabItem value="concept" label="Concept" icon="📚">
    Concept content...
  </TabItem>
  <TabItem value="example" label="Example" icon="💻">
    Example content...
  </TabItem>
</TabGroup>
```

### `<TabItem>`

Individual tab with icon support.

**Props:**
- `value` (required): Unique tab identifier
- `label` (required): Display label
- `icon` (optional): Emoji or React node icon
- `className` (optional): Custom CSS class
- `attributes` (optional): Extra HTML attributes

**Example:**
```mdx
<TabItem value="lab" label="Hands-on Lab" icon="🔬" className="custom-lab">
  Lab instructions...
</TabItem>
```

---

## Collapsible Components

### `<CollapsibleSection>`

Expandable/collapsible content section with smooth animations.

**Props:**
- `title` (required): Section title (visible when collapsed)
- `icon` (optional): Custom icon (default: ▶️/🔽)
- `defaultOpen` (optional, default: `false`): Initially expanded
- `persist` (optional, default: `false`): Remember expanded state
- `className` (optional): Custom CSS class

**Example:**
```mdx
<CollapsibleSection title="Advanced: Mathematical Formulation" icon="🧮" defaultOpen persist>
  Detailed mathematical derivations...
</CollapsibleSection>
```

### `<CodeCollapsible>`

Collapsible code block with syntax highlighting.

**Props:**
- `title` (optional, default: "Show Code"): Collapsible title
- `language` (optional, default: "python"): Code language
- `defaultOpen` (optional, default: `false`): Initially expanded
- `showLineNumbers` (optional, default: `true`): Show line numbers
- `metastring` (optional): Code block metastring

**Example:**
```mdx
<CodeCollapsible title="Show Alternative Implementation" language="python" showLineNumbers>
{`def alternative_approach():
    # This code is hidden by default
    return "efficient!"`}
</CodeCollapsible>
```

---

## Admonition Components

### `<TipAdmonition>`

Green-themed tip for pro tips and best practices.

**Props:**
- `title` (optional, default: "💡 Pro Tip")
- `icon` (optional): Custom icon
- `className` (optional): Custom CSS class

**Example:**
```mdx
<TipAdmonition title="Pro Tip: Temperature Settings">
  Use `temperature=0.3` for deterministic robot actions.
</TipAdmonition>
```

### `<WarningAdmonition>`

Orange-themed warning for cautions.

**Props:**
- `title` (optional, default: "⚠️ Warning")
- `icon` (optional): Custom icon
- `className` (optional): Custom CSS class

**Example:**
```mdx
<WarningAdmonition title="Warning: Handle Privacy">
  Always handle voice data securely and respect user privacy.
</WarningAdmonition>
```

### `<NoteAdmonition>`

Blue-themed note for additional information.

**Props:**
- `title` (optional, default: "ℹ️ Note")
- `icon` (optional): Custom icon
- `className` (optional): Custom CSS class

**Example:**
```mdx
<NoteAdmonition title="Note: Prerequisites">
  This chapter assumes basic Python knowledge.
</NoteAdmonition>
```

### `<SafetyAdmonition>`

Red-themed safety-critical warning.

**Props:**
- `title` (optional, default: "🛑 Safety Critical")
- `icon` (optional): Custom icon
- `className` (optional): Custom CSS class

**Example:**
```mdx
<SafetyAdmonition title="Safety Critical: Emergency Stop">
  **ALWAYS** implement emergency stop before testing on physical hardware!
</SafetyAdmonition>
```

---

## Lab Components

### `<ObjectiveList>`

Learning objectives list with checkmark styling.

**Props:**
- `className` (optional): Custom CSS class

**Example:**
```mdx
<ObjectiveList>
- Understand LLM architecture for robotics
- Implement natural language parsing
- Deploy LLM-ROS2 bridge
</ObjectiveList>
```

### `<LabBox>`

Full-featured lab container with badges, hardware requirements, and checklist.

**Props:**
- `duration` (required): Estimated time (e.g., "45 min")
- `difficulty` (required): "beginner" | "intermediate" | "advanced"
- `simulationAvailable` (optional, default: `true`): Simulation alternative exists
- `hardwareRequired` (optional): Array of required hardware items
- `title` (optional, default: "🔬 Hands-on Lab"): Custom title
- `className` (optional): Custom CSS class

**Example:**
```mdx
<LabBox 
  duration="45 min" 
  difficulty="intermediate"
  simulationAvailable={true}
  hardwareRequired={["ROS2 Humble", "OpenAI API Key", "Python 3.10+"]}
  title="🔬 Lab: Build LLM-ROS2 Bridge"
>

### Objective

Connect an LLM to ROS2 for natural language robot control.

### Steps

1. Install dependencies
2. Create ROS2 node
3. Integrate OpenAI API
4. Test with voice commands

</LabBox>
```

---

## Diagram Components

### `<MermaidDiagram>`

Interactive Mermaid flow chart with zoom and download.

**Props:**
- `className` (optional): Custom CSS class
- `zoomable` (optional, default: `true`): Enable zoom/pan
- `downloadable` (optional, default: `true`): Show download button

**Example:**
```mdx
<MermaidDiagram zoomable downloadable>
{`graph TD
    A[Voice Command] --> B(Whisper STT)
    B --> C{LLM Planning}
    C --> D[Action Parser]
    D --> E[ROS2 Executor]
`}
</MermaidDiagram>
```

**Note:** Requires `mermaid` package (`npm install mermaid`).

### `<ArchitectureDiagram>`

Container for architecture diagrams with title and caption.

**Props:**
- `title` (optional): Diagram title
- `caption` (optional): Diagram caption
- `zoomable` (optional, default: `true`): Enable zoom
- `className` (optional): Custom CSS class

**Example:**
```mdx
<ArchitectureDiagram 
  title="System Architecture" 
  caption="Complete LLM-robotics pipeline"
>

<MermaidDiagram>
{`graph LR
    A[Frontend] --> B[Backend]
    B --> C[Database]
`}
</MermaidDiagram>

</ArchitectureDiagram>
```

---

## Component Combinations

### Tab + Collapsible + Admonition

```mdx
<TabGroup groupId="advanced-llm" persist>
  <TabItem value="prompt" label="Prompt Engineering" icon="📝">
    <TipAdmonition title="Pro Tip">
      Use few-shot learning for better results.
    </TipAdmonition>
    
    <CollapsibleSection title="Advanced Techniques" icon="🧮">
      Detailed prompt engineering strategies...
    </CollapsibleSection>
  </TabItem>
  
  <TabItem value="code" label="Code Examples" icon="💻">
    <CodeCollapsible title="Show LLM Bridge Code">
      {`# Python code here`}
    </CodeCollapsible>
  </TabItem>
</TabGroup>
```

### Lab + Objectives + Diagram

```mdx
<ObjectiveList>
- Build complete LLM-robotics system
- Test with real hardware
</ObjectiveList>

<LabBox duration="60 min" difficulty="advanced">
  ### Procedure
  
  1. Set up environment
  2. Implement LLM bridge
  3. Test with robot
  
  <MermaidDiagram>
  {`graph TD
      A[Start] --> B[Setup]
      B --> C[Implement]
      C --> D[Test]
  `}
  </MermaidDiagram>
</LabBox>
```

---

## Accessibility Features

All components include:
- ✅ ARIA labels and roles
- ✅ Keyboard navigation support
- ✅ Focus indicators
- ✅ Screen reader announcements
- ✅ WCAG 2.1 AA color contrast

---

## Dark Mode Support

All components automatically adapt to dark mode with appropriate colors and borders.

---

## Responsive Design

All components are mobile-responsive with breakpoints at 768px.

---

## Troubleshooting

### Components not rendering?

1. Check that `src/theme/MDXComponents.js` exists
2. Verify file extension is `.mdx` not `.md`
3. Restart Docusaurus dev server

### Mermaid diagrams not showing?

1. Install mermaid: `npm install mermaid`
2. Check browser console for errors
3. Verify Mermaid syntax at [mermaid.live](https://mermaid.live)

### Styles not applying?

1. Verify `custom.css` is imported in `docusaurus.config.ts`
2. Clear browser cache
3. Check CSS class names match

---

## Component Files

```
src/components/mdx/
├── Tabs/
│   ├── TabGroup.tsx
│   ├── TabItem.tsx
│   └── index.ts
├── Collapsible/
│   ├── CollapsibleSection.tsx
│   ├── CodeCollapsible.tsx
│   └── index.ts
├── Admonition/
│   ├── TipAdmonition.tsx
│   ├── WarningAdmonition.tsx
│   ├── NoteAdmonition.tsx
│   ├── SafetyAdmonition.tsx
│   └── index.ts
├── Lab/
│   ├── ObjectiveList.tsx
│   ├── LabBox.tsx
│   └── index.ts
├── Diagram/
│   ├── MermaidDiagram.tsx
│   ├── ArchitectureDiagram.tsx
│   └── index.ts
└── index.ts
```

---

## Next Steps

1. ✅ Test components in `docs/module4/test-components.mdx`
2. 📖 Start migrating Chapter 1 to MDX
3. 🎨 Customize styling in `src/css/custom.css`
4. 🚀 Deploy and demo
