import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: ROS2 Robotic Nervous System',
      items: [
        'docs/module1/chapter1-ros2-introduction',
        'docs/module1/chapter2-ros2-communication',
        'docs/module1/chapter3-python-agents-ros2',
        'docs/module1/chapter4-urdf-humanoid',
        'docs/module1/chapter5-robot-nervous-system',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'docs/module2/chapter1-intro-simulation',
        'docs/module2/chapter2-gazebo-environment',
        'docs/module2/chapter3-physics-and-sensors',
        'docs/module2/chapter4-unity-visualization',
        'docs/module2/chapter5-building-digital-twin',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: AI Robot Brain (NVIDIA Isaac)',
      items: [
        'docs/module3/chapter1-isaac-platform',
        'docs/module3/chapter2-synthetic-data',
        'docs/module3/chapter3-visual-slam',
        'docs/module3/chapter4-nav2-navigation',
        'docs/module3/chapter5-robot-reinforcement-learning',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'docs/module4/chapter1-llm-robotics',
        'docs/module4/chapter2-voice-to-action',
        'docs/module4/chapter3-cognitive-planning',
        'docs/module4/chapter4-multimodal-interaction',
        'docs/module4/chapter5-conversational-robotics',
      ],
    },
  ],
};

export default sidebars;
