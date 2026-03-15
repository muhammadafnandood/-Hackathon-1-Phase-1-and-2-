import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Master the art of building intelligent humanoid robots',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://your-docusaurus-site.example.com',
  baseUrl: '/',

  organizationName: 'physical-ai',
  projectName: 'humanoid-robotics-textbook',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/your-org/physical-ai-book/tree/main/',
          routeBasePath: '/',
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/social-card.jpg',
    
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },

    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      },
    },

    navbar: {
      title: 'Physical AI',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
        srcDark: 'img/logo-dark.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          type: 'dropdown',
          label: 'Modules',
          position: 'left',
          items: [
            {
              label: 'Module 1: ROS2 Basics',
              to: '/docs/module1/chapter1-ros2-introduction',
            },
            {
              label: 'Module 2: Simulation',
              to: '/docs/module2/chapter1-intro-simulation',
            },
            {
              label: 'Module 3: AI Brain (Isaac)',
              to: '/docs/module3/chapter1-isaac-platform',
            },
            {
              label: 'Module 4: VLA Robotics',
              to: '/docs/module4/chapter1-llm-robotics',
            },
            {
              label: 'Module 5: RAG System',
              to: '/docs/module5/chapter1-betterauth-setup',
            },
          ],
        },
        {
          href: 'https://github.com/your-org/physical-ai-book',
          label: 'GitHub',
          position: 'right',
          className: 'header-github-link',
          'aria-label': 'GitHub repository',
        },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'Modules',
          items: [
            {
              label: 'Module 1: ROS2',
              to: '/docs/module1/chapter1-ros2-introduction',
            },
            {
              label: 'Module 2: Simulation',
              to: '/docs/module2/chapter1-intro-simulation',
            },
            {
              label: 'Module 3: Isaac AI',
              to: '/docs/module3/chapter1-isaac-platform',
            },
            {
              label: 'Module 4: VLA',
              to: '/docs/module4/chapter1-llm-robotics',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Code Examples',
              href: 'https://github.com/your-org/physical-ai-book/tree/main/physical-ai-book/docs',
            },
            {
              label: 'Labs',
              to: '/docs/labs',
            },
            {
              label: 'Glossary',
              to: '/docs/glossary',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Discord',
              href: 'https://discord.gg/physical-ai',
            },
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/physical-ai',
            },
            {
              label: 'X (Twitter)',
              href: 'https://x.com/physical_ai',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'json', 'xml', 'markdown'],
    },

    algolia: {
      appId: 'YOUR_ALGOLIA_APP_ID',
      apiKey: 'YOUR_ALGOLIA_API_KEY',
      indexName: 'physical-ai',
      contextualSearch: true,
      searchParameters: {},
      searchPagePath: 'search',
    },
  } satisfies Preset.ThemeConfig,

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'labs',
        path: 'labs',
        routeBasePath: 'labs',
        sidebarPath: './sidebars.ts',
      },
    ],
    [
      '@docusaurus/plugin-client-redirects',
      {
        redirects: [],
      },
    ],
  ],

  scripts: [
    {
      src: '/chatbot.js',
      async: true,
    },
  ],
};

export default config;
