// @ts-check
// Docusaurus Sidebar Configuration

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: ROS 2 Robotic Nervous System',
      link: {
        type: 'doc',
        id: 'module1/chapter1-ros2-introduction',
      },
      items: [
        'module1/chapter1-ros2-introduction',
        'module1/chapter2-ros2-communication',
        'module1/chapter3-python-agents-ros2',
        'module1/chapter4-urdf-humanoid',
        'module1/chapter5-robot-nervous-system',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Digital Twin Simulation',
      link: {
        type: 'doc',
        id: 'module2/chapter1-intro-simulation',
      },
      items: [
        'module2/chapter1-intro-simulation',
        'module2/chapter2-gazebo-environment',
        'module2/chapter3-physics-and-sensors',
        'module2/chapter4-unity-visualization',
        'module2/chapter5-building-digital-twin',
      ],
      collapsed: true,
    },
    {
      type: 'category',
      label: 'Module 3: AI Robot Brain',
      link: {
        type: 'doc',
        id: 'module3/chapter1-isaac-platform',
      },
      items: [
        'module3/chapter1-isaac-platform',
        'module3/chapter2-synthetic-data',
        'module3/chapter3-visual-slam',
        'module3/chapter4-nav2-navigation',
        'module3/chapter5-robot-reinforcement-learning',
      ],
      collapsed: true,
    },
    {
      type: 'category',
      label: 'Module 4: Vision Language Action',
      link: {
        type: 'doc',
        id: 'module4/chapter1-llm-robotics',
      },
      items: [
        'module4/chapter1-llm-robotics',
        'module4/chapter2-voice-to-action',
        'module4/chapter3-cognitive-planning',
        'module4/chapter4-multimodal-interaction',
        'module4/chapter5-conversational-robotics',
      ],
      collapsed: true,
    },
  ],
};

export default sidebars;
