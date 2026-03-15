import React, { useState, useRef, useEffect } from 'react';
import './AIChatbot.css';

const AIChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "👋 Hi! I'm your Physical AI assistant. Ask me anything about the book!",
      sender: 'bot',
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Format chapter name to URL slug
  const formatChapterToSlug = (chapterName) => {
    if (!chapterName) return 'unknown';
    return chapterName.toLowerCase().replace(/\s+/g, '');
  };

  // Format chapter display name
  const formatChapterDisplay = (source) => {
    const chapter = source.chapter_id || source.chapter || 'Unknown Chapter';
    const heading = source.heading ? ` - ${heading}` : '';
    // Add space between "Chapter" and number if not present
    return chapter.replace(/Chapter(\d+)/, 'Chapter $1') + heading;
  };

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
    if (!isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 300);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      // Calculate confidence from source scores if not provided
      let confidence = null;
      if (data.sources && data.sources.length > 0) {
        const avgScore = data.sources.reduce((sum, s) => sum + (s.score || 0), 0) / data.sources.length;
        confidence = Math.round(avgScore * 100);
      }

      const botMessage = {
        id: Date.now() + 1,
        text: data.response || "I'm not sure about that. Could you rephrase?",
        sender: 'bot',
        sources: data.sources || [],
        confidence: confidence,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage = {
        id: Date.now() + 1,
        text: "⚠️ Sorry, I'm having trouble connecting. Please make sure the backend is running.",
        sender: 'bot',
        error: true,
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  return (
    <>
      {/* Floating Toggle Button */}
      <button
        className={`chatbot-toggle ${isOpen ? 'open' : ''}`}
        onClick={toggleChatbot}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        <div className="toggle-icon">
          {isOpen ? (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 6L6 18M6 6L18 18" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          ) : (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15C21 15.53 20.79 16.04 20.41 16.41C20.04 16.79 19.53 17 19 17H7L3 21V7C3 6.47 3.21 5.96 3.59 5.59C3.96 5.21 4.47 5 5 5H19C19.53 5 20.04 5.21 20.41 5.59C20.79 5.96 21 6.47 21 7V15Z" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          )}
        </div>
        {!isOpen && <span className="notification-dot"></span>}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chatbot-window">
          {/* Header */}
          <div className="chatbot-header">
            <div className="header-content">
              <div className="bot-avatar">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 16V12M12 8H12.01"/>
                </svg>
              </div>
              <div className="header-info">
                <h3>AI Assistant</h3>
                <span className="status-indicator">
                  <span className="status-dot"></span>
                  Online
                </span>
              </div>
            </div>
            <button className="close-btn" onClick={toggleChatbot} aria-label="Close chat">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M18 6L6 18M6 6L18 18" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>

          {/* Messages Area */}
          <div className="chatbot-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'} ${message.error ? 'error-message' : ''}`}
              >
                <div className="message-avatar">
                  {message.sender === 'user' ? (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  ) : (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <circle cx="12" cy="12" r="10"/>
                      <path d="M12 16V12M12 8H12.01"/>
                    </svg>
                  )}
                </div>
                <div className="message-body">
                  <div className="message-content">
                    <div className="message-text">{message.text}</div>

                    {/* Confidence Score */}
                    {message.confidence !== null && message.sender === 'bot' && !message.error && (
                      <div className="confidence-section">
                        <div className="confidence-bar-wrapper">
                          <div
                            className="confidence-bar-fill"
                            style={{
                              width: `${message.confidence}%`,
                              background: message.confidence >= 80
                                ? 'linear-gradient(90deg, #4CAF50, #8BC34A)'
                                : message.confidence >= 60
                                ? 'linear-gradient(90deg, #FFC107, #FFEB3B)'
                                : 'linear-gradient(90deg, #FF5722, #FF7043)',
                            }}
                          />
                        </div>
                        <span className="confidence-percentage">{message.confidence}%</span>
                      </div>
                    )}

                    {/* Sources */}
                    {message.sources && message.sources.length > 0 && message.sender === 'bot' && !message.error && (
                      <div className="sources-container">
                        <div className="sources-header">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M4 19.5C4 19.5 4 8.2 4 5.5C4 3.5 5.5 2 7.5 2C9.5 2 20 2 20 2V19.5C20 20.5 19.5 21 18.5 21H5.5C4.5 21 4 20.5 4 19.5Z" strokeLinecap="round" strokeLinejoin="round"/>
                            <path d="M8 7H14" strokeLinecap="round" strokeLinejoin="round"/>
                            <path d="M8 11H16" strokeLinecap="round" strokeLinejoin="round"/>
                          </svg>
                          <span>Sources</span>
                        </div>
                        <div className="sources-list">
                          {message.sources.map((source, index) => {
                            const slug = formatChapterToSlug(source.chapter_id || source.chapter);
                            const display = formatChapterDisplay(source);
                            return (
                              <a
                                key={index}
                                href={`/docs/${slug}`}
                                className="source-chip"
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                  <path d="M18 13V19C18 19.5304 17.7893 20.0391 17.4142 20.4142C17.0391 20.7893 16.5304 21 16 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H16" strokeLinecap="round" strokeLinejoin="round"/>
                                  <path d="M15 3H21V9" strokeLinecap="round" strokeLinejoin="round"/>
                                  <path d="M10 14L21 3" strokeLinecap="round" strokeLinejoin="round"/>
                                </svg>
                                <span>{display}</span>
                              </a>
                            );
                          })}
                        </div>
                      </div>
                    )}
                  </div>
                  <span className="message-time">
                    {new Date(message.id).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>
            ))}

            {/* Loading Indicator */}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-avatar">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 16V12M12 8H12.01"/>
                  </svg>
                </div>
                <div className="message-body">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <form className="chatbot-input-area" onSubmit={handleSendMessage}>
            <div className="input-wrapper">
              <input
                ref={inputRef}
                type="text"
                className="chatbot-input"
                placeholder="Ask a question about the book..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={isLoading}
                autoComplete="off"
              />
              <button
                type="submit"
                className="send-button"
                disabled={isLoading || !inputValue.trim()}
                aria-label="Send message"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
};

export default AIChatbot;
