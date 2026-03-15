/**
 * Custom MDX Components Registration
 * 
 * This file registers all custom MDX components globally.
 * Components registered here can be used in any MDX file without explicit imports.
 */

import React from 'react';
import MDXComponents from '@theme-original/MDXComponents';
import {TabGroup, TabItem} from '@site/src/components/mdx/Tabs';
import {CollapsibleSection, CodeCollapsible} from '@site/src/components/mdx/Collapsible';
import {
  TipAdmonition,
  WarningAdmonition,
  NoteAdmonition,
  SafetyAdmonition,
} from '@site/src/components/mdx/Admonition';
import {ObjectiveList, LabBox} from '@site/src/components/mdx/Lab';
import {MermaidDiagram, ArchitectureDiagram} from '@site/src/components/mdx/Diagram';

// Extend the default MDX components with our custom components
const components = {
  ...MDXComponents,
  
  // Tabs
  TabGroup,
  TabItem,
  
  // Collapsibles
  CollapsibleSection,
  CodeCollapsible,
  
  // Admonitions (custom versions)
  TipAdmonition,
  WarningAdmonition,
  NoteAdmonition,
  SafetyAdmonition,
  
  // Lab Components
  ObjectiveList,
  LabBox,
  
  // Diagrams
  MermaidDiagram,
  ArchitectureDiagram,
};

export default components;
