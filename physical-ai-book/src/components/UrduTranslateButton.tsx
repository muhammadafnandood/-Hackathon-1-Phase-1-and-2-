import React, { useState, useCallback } from 'react';

interface UrduTranslateButtonProps {
  chapterContent: string;
  chapterId: string;
  chapterTitle: string;
  onContentChange?: (newContent: string, isUrdu: boolean) => void;
  isUrduMode?: boolean;
  onUrduModeChange?: (isUrdu: boolean) => void;
}

interface TranslateRequest {
  chapter_id: string;
  chapter_content: string;
  chapter_title: string;
}

interface TranslateResponse {
  urdu_content: string;
  is_cached: boolean;
}

const UrduTranslateButton: React.FC<UrduTranslateButtonProps> = ({
  chapterContent,
  chapterId,
  chapterTitle,
  onContentChange,
  isUrduMode = false,
  onUrduModeChange,
}) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [originalContent, setOriginalContent] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTranslateToUrdu = useCallback(async () => {
    setIsTranslating(true);
    setError(null);

    try {
      // Store original content for restore functionality
      if (!originalContent) {
        setOriginalContent(chapterContent);
      }

      const requestPayload: TranslateRequest = {
        chapter_id: chapterId,
        chapter_content: chapterContent,
        chapter_title: chapterTitle,
      };

      const response = await fetch('http://localhost:8000/api/translate-urdu', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestPayload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Translation failed');
      }

      const data: TranslateResponse = await response.json();

      // Update content with Urdu translation
      if (onContentChange) {
        onContentChange(data.urdu_content, true);
      } else {
        // Fallback: update DOM directly
        const contentDiv = document.getElementById(`chapter-content-${chapterId}`);
        if (contentDiv) {
          contentDiv.innerHTML = data.urdu_content;
          contentDiv.setAttribute('dir', 'rtl');
          contentDiv.classList.add('urdu-content');
        }
      }

      // Update Urdu mode state
      if (onUrduModeChange) {
        onUrduModeChange(true);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred during translation');
      // Restore original content on error
      if (originalContent) {
        const contentDiv = document.getElementById(`chapter-content-${chapterId}`);
        if (contentDiv) {
          contentDiv.innerHTML = originalContent;
          contentDiv.removeAttribute('dir');
          contentDiv.classList.remove('urdu-content');
        }
      }
    } finally {
      setIsTranslating(false);
    }
  }, [chapterContent, chapterId, chapterTitle, originalContent, onContentChange, onUrduModeChange]);

  const handleRestoreEnglish = useCallback(() => {
    if (originalContent) {
      // Restore original English content
      if (onContentChange) {
        onContentChange(originalContent, false);
      } else {
        // Fallback: update DOM directly
        const contentDiv = document.getElementById(`chapter-content-${chapterId}`);
        if (contentDiv) {
          contentDiv.innerHTML = originalContent;
          contentDiv.removeAttribute('dir');
          contentDiv.classList.remove('urdu-content');
        }
      }

      // Update Urdu mode state
      if (onUrduModeChange) {
        onUrduModeChange(false);
      }

      setOriginalContent(null);
      setError(null);
    }
  }, [originalContent, chapterId, onContentChange, onUrduModeChange]);

  return (
    <div className="urdu-translate-button-container" style={{
      display: 'inline-block',
    }}>
      {!isUrduMode ? (
        <button
          onClick={handleTranslateToUrdu}
          disabled={isTranslating}
          style={{
            padding: '0.75rem 1.5rem',
            fontSize: '1rem',
            fontWeight: 600,
            color: 'white',
            backgroundColor: isTranslating 
              ? '#059669' // Darker green when disabled
              : '#10b981', // Emerald green
            border: 'none',
            borderRadius: '6px',
            cursor: isTranslating ? 'not-allowed' : 'pointer',
            transition: 'all 0.2s ease',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            fontFamily: "'Noto Nastaliq Urdu', serif",
            direction: 'rtl',
          }}
          onMouseEnter={(e) => {
            if (!isTranslating) {
              e.currentTarget.style.backgroundColor = '#059669';
            }
          }}
          onMouseLeave={(e) => {
            if (!isTranslating) {
              e.currentTarget.style.backgroundColor = '#10b981';
            }
          }}
        >
          {isTranslating ? (
            <>
              <svg
                style={{
                  width: '18px',
                  height: '18px',
                  animation: 'spin 1s linear infinite',
                }}
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeOpacity="0.3"
                />
                <path
                  d="M12 2C6.47715 2 2 6.47715 2 12"
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
              </svg>
              <span>ترجمہ ہو رہا ہے...</span>
            </>
          ) : (
            <>
              <svg
                style={{ width: '18px', height: '18px' }}
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M3 5H21M3 12H21M3 19H21M8 5L8 19M16 5L16 19"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <span>اردو میں پڑھیں</span>
            </>
          )}
        </button>
      ) : (
        <button
          onClick={handleRestoreEnglish}
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
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--ifm-color-secondary-dark)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--ifm-color-secondary)';
          }}
        >
          <svg
            style={{ width: '18px', height: '18px' }}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M9 14L4 9L9 4M4 9H15C17.7614 9 20 11.2386 20 14M20 14L15 19M20 14L15 9"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span>انگریزی میں واپس جائیں</span>
        </button>
      )}

      {error && (
        <div style={{
          marginTop: '0.75rem',
          padding: '0.5rem 0.75rem',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          borderRadius: '4px',
          color: 'var(--ifm-color-danger)',
          fontSize: '0.85rem',
          direction: 'ltr',
          textAlign: 'left',
        }}>
          ⚠️ {error}
        </div>
      )}
    </div>
  );
};

export default UrduTranslateButton;
