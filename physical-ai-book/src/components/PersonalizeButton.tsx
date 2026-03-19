import React, { useState, useCallback } from 'react';

interface UserProfile {
  experience_level: 'beginner' | 'intermediate' | 'advanced';
  software_background: string;
  hardware_background: string;
  learning_goal: string;
}

interface PersonalizeButtonProps {
  chapterContent: string;
  chapterId: string;
  onContentChange?: (newContent: string) => void;
}

interface PersonalizeRequest {
  chapter_content: string;
  user_profile: UserProfile;
}

interface PersonalizeResponse {
  personalized_content: string;
}

interface User {
  experience_level: string;
  software_background: string;
  hardware_background: string;
  learning_goal: string;
}

const PersonalizeButton: React.FC<PersonalizeButtonProps> = ({
  chapterContent,
  chapterId,
  onContentChange,
}) => {
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [originalContent, setOriginalContent] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Get user profile from localStorage (set during login)
  const getUserProfile = (): UserProfile | null => {
    try {
      const userData = localStorage.getItem('user_data');
      if (userData) {
        const user: User = JSON.parse(userData);
        return {
          experience_level: user.experience_level || 'beginner',
          software_background: user.software_background || '',
          hardware_background: user.hardware_background || '',
          learning_goal: user.learning_goal || '',
        };
      }
    } catch (e) {
      console.error('Error parsing user data:', e);
    }
    return null;
  };

  const handlePersonalize = useCallback(async () => {
    const userProfile = getUserProfile();
    
    if (!userProfile) {
      setError('Please log in to personalize content');
      return;
    }

    setIsPersonalizing(true);
    setError(null);

    try {
      // Store original content for restore functionality
      if (!originalContent) {
        setOriginalContent(chapterContent);
      }

      const requestPayload: PersonalizeRequest = {
        chapter_content: chapterContent,
        user_profile: userProfile,
      };

      const response = await fetch('http://localhost:8000/api/personalize-chapter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestPayload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to personalize content');
      }

      const data: PersonalizeResponse = await response.json();
      
      // Update the chapter content with personalized version
      const contentDiv = document.getElementById(`chapter-content-${chapterId}`);
      if (contentDiv && onContentChange) {
        onContentChange(data.personalized_content);
      } else if (contentDiv) {
        contentDiv.innerHTML = data.personalized_content;
      }

      setIsPersonalized(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      // Restore original content on error
      if (originalContent) {
        const contentDiv = document.getElementById(`chapter-content-${chapterId}`);
        if (contentDiv) {
          contentDiv.innerHTML = originalContent;
        }
      }
    } finally {
      setIsPersonalizing(false);
    }
  }, [chapterContent, chapterId, originalContent, onContentChange]);

  const handleRestoreOriginal = useCallback(() => {
    if (originalContent) {
      const contentDiv = document.getElementById(`chapter-content-${chapterId}`);
      if (contentDiv && onContentChange) {
        onContentChange(originalContent);
      } else if (contentDiv) {
        contentDiv.innerHTML = originalContent;
      }
      setIsPersonalized(false);
      setOriginalContent(null);
      setError(null);
    }
  }, [originalContent, chapterId, onContentChange]);

  // Check if user is logged in
  const isLoggedIn = !!localStorage.getItem('user_data');
  
  // Don't show button if user is not logged in
  if (!isLoggedIn) {
    return null;
  }

  const user = getUserProfile();

  return (
    <div className="personalize-button-container" style={{
      marginBottom: '2rem',
      padding: '1rem',
      backgroundColor: 'var(--ifm-color-primary-lightest)',
      borderRadius: '8px',
      border: '1px solid var(--ifm-color-primary-lighter)',
    }}>
      <div style={{
        display: 'flex',
        gap: '1rem',
        alignItems: 'center',
        flexWrap: 'wrap',
      }}>
        {!isPersonalized ? (
          <button
            onClick={handlePersonalize}
            disabled={isPersonalizing}
            style={{
              padding: '0.75rem 1.5rem',
              fontSize: '1rem',
              fontWeight: 600,
              color: 'white',
              backgroundColor: isPersonalizing 
                ? 'var(--ifm-color-primary-dark)' 
                : 'var(--ifm-color-primary)',
              border: 'none',
              borderRadius: '6px',
              cursor: isPersonalizing ? 'not-allowed' : 'pointer',
              transition: 'all 0.2s ease',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
            onMouseEnter={(e) => {
              if (!isPersonalizing) {
                e.currentTarget.style.backgroundColor = 'var(--ifm-color-primary-darker)';
              }
            }}
            onMouseLeave={(e) => {
              if (!isPersonalizing) {
                e.currentTarget.style.backgroundColor = 'var(--ifm-color-primary)';
              }
            }}
          >
            {isPersonalizing ? (
              <>
                <svg
                  style={{
                    width: '20px',
                    height: '20px',
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
                <span>Personalizing...</span>
              </>
            ) : (
              <>
                <svg
                  style={{ width: '20px', height: '20px' }}
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M12 6V12L16 14M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <span>Personalize for Me</span>
              </>
            )}
          </button>
        ) : (
          <button
            onClick={handleRestoreOriginal}
            style={{
              padding: '0.75rem 1.5rem',
              fontSize: '1rem',
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
              style={{ width: '20px', height: '20px' }}
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M3 10V12C3 16.9706 7.02944 21 12 21C16.9706 21 21 16.9706 21 12V8M7 8V4C7 3.44772 7.44772 3 8 3H16C16.5523 3 17 3.44772 17 4V8M12 12V16M12 12L9 15M12 12L15 15"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <span>Restore Original</span>
          </button>
        )}

        {user && (
          <span style={{
            color: 'var(--ifm-color-emphasis-700)',
            fontSize: '0.9rem',
          }}>
            Personalizing for: <strong>{user.experience_level || 'Beginner'}</strong> level
          </span>
        )}
      </div>

      {error && (
        <div style={{
          marginTop: '1rem',
          padding: '0.75rem',
          backgroundColor: 'var(--ifm-color-danger-lightest)',
          border: '1px solid var(--ifm-color-danger-lighter)',
          borderRadius: '4px',
          color: 'var(--ifm-color-danger)',
          fontSize: '0.9rem',
        }}>
          ⚠️ {error}
        </div>
      )}

      <style>{`
        @keyframes spin {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </div>
  );
};

export default PersonalizeButton;
