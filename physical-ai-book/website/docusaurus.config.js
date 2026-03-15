// @ts-check
// Docusaurus Configuration for Physical AI Textbook

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Learn to build intelligent humanoid robots with ROS 2, AI, and simulation',
  favicon: 'img/favicon.ico',

  url: 'https://physical-ai-book.github.io',
  baseUrl: '/',
  organizationName: 'physical-ai-book',
  projectName: 'textbook',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        htmlLang: 'en',
      },
      ur: {
        htmlLang: 'ur',
        direction: 'rtl',
      },
    },
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/physical-ai-book/textbook/tree/main/website/',
          routeBasePath: '/', // Serve docs at the root
        },
        blog: false, // Disable blog
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  scripts: [
    {
      src: '/js/chat-widget.js',
      async: true,
    },
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Physical AI Textbook',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Modules',
          },
          {
            href: 'https://github.com/physical-ai-book/textbook',
            label: 'GitHub',
            position: 'right',
          },
          {
            type: 'localeDropdown',
            position: 'right',
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
                label: 'Module 1: ROS 2',
                to: '/module1',
              },
              {
                label: 'Module 2: Simulation',
                to: '/module2',
              },
              {
                label: 'Module 3: AI Brain',
                to: '/module3',
              },
              {
                label: 'Module 4: VLA',
                to: '/module4',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/physical-ai-book/textbook',
              },
              {
                label: 'Discord',
                href: 'https://discord.gg/placeholder',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'yaml', 'xml'],
      },
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
    }),
};

export default config;
