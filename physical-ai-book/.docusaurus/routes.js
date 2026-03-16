import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/blog',
    component: ComponentCreator('/blog', 'b2f'),
    exact: true
  },
  {
    path: '/blog/archive',
    component: ComponentCreator('/blog/archive', '182'),
    exact: true
  },
  {
    path: '/blog/authors',
    component: ComponentCreator('/blog/authors', '0b7'),
    exact: true
  },
  {
    path: '/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/blog/authors/all-sebastien-lorber-articles', '4a1'),
    exact: true
  },
  {
    path: '/blog/authors/yangshun',
    component: ComponentCreator('/blog/authors/yangshun', 'a68'),
    exact: true
  },
  {
    path: '/blog/first-blog-post',
    component: ComponentCreator('/blog/first-blog-post', '89a'),
    exact: true
  },
  {
    path: '/blog/long-blog-post',
    component: ComponentCreator('/blog/long-blog-post', '9ad'),
    exact: true
  },
  {
    path: '/blog/mdx-blog-post',
    component: ComponentCreator('/blog/mdx-blog-post', 'e9f'),
    exact: true
  },
  {
    path: '/blog/tags',
    component: ComponentCreator('/blog/tags', '287'),
    exact: true
  },
  {
    path: '/blog/tags/docusaurus',
    component: ComponentCreator('/blog/tags/docusaurus', '704'),
    exact: true
  },
  {
    path: '/blog/tags/facebook',
    component: ComponentCreator('/blog/tags/facebook', '858'),
    exact: true
  },
  {
    path: '/blog/tags/hello',
    component: ComponentCreator('/blog/tags/hello', '299'),
    exact: true
  },
  {
    path: '/blog/tags/hola',
    component: ComponentCreator('/blog/tags/hola', '00d'),
    exact: true
  },
  {
    path: '/blog/welcome',
    component: ComponentCreator('/blog/welcome', 'd2b'),
    exact: true
  },
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', '3d7'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '067'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'a8a'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'ccf'),
            routes: [
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '853'),
                exact: true
              },
              {
                path: '/docs/module1/chapter1-ros2-introduction',
                component: ComponentCreator('/docs/module1/chapter1-ros2-introduction', '6e4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module1/chapter2-ros2-communication',
                component: ComponentCreator('/docs/module1/chapter2-ros2-communication', '45d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module1/chapter3-python-agents-ros2',
                component: ComponentCreator('/docs/module1/chapter3-python-agents-ros2', 'b63'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module1/chapter4-urdf-humanoid',
                component: ComponentCreator('/docs/module1/chapter4-urdf-humanoid', 'f02'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module1/chapter5-robot-nervous-system',
                component: ComponentCreator('/docs/module1/chapter5-robot-nervous-system', '5ae'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module2/chapter1-betterauth-setup',
                component: ComponentCreator('/docs/module2/chapter1-betterauth-setup', '116'),
                exact: true
              },
              {
                path: '/docs/module2/chapter1-intro-simulation',
                component: ComponentCreator('/docs/module2/chapter1-intro-simulation', '8c6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module2/chapter2-gazebo-environment',
                component: ComponentCreator('/docs/module2/chapter2-gazebo-environment', '3b4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module2/chapter2-user-personalization',
                component: ComponentCreator('/docs/module2/chapter2-user-personalization', '9b4'),
                exact: true
              },
              {
                path: '/docs/module2/chapter3-physics-and-sensors',
                component: ComponentCreator('/docs/module2/chapter3-physics-and-sensors', '015'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module2/chapter3-urdu-chatbot',
                component: ComponentCreator('/docs/module2/chapter3-urdu-chatbot', 'ec0'),
                exact: true
              },
              {
                path: '/docs/module2/chapter4-unity-visualization',
                component: ComponentCreator('/docs/module2/chapter4-unity-visualization', '748'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module2/chapter5-building-digital-twin',
                component: ComponentCreator('/docs/module2/chapter5-building-digital-twin', '808'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module2/code/',
                component: ComponentCreator('/docs/module2/code/', '0e1'),
                exact: true
              },
              {
                path: '/docs/module2/code/chapter1/install_unity',
                component: ComponentCreator('/docs/module2/code/chapter1/install_unity', 'bb0'),
                exact: true
              },
              {
                path: '/docs/module2/labs/',
                component: ComponentCreator('/docs/module2/labs/', '790'),
                exact: true
              },
              {
                path: '/docs/module3/chapter1-betterauth-setup',
                component: ComponentCreator('/docs/module3/chapter1-betterauth-setup', '637'),
                exact: true
              },
              {
                path: '/docs/module3/chapter1-isaac-platform',
                component: ComponentCreator('/docs/module3/chapter1-isaac-platform', '4fc'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module3/chapter2-synthetic-data',
                component: ComponentCreator('/docs/module3/chapter2-synthetic-data', 'bd5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module3/chapter2-user-personalization',
                component: ComponentCreator('/docs/module3/chapter2-user-personalization', '7c0'),
                exact: true
              },
              {
                path: '/docs/module3/chapter3-urdu-chatbot',
                component: ComponentCreator('/docs/module3/chapter3-urdu-chatbot', 'eca'),
                exact: true
              },
              {
                path: '/docs/module3/chapter3-visual-slam',
                component: ComponentCreator('/docs/module3/chapter3-visual-slam', '617'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module3/chapter4-nav2-navigation',
                component: ComponentCreator('/docs/module3/chapter4-nav2-navigation', '5ad'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module3/chapter5-robot-reinforcement-learning',
                component: ComponentCreator('/docs/module3/chapter5-robot-reinforcement-learning', 'c13'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module3/code/',
                component: ComponentCreator('/docs/module3/code/', '6e3'),
                exact: true
              },
              {
                path: '/docs/module3/labs/',
                component: ComponentCreator('/docs/module3/labs/', 'f19'),
                exact: true
              },
              {
                path: '/docs/module4/chapter1-llm-robotics',
                component: ComponentCreator('/docs/module4/chapter1-llm-robotics', '492'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module4/chapter2-voice-to-action',
                component: ComponentCreator('/docs/module4/chapter2-voice-to-action', '63f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module4/chapter3-cognitive-planning',
                component: ComponentCreator('/docs/module4/chapter3-cognitive-planning', '088'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module4/chapter4-multimodal-interaction',
                component: ComponentCreator('/docs/module4/chapter4-multimodal-interaction', '9cd'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module4/chapter5-conversational-robotics',
                component: ComponentCreator('/docs/module4/chapter5-conversational-robotics', '05a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/docs/tutorial-basics/congratulations', '70e'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/docs/tutorial-basics/create-a-blog-post', '315'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/docs/tutorial-basics/create-a-document', 'f86'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/docs/tutorial-basics/create-a-page', '9f6'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/docs/tutorial-basics/deploy-your-site', 'b91'),
                exact: true
              },
              {
                path: '/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/docs/tutorial-basics/markdown-features', '272'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/docs/tutorial-extras/manage-docs-versions', 'a34'),
                exact: true
              },
              {
                path: '/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/docs/tutorial-extras/translate-your-site', '739'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'e5f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
