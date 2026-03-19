import React, { useState, useRef, useEffect } from 'react';
import AnswerCard from './AnswerCard';

interface Message {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
  answerCard?: AnswerCardData;
}

interface AnswerCardData {
  book_answer: string | null;
  extended_knowledge: string;
  mermaid_diagram: string | 'NO_DIAGRAM';
  image_keywords: string[];
}

interface ChatbotProps {
  apiUrl?: string;
  chapterId?: string;
  userLevel?: string; // Add user level prop
}

const Chatbot: React.FC<ChatbotProps> = ({
  apiUrl = 'http://localhost:8000',
  chapterId = 'unknown',
  userLevel = 'Beginner', // Default to Beginner
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      type: 'bot',
      content: "Hello! I'm your Physical AI Assistant. Ask me anything about ROS 2, humanoid robotics, or this textbook!",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  // Get current chapter ID from URL or props
  useEffect(() => {
    const path = window.location.pathname;
    const chapterMatch = path.match(/chapter-(\d+)/);
    if (chapterMatch) {
      chapterId = `chapter-${chapterMatch[1]}`;
    }
    
    // Get user level from localStorage (set during login/profile setup)
    const userData = localStorage.getItem('user_data');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user.experience_level) {
          // Map experience_level to userLevel
          const levelMap: Record<string, string> = {
            'beginner': 'Beginner',
            'intermediate': 'Student', 
            'advanced': 'Engineer',
            'expert': 'Researcher'
          };
          userLevel = levelMap[user.experience_level] || 'Beginner';
        }
      } catch (e) {
        console.error('Error parsing user data:', e);
      }
    }
  }, []);

  const handleSendMessage = async (question?: string) => {
    const textToSend = question || inputValue.trim();
    if (!textToSend || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: textToSend,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // Add loading message with typing indicator
    const loadingMessageId = `loading-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      {
        id: loadingMessageId,
        type: 'bot',
        content: '',
        timestamp: new Date(),
      },
    ]);

    try {
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: textToSend,
          chapter_id: chapterId,
          user_level: userLevel, // Send user's expertise level
          conversation_history: messages
            .slice(-5)
            .map((m) => ({ role: m.type, content: m.content })),
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: AnswerCardData = await response.json();

      // Remove loading message
      setMessages((prev) => prev.filter((m) => m.id !== loadingMessageId));

      // Add bot response with AnswerCard
      const botMessage: Message = {
        id: Date.now().toString(),
        type: 'bot',
        content: generateBotResponseText(data),
        timestamp: new Date(),
        answerCard: data,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);

      // Remove loading message
      setMessages((prev) => prev.filter((m) => m.id !== loadingMessageId));

      // Add error message
      setMessages((prev) => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          type: 'bot',
          content: "I'm sorry, I encountered an error. Please try again.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const generateBotResponseText = (data: AnswerCardData): string => {
    let text = '';
    if (data.book_answer) {
      text += '📖 From the textbook: ';
    }
    text += 'Here\'s what I found...';
    return text;
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <>
      {/* Chat Toggle Button */}
      <button
        className={`chatbot-toggle ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        )}
      </button>

      {/* Chat Panel */}
      {isOpen && (
        <div className="chatbot-panel">
          {/* Header */}
          <div className="chatbot-header">
            <h3>AI Assistant</h3>
            <button onClick={() => setIsOpen(false)} aria-label="Close chat">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          {/* Messages */}
          <div className="chatbot-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.type} ${message.type === 'bot' && message.answerCard ? 'with-card' : ''}`}
              >
                <div className="message-bubble">
                  {message.content && <p>{message.content}</p>}

                  {/* Render AnswerCard for bot messages with data */}
                  {message.type === 'bot' && message.answerCard && (
                    <AnswerCard data={message.answerCard} />
                  )}

                  <span className="message-time">{formatTime(message.timestamp)}</span>
                </div>
              </div>
            ))}

            {/* Typing Indicator */}
            {isLoading && (
              <div className="message bot typing">
                <div className="message-bubble">
                  <div className="typing-indicator">
                    <span className="typing-dot"></span>
                    <span className="typing-dot"></span>
                    <span className="typing-dot"></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="chatbot-input">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question..."
              disabled={isLoading}
            />
            <button
              onClick={() => handleSendMessage()}
              disabled={isLoading || !inputValue.trim()}
              aria-label="Send message"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Styles */}
      <style>{`
        /* Chatbot Toggle Button */
        .chatbot-toggle {
          position: fixed;
          bottom: 24px;
          right: 24px;
          width: 56px;
          height: 56px;
          border-radius: 50%;
          background-color: #424242;
          color: white;
          border: none;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          transition: all 0.3s ease;
          z-index: 9999;
        }

        .chatbot-toggle:hover {
          background-color: #212121;
          transform: scale(1.05);
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        }

        .chatbot-toggle.open {
          background-color: #616161;
        }

        [data-theme='dark'] .chatbot-toggle {
          background-color: #333333;
        }

        [data-theme='dark'] .chatbot-toggle:hover {
          background-color: #424242;
        }

        /* Chatbot Panel */
        .chatbot-panel {
          position: fixed;
          bottom: 24px;
          right: 24px;
          width: 380px;
          height: 560px;
          background-color: #F5F5F5;
          border: 1px solid #BDBDBD;
          border-radius: 12px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          z-index: 9998;
          animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }

        [data-theme='dark'] .chatbot-panel {
          background-color: #1E1E1E;
          border-color: #3A3A3A;
        }

        /* Header */
        .chatbot-header {
          background-color: #2C2C2C;
          color: white;
          padding: 16px 20px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 1px solid #3A3A3A;
        }

        .chatbot-header h3 {
          margin: 0;
          font-size: 16px;
          font-weight: 600;
        }

        .chatbot-header button {
          background: none;
          border: none;
          color: white;
          cursor: pointer;
          padding: 4px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 4px;
        }

        .chatbot-header button:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }

        /* Messages */
        .chatbot-messages {
          flex: 1;
          overflow-y: auto;
          padding: 16px;
          display: flex;
          flex-direction: column;
          gap: 12px;
          min-height: 0; /* Important for flex child scrolling */
        }

        .message {
          display: flex;
          max-width: 100%;
        }

        .message.user {
          justify-content: flex-end;
        }

        .message.bot {
          justify-content: flex-start;
        }

        .message-bubble {
          max-width: 85%;
          padding: 10px 14px;
          border-radius: 12px;
          position: relative;
        }

        .message.user .message-bubble {
          background-color: #616161;
          color: white;
          border-bottom-right-radius: 4px;
        }

        .message.bot .message-bubble {
          background-color: #EEEEEE;
          color: #212121;
          border-bottom-left-radius: 4px;
        }

        [data-theme='dark'] .message.user .message-bubble {
          background-color: #424242;
        }

        [data-theme='dark'] .message.bot .message-bubble {
          background-color: #2C2C2C;
          color: #E8E8E8;
        }

        .message-bubble p {
          margin: 0 0 8px 0;
          line-height: 1.5;
        }

        .message-time {
          font-size: 11px;
          color: #9E9E9E;
          display: block;
          text-align: right;
        }

        .message.bot .message-time {
          color: #757575;
        }

        /* Typing Indicator */
        .typing-indicator {
          display: flex;
          gap: 4px;
          padding: 8px 0;
        }

        .typing-dot {
          width: 8px;
          height: 8px;
          background-color: #9E9E9E;
          border-radius: 50%;
          animation: typing 1.4s infinite;
        }

        .typing-dot:nth-child(2) {
          animation-delay: 0.2s;
        }

        .typing-dot:nth-child(3) {
          animation-delay: 0.4s;
        }

        @keyframes typing {
          0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.7;
          }
          30% {
            transform: translateY(-4px);
            opacity: 1;
          }
        }

        /* Input Area */
        .chatbot-input {
          display: flex;
          gap: 8px;
          padding: 16px;
          background-color: var(--ifm-background-surface-color);
          border-top: 1px solid var(--ifm-border-color);
          flex-shrink: 0; /* Prevent input area from shrinking */
        }

        .chatbot-input input {
          flex: 1;
          min-width: 0; /* Allow input to shrink if needed */
          padding: 10px 14px;
          border: 1px solid var(--ifm-input-border-color);
          border-radius: 8px;
          background-color: var(--ifm-input-background);
          color: var(--ifm-font-color-base);
          font-size: 14px;
          outline: none;
        }

        .chatbot-input input:focus {
          border-color: var(--ifm-color-primary);
        }

        .chatbot-input input:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .chatbot-input button {
          width: 40px;
          height: 40px;
          min-width: 40px; /* Prevent button from shrinking */
          border-radius: 8px;
          background-color: var(--ifm-color-primary);
          color: white;
          border: none;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.2s;
          flex-shrink: 0; /* Prevent button from shrinking */
        }

        .chatbot-input button:hover:not(:disabled) {
          background-color: var(--ifm-color-primary-dark);
          transform: scale(1.05);
        }

        .chatbot-input button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        /* Responsive */
        @media (max-width: 768px) {
          .chatbot-panel {
            bottom: 0;
            right: 0;
            left: 0;
            width: 100%;
            height: calc(100vh - 100px);
            border-radius: 12px 12px 0 0;
          }

          .chatbot-toggle {
            bottom: 16px;
            right: 16px;
            width: 52px;
            height: 52px;
          }
        }
      `}</style>
    </>
  );
};

export default Chatbot;
