/**
 * MDX Components Library for Physical AI Textbook
 * 
 * This module exports all custom MDX components for interactive content.
 * Import these in your MDX files or register them globally in MDXComponents.js
 */

// Tabs
export {TabGroup, TabItem, useTabGroup} from './Tabs';
export type {TabGroupProps, TabItemProps} from './Tabs';

// Collapsible
export {CollapsibleSection, CodeCollapsible} from './Collapsible';
export type {CollapsibleSectionProps, CodeCollapsibleProps} from './Collapsible';

// Admonitions
export {
  TipAdmonition,
  WarningAdmonition,
  NoteAdmonition,
  SafetyAdmonition,
} from './Admonition';
export type {
  TipAdmonitionProps,
  WarningAdmonitionProps,
  NoteAdmonitionProps,
  SafetyAdmonitionProps,
} from './Admonition';

// Lab Components
export {ObjectiveList, LabBox} from './Lab';
export type {ObjectiveListProps, LabBoxProps} from './Lab';

// Diagrams
export {MermaidDiagram, ArchitectureDiagram} from './Diagram';
export type {MermaidDiagramProps, ArchitectureDiagramProps} from './Diagram';
