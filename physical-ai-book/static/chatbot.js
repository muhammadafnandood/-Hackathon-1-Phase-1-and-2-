// Physical AI Chat Widget
(function() {
  const API_URL = 'http://localhost:8000'; // FastAPI backend URL

  // Create chat button
  const chatButton = document.createElement('button');
  chatButton.id = 'chat-widget-button';
  chatButton.innerHTML = '💬 Ask AI';
  document.body.appendChild(chatButton);

  // Create chat window
  const chatWindow = document.createElement('div');
  chatWindow.id = 'chat-widget-window';
  chatWindow.innerHTML = `
    <div class="chat-widget-header">
      <h3>Physical AI Assistant</h3>
      <button class="chat-widget-close">×</button>
    </div>
    <div class="chat-widget-messages" id="chat-messages">
      <div class="chat-message bot">
        <div class="message-content">
          Hello! I'm your Physical AI assistant. Ask me anything about ROS 2, humanoid robotics, or this textbook!
        </div>
      </div>
    </div>
    <div class="chat-widget-input">
      <input 
        type="text" 
        id="chat-input" 
        placeholder="Type your question..." 
        autocomplete="off"
      />
      <button id="chat-send">Send</button>
    </div>
  `;
  document.body.appendChild(chatWindow);

  // Text selection popup
  const selectionPopup = document.createElement('div');
  selectionPopup.id = 'selection-popup';
  selectionPopup.innerHTML = `
    <button id="ask-ai-selection">
      <span>💬</span> Ask AI
    </button>
  `;
  document.body.appendChild(selectionPopup);

  // State
  let isOpen = false;
  let isLoading = false;
  let selectedText = '';

  // Elements
  const messagesContainer = document.getElementById('chat-messages');
  const chatInput = document.getElementById('chat-input');
  const sendButton = document.getElementById('chat-send');
  const closeButton = chatWindow.querySelector('.chat-widget-close');
  const askAiButton = document.getElementById('ask-ai-selection');

  // Toggle chat window
  chatButton.addEventListener('click', () => {
    isOpen = !isOpen;
    chatWindow.classList.toggle('open', isOpen);
    chatButton.classList.toggle('active', isOpen);
    if (isOpen) {
      setTimeout(() => chatInput.focus(), 300);
    }
  });

  // Close button
  closeButton.addEventListener('click', () => {
    isOpen = false;
    chatWindow.classList.remove('open');
    chatButton.classList.remove('active');
  });

  // Text selection handler
  let hidePopupTimeout;

  function showSelectionPopup() {
    const selection = window.getSelection();
    selectedText = selection.toString().trim();

    if (!selectedText || selectedText.length < 5) {
      hideSelectionPopup();
      return;
    }

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();

    // Position popup above selected text
    selectionPopup.style.top = `${rect.top + window.scrollY - 50}px`;
    selectionPopup.style.left = `${rect.left + window.scrollX + (rect.width / 2) - 50}px`;
    selectionPopup.style.opacity = '1';
    selectionPopup.style.visibility = 'visible';
  }

  function hideSelectionPopup() {
    selectionPopup.style.opacity = '0';
    selectionPopup.style.visibility = 'hidden';
  }

  // Show popup on text selection
  document.addEventListener('mouseup', () => {
    clearTimeout(hidePopupTimeout);
    hidePopupTimeout = setTimeout(showSelectionPopup, 100);
  });

  // Hide popup on click elsewhere
  document.addEventListener('mousedown', (e) => {
    if (!selectionPopup.contains(e.target)) {
      clearTimeout(hidePopupTimeout);
      hidePopupTimeout = setTimeout(hideSelectionPopup, 200);
    }
  });

  // Ask AI button click handler
  askAiButton.addEventListener('click', () => {
    if (selectedText) {
      // Open chat window
      isOpen = true;
      chatWindow.classList.add('open');
      chatButton.classList.add('active');

      // Send selected text as question
      sendMessage(selectedText);
      hideSelectionPopup();
    }
  });

  // Send message
  async function sendMessage(question) {
    if (!question || isLoading) return;

    // Add user message
    addMessage(question, 'user');
    chatInput.value = '';
    isLoading = true;
    showTypingIndicator();

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      removeTypingIndicator();

      if (response.ok) {
        const data = await response.json();
        addMessage(data.answer || data.response || 'Got your question!', 'bot');
      } else {
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
      }
    } catch (error) {
      removeTypingIndicator();
      addMessage('Sorry, I couldn\'t connect to the server. Please try again.', 'bot');
      console.error('Chat error:', error);
    }

    isLoading = false;
  }

  // Add message to chat
  function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    messageDiv.innerHTML = `
      <div class="message-content">${escapeHtml(text)}</div>
    `;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Show typing indicator
  function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot typing';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
      <div class="message-content">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Remove typing indicator
  function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
      typingIndicator.remove();
    }
  }

  // Escape HTML
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Event listeners
  sendButton.addEventListener('click', sendMessage);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });
})();
