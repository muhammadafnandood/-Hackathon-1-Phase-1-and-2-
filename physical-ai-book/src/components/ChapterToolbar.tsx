import React, { useState, useCallback, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import PersonalizeButton from './PersonalizeButton';
import UrduTranslateButton from './UrduTranslateButton';

interface ChapterToolbarProps {
  chapterContent: string;
  chapterId: string;
  chapterTitle: string;
  onContentChange?: (newContent: string) => void;
}

/**
 * Combined toolbar component that manages both Personalize and Urdu Translate buttons.
 * 
 * Features:
 * - Tracks currentContent state (starts as original, updates after personalize/translate)
 * - Urdu translation runs on PERSONALIZED content if user personalized first
 * - Loading skeleton animation during API calls
 * - Proper state management to avoid conflicts
 */
const ChapterToolbar: React.FC<ChapterToolbarProps> = ({
  chapterContent,
  chapterId,
  chapterTitle,
  onContentChange,
}) => {
  const { isAuthenticated } = useAuth();
  
  // Central state management for content
  const [currentContent, setCurrentContent] = useState<string>(chapterContent);
  const [isUrduMode, setIsUrduMode] = useState(false);
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [originalContent, setOriginalContent] = useState<string>(chapterContent);
  const [personalizedContent, setPersonalizedContent] = useState<string | null>(null);
  const [urduContent, setUrduContent] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingType, setLoadingType] = useState<'personalize' | 'translate' | null>(null);

  // Reset state when chapter changes
  useEffect(() => {
    setCurrentContent(chapterContent);
    setOriginalContent(chapterContent);
    setIsUrduMode(false);
    setIsPersonalized(false);
    setPersonalizedContent(null);
    setUrduContent(null);
    setIsLoading(false);
    setLoadingType(null);
  }, [chapterId, chapterContent]);

  // Handle content change from either button
  const handleContentChange = useCallback((newContent: string, isUrdu: boolean = false) => {
    setCurrentContent(newContent);
    
    if (isUrdu) {
      setUrduContent(newContent);
      setIsUrduMode(true);
    } else {
      setPersonalizedContent(newContent);
      setIsPersonalized(true);
    }
    
    // Update DOM directly as fallback
    const contentDiv = document.getElementById(`chapter-content-${chapterId}`);
    if (contentDiv) {
      contentDiv.innerHTML = newContent;
      
      if (isUrdu) {
        contentDiv.setAttribute('dir', 'rtl');
        contentDiv.classList.add('urdu-content');
      } else {
        contentDiv.removeAttribute('dir');
        contentDiv.classList.remove('urdu-content');
      }
    }
    
    // Call parent handler if provided
    if (onContentChange) {
      onContentChange(newContent);
    }
  }, [chapterId, onContentChange]);

  // Handle restore to original
  const handleRestoreOriginal = useCallback(() => {
    setCurrentContent(originalContent);
    setIsUrduMode(false);
    setIsPersonalized(false);
    setPersonalizedContent(null);
    setUrduContent(null);
    
    const contentDiv = document.getElementById(`chapter-content-${chapterId}`);
    if (contentDiv) {
      contentDiv.innerHTML = originalContent;
      contentDiv.removeAttribute('dir');
      contentDiv.classList.remove('urdu-content');
    }
    
    if (onContentChange) {
      onContentChange(originalContent);
    }
  }, [originalContent, chapterId, onContentChange]);

  // Get content to send to API (always the current displayed content)
  const getContentForAPI = () => {
    return currentContent;
  };

  // Loading skeleton component
  const LoadingSkeleton = () => (
    <div className="content-loading">
      <div className="skeleton skeleton-heading" />
      <div className="skeleton skeleton-text long" />
      <div className="skeleton skeleton-text medium" />
      <div className="skeleton skeleton-text short" />
      <div className="skeleton skeleton-code" />
      <div className="skeleton skeleton-text long" />
      <div className="skeleton skeleton-text medium" />
      <div className="skeleton skeleton-text long" />
    </div>
  );

  return (
    <div className="chapter-toolbar-wrapper">
      {/* Toolbar with both buttons */}
      <div className="chapter-toolbar" style={{
        display: 'flex',
        gap: '1rem',
        alignItems: 'center',
        flexWrap: 'wrap',
        marginBottom: '2rem',
        padding: '1rem',
        backgroundColor: 'var(--ifm-background-surface-color)',
        borderRadius: '8px',
        border: '1px solid var(--ifm-color-emphasis-200)',
      }}>
        {/* Personalize Button (only show if logged in) */}
        {isAuthenticated && (
          <PersonalizeButton
            chapterContent={getContentForAPI()}
            chapterId={chapterId}
            onContentChange={(newContent) => handleContentChange(newContent, false)}
          />
        )}

        {/* Urdu Translate Button */}
        <UrduTranslateButton
          chapterContent={getContentForAPI()}
          chapterId={chapterId}
          chapterTitle={chapterTitle}
          onContentChange={handleContentChange}
          isUrduMode={isUrduMode}
          onUrduModeChange={setIsUrduMode}
        />

        {/* Restore Original Button (show when personalized or translated) */}
        {(isPersonalized || isUrduMode) && (
          <button
            onClick={handleRestoreOriginal}
            style={{
              padding: '0.75rem 1.5rem',
              fontSize: '0.95rem',
              fontWeight: 600,
              color: 'white',
              backgroundColor: 'var(--ifm-color-secondary)',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'var(--ifm-color-secondary-dark)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'var(--ifm-color-secondary)';
            }}
          >
            🔄 Restore Original
          </button>
        )}
      </div>

      {/* Loading Skeleton Overlay */}
      {isLoading && (
        <div className={`loading-overlay ${loadingType === 'translate' ? 'urdu-loading' : 'personalize-loading'}`}>
          <LoadingSkeleton />
        </div>
      )}

      {/* Hidden div to store current content for DOM updates */}
      <div
        id={`chapter-content-${chapterId}`}
        className={`markdown ${isUrduMode ? 'urdu-content' : ''}`}
        dir={isUrduMode ? 'rtl' : undefined}
        style={{ display: 'none' }}
        dangerouslySetInnerHTML={{ __html: currentContent }}
      />
    </div>
  );
};

export default ChapterToolbar;
