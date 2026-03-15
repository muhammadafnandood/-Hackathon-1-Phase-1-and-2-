/**
 * RAG Chatbot Widget for Docusaurus
 * 
 * A floating chat widget that provides AI-powered answers based on textbook content.
 * 
 * Installation:
 * 1. Copy this file to your Docusaurus project's static/js folder
 * 2. Add the script to your docusaurus.config.js
 * 3. Customize the API_URL to point to your backend
 */

(function() {
  // Configuration
  const CONFIG = {
    API_URL: window.CHATBOT_API_URL || 'http://localhost:8000',
    BOT_NAME: 'Textbook Assistant',
    BOT_AVATAR: '🤖',
    USER_AVATAR: '👤',
    THEME_COLOR: '#2563eb',
    POSITION: 'bottom-right', // 'bottom-right' or 'bottom-left'
  };

  // Expose openChat function globally for custom buttons
  window.openChat = function() {
    const chatWindow = document.getElementById('rag-chatbot-window');
    const chatIcon = document.getElementById('rag-chatbot-icon-chat');
    const closeIcon = document.getElementById('rag-chatbot-icon-close');
    if (chatWindow && chatIcon && closeIcon) {
      chatWindow.style.display = 'flex';
      chatIcon.style.display = 'none';
      closeIcon.style.display = 'block';
      document.getElementById('rag-chatbot-input')?.focus();
    }
  };

  // Text Selection Q&A Feature
  function initTextSelection() {
    let selectionTimeout;
    
    document.addEventListener('mouseup', function(e) {
      // Don't trigger if clicking inside chat widget
      if (e.target.closest('#rag-chatbot-widget')) return;
      
      clearTimeout(selectionTimeout);
      
      selectionTimeout = setTimeout(function() {
        const selection = window.getSelection();
        const selectedText = selection.toString().trim();
        
        // Show popup if text is selected (min 10 chars)
        if (selectedText.length > 10) {
          showSelectionPopup(selectedText, selection);
        }
      }, 300);
    });
    
    document.addEventListener('mousedown', function(e) {
      // Clear timeout on new mousedown
      clearTimeout(selectionTimeout);
    });
  }
  
  function showSelectionPopup(text, selection) {
    // Remove existing popup if any
    const existing = document.getElementById('selection-ai-popup');
    if (existing) existing.remove();
    
    // Get selection range for positioning
    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    
    // Create popup
    const popup = document.createElement('div');
    popup.id = 'selection-ai-popup';
    popup.innerHTML = `
      <div class="selection-popup-content">
        <span class="selection-popup-icon">💬</span>
        <span class="selection-popup-text">Ask AI about this</span>
      </div>
    `;
    
    // Position popup above selection
    popup.style.position = 'fixed';
    popup.style.left = (rect.left + (rect.width / 2) - 80) + 'px';
    popup.style.top = (rect.top - 45 + window.scrollY) + 'px';
    popup.style.zIndex = '10000';
    
    // Add click handler
    popup.addEventListener('click', function() {
      openChatWithSelection(text);
      popup.remove();
    });
    
    document.body.appendChild(popup);
    
    // Auto-hide after 5 seconds
    setTimeout(function() {
      if (popup.parentNode) popup.remove();
    }, 5000);
  }
  
  function openChatWithSelection(selectedText) {
    // Open chat window
    const chatWindow = document.getElementById('rag-chatbot-window');
    const chatIcon = document.getElementById('rag-chatbot-icon-chat');
    const closeIcon = document.getElementById('rag-chatbot-icon-close');
    
    if (chatWindow && chatIcon && closeIcon) {
      chatWindow.style.display = 'flex';
      chatIcon.style.display = 'none';
      closeIcon.style.display = 'block';
    }
    
    // Pre-fill input with selected text as context
    const input = document.getElementById('rag-chatbot-input');
    if (input) {
      input.value = 'Explain this: "' + selectedText + '"';
      input.focus();
    }
  }

  // Chat state
  let isOpen = false;
  let isLoading = false;
  let chatHistory = [];

  // Create widget HTML
  function createWidget() {
    const widgetHTML = `
      <div id="rag-chatbot-widget">
        <!-- Chat Button -->
        <button id="rag-chatbot-toggle" aria-label="Toggle chat">
          <svg id="rag-chatbot-icon-chat" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
          <svg id="rag-chatbot-icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>

        <!-- Chat Window -->
        <div id="rag-chatbot-window" style="display: none;">
          <!-- Header -->
          <div id="rag-chatbot-header">
            <div class="rag-chatbot-header-title">
              <span class="rag-chatbot-avatar">${CONFIG.BOT_AVATAR}</span>
              <span>${CONFIG.BOT_NAME}</span>
            </div>
            <button id="rag-chatbot-close" aria-label="Close chat">×</button>
          </div>

          <!-- Messages -->
          <div id="rag-chatbot-messages">
            <div class="rag-chatbot-message rag-chatbot-bot-message">
              <div class="rag-chatbot-message-avatar">${CONFIG.BOT_AVATAR}</div>
              <div class="rag-chatbot-message-content">
                Hi! I'm your textbook assistant. Ask me anything about Physical AI, humanoid robotics, ROS 2, or related topics!
              </div>
            </div>
          </div>

          <!-- Input -->
          <div id="rag-chatbot-input-container">
            <textarea 
              id="rag-chatbot-input" 
              placeholder="Ask a question..." 
              rows="1"
              maxlength="2000"
            ></textarea>
            <button id="rag-chatbot-send" aria-label="Send message" ${isLoading ? 'disabled' : ''}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>

          <!-- Sources Panel -->
          <div id="rag-chatbot-sources" style="display: none;">
            <div class="rag-chatbot-sources-title">📚 Sources</div>
            <div id="rag-chatbot-sources-list"></div>
          </div>
        </div>
      </div>
    `;

    // Add to DOM
    document.body.insertAdjacentHTML('beforeend', widgetHTML);

    // Add styles
    addStyles();

    // Attach event listeners
    attachEventListeners();
  }

  // Add CSS styles
  function addStyles() {
    const styles = `
      <style>
        #rag-chatbot-widget {
          position: fixed;
          ${CONFIG.POSITION === 'bottom-left' ? 'left' : 'right'}: 20px;
          bottom: 20px;
          z-index: 9999;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        }

        /* Toggle Button */
        #rag-chatbot-toggle {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background: ${CONFIG.THEME_COLOR};
          border: none;
          cursor: pointer;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          transition: transform 0.2s, box-shadow 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        #rag-chatbot-toggle:hover {
          transform: scale(1.1);
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        }

        #rag-chatbot-toggle svg {
          width: 28px;
          height: 28px;
          color: white;
        }

        /* Chat Window */
        #rag-chatbot-window {
          position: absolute;
          ${CONFIG.POSITION === 'bottom-left' ? 'left' : 'right'}: 0;
          bottom: 80px;
          width: 380px;
          height: 600px;
          max-height: calc(100vh - 100px);
          background: white;
          border-radius: 16px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          animation: rag-slide-up 0.3s ease-out;
        }

        @keyframes rag-slide-up {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        /* Header */
        #rag-chatbot-header {
          background: ${CONFIG.THEME_COLOR};
          color: white;
          padding: 16px 20px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .rag-chatbot-header-title {
          display: flex;
          align-items: center;
          gap: 10px;
          font-weight: 600;
          font-size: 16px;
        }

        .rag-chatbot-avatar {
          font-size: 24px;
        }

        #rag-chatbot-close {
          background: none;
          border: none;
          color: white;
          font-size: 28px;
          cursor: pointer;
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          transition: background 0.2s;
        }

        #rag-chatbot-close:hover {
          background: rgba(255, 255, 255, 0.2);
        }

        /* Messages */
        #rag-chatbot-messages {
          flex: 1;
          overflow-y: auto;
          padding: 16px;
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .rag-chatbot-message {
          display: flex;
          gap: 8px;
          max-width: 85%;
        }

        .rag-chatbot-user-message {
          align-self: flex-end;
          flex-direction: row-reverse;
        }

        .rag-chatbot-bot-message {
          align-self: flex-start;
        }

        .rag-chatbot-message-avatar {
          font-size: 24px;
          flex-shrink: 0;
        }

        .rag-chatbot-message-content {
          background: #f1f5f9;
          padding: 12px 16px;
          border-radius: 12px;
          font-size: 14px;
          line-height: 1.5;
          white-space: pre-wrap;
          word-break: break-word;
        }

        .rag-chatbot-user-message .rag-chatbot-message-content {
          background: ${CONFIG.THEME_COLOR};
          color: white;
        }

        /* Loading */
        .rag-chatbot-loading {
          display: flex;
          gap: 4px;
          padding: 12px 16px;
        }

        .rag-chatbot-loading-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #94a3b8;
          animation: rag-bounce 1.4s infinite ease-in-out;
        }

        .rag-chatbot-loading-dot:nth-child(1) { animation-delay: -0.32s; }
        .rag-chatbot-loading-dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes rag-bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }

        /* Input */
        #rag-chatbot-input-container {
          display: flex;
          gap: 8px;
          padding: 16px;
          border-top: 1px solid #e2e8f0;
          background: white;
        }

        #rag-chatbot-input {
          flex: 1;
          border: 1px solid #e2e8f0;
          border-radius: 20px;
          padding: 12px 16px;
          font-size: 14px;
          resize: none;
          max-height: 120px;
          font-family: inherit;
          outline: none;
          transition: border-color 0.2s;
        }

        #rag-chatbot-input:focus {
          border-color: ${CONFIG.THEME_COLOR};
        }

        #rag-chatbot-send {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: ${CONFIG.THEME_COLOR};
          border: none;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background 0.2s, transform 0.2s;
        }

        #rag-chatbot-send:hover:not(:disabled) {
          background: #1d4ed8;
          transform: scale(1.05);
        }

        #rag-chatbot-send:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        #rag-chatbot-send svg {
          width: 18px;
          height: 18px;
          color: white;
        }

        /* Sources */
        #rag-chatbot-sources {
          border-top: 1px solid #e2e8f0;
          padding: 12px 16px;
          background: #f8fafc;
          max-height: 200px;
          overflow-y: auto;
        }

        .rag-chatbot-sources-title {
          font-weight: 600;
          font-size: 13px;
          color: #64748b;
          margin-bottom: 8px;
        }

        #rag-chatbot-sources-list {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }

        .rag-chatbot-source {
          background: white;
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          padding: 8px 12px;
          font-size: 12px;
          cursor: pointer;
          transition: border-color 0.2s;
        }

        .rag-chatbot-source:hover {
          border-color: ${CONFIG.THEME_COLOR};
        }

        .rag-chatbot-source-title {
          font-weight: 600;
          color: #1e293b;
          margin-bottom: 4px;
        }

        .rag-chatbot-source-score {
          color: #94a3b8;
          font-size: 11px;
        }

        /* Scrollbar */
        #rag-chatbot-messages::-webkit-scrollbar,
        #rag-chatbot-sources::-webkit-scrollbar {
          width: 6px;
        }

        #rag-chatbot-messages::-webkit-scrollbar-track,
        #rag-chatbot-sources::-webkit-scrollbar-track {
          background: #f1f5f9;
        }

        #rag-chatbot-messages::-webkit-scrollbar-thumb,
        #rag-chatbot-sources::-webkit-scrollbar-thumb {
          background: #cbd5e1;
          border-radius: 3px;
        }

        #rag-chatbot-messages::-webkit-scrollbar-thumb:hover,
        #rag-chatbot-sources::-webkit-scrollbar-thumb:hover {
          background: #94a3b8;
        }

        /* Mobile */
        @media (max-width: 480px) {
          #rag-chatbot-window {
            width: calc(100vw - 40px);
            height: calc(100vh - 120px);
            bottom: 80px;
          }
        }

        /* Text Selection Popup */
        .selection-popup-content {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 10px 16px;
          border-radius: 24px;
          display: flex;
          align-items: center;
          gap: 8px;
          cursor: pointer;
          box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
          animation: selection-popup-appear 0.2s ease-out;
          white-space: nowrap;
        }

        @keyframes selection-popup-appear {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .selection-popup-icon {
          font-size: 18px;
        }

        .selection-popup-text {
          font-size: 13px;
          font-weight: 600;
        }

        /* Chapter Citation Styles */
        .rag-chatbot-citation {
          margin-top: 12px;
          padding-top: 12px;
          border-top: 1px solid rgba(0, 0, 0, 0.1);
          font-size: 12px;
          color: #64748b;
        }

        .rag-chatbot-citation-title {
          font-weight: 600;
          color: #475569;
          margin-bottom: 6px;
          display: flex;
          align-items: center;
          gap: 4px;
        }

        .rag-chatbot-citation-item {
          background: #f1f5f9;
          padding: 6px 10px;
          border-radius: 6px;
          margin-top: 4px;
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .rag-chatbot-citation-item:before {
          content: "📖";
          font-size: 12px;
        }
      </style>
    `;

    document.head.insertAdjacentHTML('beforeend', styles);
    
    // Initialize text selection feature
    initTextSelection();
  }

  // Attach event listeners
  function attachEventListeners() {
    const toggleBtn = document.getElementById('rag-chatbot-toggle');
    const closeBtn = document.getElementById('rag-chatbot-close');
    const sendBtn = document.getElementById('rag-chatbot-send');
    const input = document.getElementById('rag-chatbot-input');
    const chatIcon = document.getElementById('rag-chatbot-icon-chat');
    const closeIcon = document.getElementById('rag-chatbot-icon-close');

    // Toggle chat
    toggleBtn.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', closeChat);

    // Send message
    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    // Auto-resize textarea
    input.addEventListener('input', () => {
      input.style.height = 'auto';
      input.style.height = Math.min(input.scrollHeight, 120) + 'px';
    });
  }

  // Toggle chat window
  function toggleChat() {
    isOpen = !isOpen;
    const window = document.getElementById('rag-chatbot-window');
    const chatIcon = document.getElementById('rag-chatbot-icon-chat');
    const closeIcon = document.getElementById('rag-chatbot-icon-close');

    if (isOpen) {
      window.style.display = 'flex';
      chatIcon.style.display = 'none';
      closeIcon.style.display = 'block';
      document.getElementById('rag-chatbot-input').focus();
    } else {
      window.style.display = 'none';
      chatIcon.style.display = 'block';
      closeIcon.style.display = 'none';
    }
  }

  // Close chat
  function closeChat() {
    isOpen = false;
    const window = document.getElementById('rag-chatbot-window');
    const chatIcon = document.getElementById('rag-chatbot-icon-chat');
    const closeIcon = document.getElementById('rag-chatbot-icon-close');

    window.style.display = 'none';
    chatIcon.style.display = 'block';
    closeIcon.style.display = 'none';
  }

  // Add message to chat
  function addMessage(content, isUser = false, citations = []) {
    const messagesContainer = document.getElementById('rag-chatbot-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `rag-chatbot-message ${isUser ? 'rag-chatbot-user-message' : 'rag-chatbot-bot-message'}`;

    let citationsHTML = '';
    if (!isUser && citations.length > 0) {
      citationsHTML = `
        <div class="rag-chatbot-citation">
          <div class="rag-chatbot-citation-title">📚 Source:</div>
          ${citations.map(cite => `
            <div class="rag-chatbot-citation-item">${escapeHtml(cite)}</div>
          `).join('')}
        </div>
      `;
    }

    messageDiv.innerHTML = `
      <div class="rag-chatbot-message-avatar">${isUser ? CONFIG.USER_AVATAR : CONFIG.BOT_AVATAR}</div>
      <div class="rag-chatbot-message-content">
        ${escapeHtml(content)}
        ${citationsHTML}
      </div>
    `;

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Show loading indicator
  function showLoading() {
    const messagesContainer = document.getElementById('rag-chatbot-messages');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'rag-chatbot-loading';
    loadingDiv.id = 'rag-chatbot-loading';
    loadingDiv.innerHTML = `
      <div class="rag-chatbot-loading-dot"></div>
      <div class="rag-chatbot-loading-dot"></div>
      <div class="rag-chatbot-loading-dot"></div>
    `;
    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Hide loading indicator
  function hideLoading() {
    const loading = document.getElementById('rag-chatbot-loading');
    if (loading) loading.remove();
  }

  // Show sources
  function showSources(sources) {
    const sourcesPanel = document.getElementById('rag-chatbot-sources');
    const sourcesList = document.getElementById('rag-chatbot-sources-list');

    if (!sources || sources.length === 0) {
      sourcesPanel.style.display = 'none';
      return;
    }

    sourcesList.innerHTML = sources.map(source => `
      <div class="rag-chatbot-source">
        <div class="rag-chatbot-source-title">📖 ${escapeHtml(source.chapter)}${source.section ? ' – ' + escapeHtml(source.section) : ''}</div>
        <div class="rag-chatbot-source-score">Relevance: ${(source.score * 100).toFixed(0)}%</div>
      </div>
    `).join('');

    sourcesPanel.style.display = 'block';
  }

  // Send message
  async function sendMessage() {
    const input = document.getElementById('rag-chatbot-input');
    const query = input.value.trim();

    if (!query || isLoading) return;

    // Add user message
    addMessage(query, true);
    input.value = '';
    input.style.height = 'auto';

    // Show loading
    showLoading();
    isLoading = true;
    document.getElementById('rag-chatbot-send').disabled = true;

    try {
      // Call API
      const response = await fetch(`${CONFIG.API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: query,
          top_k: 5,
          include_sources: true,
        }),
      });

      if (!response.ok) {
        throw new Error('API error');
      }

      const data = await response.json();

      // Hide loading
      hideLoading();

      // Extract chapter citations from sources
      const citations = [];
      if (data.sources && data.sources.length > 0) {
        data.sources.forEach(source => {
          const citation = `${source.chapter}${source.section ? ' – ' + source.section : ''}`;
          if (!citations.includes(citation)) {
            citations.push(citation);
          }
        });
      }

      // Add bot response with citations
      addMessage(data.answer, false, citations);

      // Show sources panel
      showSources(data.sources);

      // Add to history
      chatHistory.push({ query, response: data.answer });

    } catch (error) {
      hideLoading();
      addMessage('Sorry, I encountered an error. Please check your connection and try again.');
      console.error('Chat error:', error);
    } finally {
      isLoading = false;
      document.getElementById('rag-chatbot-send').disabled = false;
      document.getElementById('rag-chatbot-input').focus();
    }
  }

  // Escape HTML
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Initialize widget when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createWidget);
  } else {
    createWidget();
  }
})();
