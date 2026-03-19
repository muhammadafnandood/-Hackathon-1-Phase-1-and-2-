import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import { useWindowSize } from '@docusaurus/theme-common';
import { useDoc } from '@docusaurus/theme-common/internal';
import DocItemPaginator from '@theme/DocItem/Paginator';
import DocVersionBanner from '@theme/DocVersionBanner';
import DocVersionBadge from '@theme/DocVersionBadge';
import DocItemFooter from '@theme/DocItem/Footer';
import DocItemTOCMobile from '@theme/DocItem/TOC/Mobile';
import DocItemTOCDesktop from '@theme/DocItem/TOC/Desktop';
import DocItemContent from '@theme/DocItem/Content';
import DocBreadcrumbs from '@theme/DocBreadcrumbs';
import type { Props } from '@theme/DocItem/Layout';
import styles from './styles.module.css';

// Import the PersonalizeButton component
import PersonalizeButton from '../../../components/PersonalizeButton';

/**
 * Decide if the toc table is visible, even if the window size is big enough.
 */
function useDocTOC() {
  const {
    frontMatter,
    toc,
  } = useDoc();
  const windowSize = useWindowSize();

  // Hidden only if explicitly disabled via front matter
  const hidden = {
    inline: frontMatter.hide_table_of_contents,
    desktop: frontMatter.hide_table_of_contents,
  };

  const mobile = {
    hidden: hidden.inline,
    toc,
  };

  const desktop = {
    hidden: hidden.desktop || windowSize === 'mobile',
    toc,
  };

  return {
    hidden,
    mobile,
    desktop,
  };
}

export default function DocItemLayout({ children }: Props): JSX.Element {
  const docTOC = useDocTOC();
  const { metadata } = useDoc();
  const [originalContent, setOriginalContent] = useState<string>('');
  const [currentContent, setCurrentContent] = useState<string>(children as string);

  // Extract the chapter content from the rendered HTML
  useEffect(() => {
    // Store original content on mount
    const contentDiv = document.querySelector('.markdown');
    if (contentDiv && !originalContent) {
      setOriginalContent(contentDiv.innerHTML);
      setCurrentContent(contentDiv.innerHTML);
    }
  }, [originalContent]);

  // Handle content change from PersonalizeButton
  const handleContentChange = (newContent: string) => {
    const contentDiv = document.querySelector('.markdown');
    if (contentDiv) {
      contentDiv.innerHTML = newContent;
      setCurrentContent(newContent);
      
      // Re-run any scripts that might be in the content
      const scripts = contentDiv.querySelectorAll('script');
      scripts.forEach((oldScript) => {
        const newScript = document.createElement('script');
        Array.from(oldScript.attributes).forEach((attr) => {
          newScript.setAttribute(attr.name, attr.value);
        });
        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
        oldScript.parentNode?.replaceChild(newScript, oldScript);
      });
    }
  };

  // Get chapter ID from metadata
  const chapterId = metadata.id || metadata.permalink || 'chapter';

  // Extract raw markdown content if available
  const getChapterContent = () => {
    // Try to get content from the children prop or from the DOM
    if (typeof children === 'string') {
      return children;
    }
    
    // Fallback: try to get from DOM
    const contentDiv = document.querySelector('.markdown');
    return contentDiv ? contentDiv.innerHTML : '';
  };

  return (
    <div className={styles.docItemContainer}>
      <div className={styles.docItemWrapper}>
        <DocBreadcrumbs />
        <DocVersionBanner />
        
        {/* Personalize This Chapter Button */}
        <PersonalizeButton
          chapterContent={getChapterContent()}
          chapterId={chapterId}
          onContentChange={handleContentChange}
        />
        
        <div className="row">
          <div className={clsx('col', !docTOC.desktop.hidden && styles.docItemCol)}>
            <DocVersionBadge />
            <DocItemTOCMobile
              hidden={docTOC.mobile.hidden}
              toc={docTOC.mobile.toc}
            />
            <DocItemContent>{children}</DocItemContent>
            <DocItemFooter />
            <DocItemPaginator />
          </div>
          
          {!docTOC.desktop.hidden && (
            <div className="col col--3">
              <DocItemTOCDesktop
                hidden={docTOC.desktop.hidden}
                toc={docTOC.desktop.toc}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
