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
    API_URL: 'http://localhost:8000',
    BOT_NAME: 'Textbook Assistant',
    BOT_AVATAR: '🤖',
    USER_AVATAR: '👤',
    THEME_COLOR: '#2563eb',
    POSITION: 'bottom-right', // 'bottom-right' or 'bottom-left'
  };

  // Chat state
  let isOpen = false;
  let isLoading = false;
  let chatHistory = [];
  let userLevel = 'Beginner'; // Default level

  // Diagram templates for different topics
  const DIAGRAM_TEMPLATES = {
    ros2_pubsub: {
      title: '🏗️ ROS 2 Publisher-Subscriber Architecture',
      mermaid: `graph LR
    subgraph ROS2_Network["ROS 2 Network"]
        direction LR
        subgraph Node1["Node 1"]
            P1[Publisher]
        end
        subgraph Node2["Node 2"]
            S1[Subscriber]
        end
        subgraph Node3["Node 3"]
            S2[Subscriber]
        end
        T[("Topic: /sensor_data")]
    end
    P1 -->|Publishes| T
    T -->|Subscribes| S1
    T -->|Subscribes| S2
    style Node1 fill:#4CAF50,color:#fff
    style Node2 fill:#2196F3,color:#fff
    style Node3 fill:#2196F3,color:#fff
    style T fill:#FF9800,color:#fff`
    },
    ros2_node: {
      title: '🏗️ ROS 2 Node Architecture',
      mermaid: `graph TB
    subgraph Node["ROS 2 Node"]
        Publishers[Publishers]
        Subscribers[Subscribers]
        Services[Services]
        Clients[Clients]
        Executor[Executor]
    end
    Publishers --> Executor
    Subscribers --> Executor
    Services --> Executor
    Clients --> Executor
    Executor --> ROS2Core[("ROS 2 Core<br/>DDS")]
    style Node fill:#E3F2FD
    style ROS2Core fill:#FF9800,color:#fff`
    },
    rag_pipeline: {
      title: '🏗️ RAG Pipeline Architecture',
      mermaid: `graph TD
    User[("User Query")] --> Embed[Embedding Model]
    subgraph Retrieval["Retrieval Phase"]
        Embed --> Search[("Vector Search<br/>Qdrant")]
        Search --> Rank[Rank Results]
        Rank --> Retrieve[Retrieve Chunks]
    end
    subgraph Generation["Generation Phase"]
        Retrieve --> Context[Build Context]
        Context --> Prompt[Construct Prompt]
        Prompt --> LLM[("LLM<br/>GPT")]
        LLM --> Answer[Generate Answer]
    end
    Answer --> Output[("Response + Sources")]
    style User fill:#E3F2FD
    style Embed fill:#FFF3E0
    style LLM fill:#FFEBEE
    style Output fill:#E0F2F1`
    },
    robot_perception: {
      title: '🏗️ Robot Perception Pipeline',
      mermaid: `graph TD
    subgraph Sensors["Sensors"]
        Camera[("Camera<br/>RGB-D")]
        LiDAR[("LiDAR<br/>3D Points")]
        IMU[("IMU<br/>Orientation")]
    end
    subgraph Processing["Processing"]
        Calib[Sensor Calibration]
        Filter[Noise Filtering]
        Fuse[Data Fusion]
    end
    subgraph Output["Output"]
        Detect[Object Detection]
        Track[Tracking]
        World[("World Model")]
    end
    Camera --> Calib
    LiDAR --> Calib
    IMU --> Fuse
    Calib --> Filter
    Filter --> Fuse
    Fuse --> Detect
    Detect --> Track
    Track --> World
    style Sensors fill:#E3F2FD
    style Processing fill:#FFF3E0
    style Output fill:#E8F5E9`
    },
    vla_model: {
      title: '🏗️ Vision-Language-Action (VLA) Model',
      mermaid: `graph LR
    subgraph Inputs["Input Encoders"]
        Vision[("Vision<br/>ViT")]
        Language[("Language<br/>LLM")]
        Proprio[("Proprioception")]
    end
    subgraph Fusion["Fusion"]
        CrossAttn[Cross-Attention]
        Transformer[Fusion Transformer]
    end
    subgraph Output["Action Output"]
        ActionHead[("Action Head")]
        Traj[Trajectory]
    end
    Vision --> CrossAttn
    Language --> CrossAttn
    Proprio --> Transformer
    CrossAttn --> Transformer
    Transformer --> ActionHead
    ActionHead --> Traj
    style Inputs fill:#E3F2FD
    style Fusion fill:#FFF3E0
    style Output fill:#E8F5E9`
    },
    control_loop: {
      title: '🏗️ Robot Control Loop',
      mermaid: `graph LR
    subgraph Loop["Control Loop (100Hz)"]
        Sense[("Sense")]
        Plan[("Plan")]
        Act[("Act")]
    end
    Environment[("Environment")]
    Sense --> Plan
    Plan --> Act
    Act --> Environment
    Environment --> Sense
    style Sense fill:#4CAF50,color:#fff
    style Plan fill:#2196F3,color:#fff
    style Act fill:#FF9800,color:#fff`
    }
  };

  // Keywords to detect diagram topics
  const DIAGRAM_KEYWORDS = {
    ros2_pubsub: ['ros 2 publisher', 'ros 2 subscriber', 'publish subscribe', 'ros 2 communication', 'ros 2 topics'],
    ros2_node: ['ros 2 node', 'ros 2 architecture', 'ros 2 structure'],
    rag_pipeline: ['rag pipeline', 'rag architecture', 'retrieval augmentation', 'rag system', 'vector search'],
    robot_perception: ['perception pipeline', 'sensor fusion', 'robot perception', 'camera lidar'],
    vla_model: ['vla model', 'vision language action', 'vla architecture', 'robot learning'],
    control_loop: ['control loop', 'sense plan act', 'robot control', 'feedback loop']
  };

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
            <div class="rag-chatbot-level-selector">
              <label for="rag-chatbot-level">Level:</label>
              <select id="rag-chatbot-level">
                <option value="Beginner" ${userLevel === 'Beginner' ? 'selected' : ''}>🌱 Beginner</option>
                <option value="Student" ${userLevel === 'Student' ? 'selected' : ''}>📚 Student</option>
                <option value="Engineer" ${userLevel === 'Engineer' ? 'selected' : ''}>⚙️ Engineer</option>
                <option value="Researcher" ${userLevel === 'Researcher' ? 'selected' : ''}>🔬 Researcher</option>
              </select>
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

        .rag-chatbot-level-selector {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 13px;
        }

        .rag-chatbot-level-selector label {
          font-weight: 500;
          opacity: 0.9;
        }

        .rag-chatbot-level-selector select {
          background: rgba(255, 255, 255, 0.2);
          border: 1px solid rgba(255, 255, 255, 0.3);
          border-radius: 6px;
          padding: 4px 8px;
          color: white;
          font-size: 12px;
          cursor: pointer;
          outline: none;
          transition: all 0.2s;
        }

        .rag-chatbot-level-selector select:hover {
          background: rgba(255, 255, 255, 0.3);
        }

        .rag-chatbot-level-selector select option {
          background: ${CONFIG.THEME_COLOR};
          color: white;
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
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .rag-chatbot-source:hover {
          border-color: ${CONFIG.THEME_COLOR};
        }

        .rag-chatbot-source-link {
          color: ${CONFIG.THEME_COLOR};
          text-decoration: none;
          font-weight: 600;
        }

        .rag-chatbot-source-link:hover {
          text-decoration: underline;
        }

        .rag-chatbot-source-confidence {
          background: #dbeafe;
          color: #1e40af;
          padding: 2px 8px;
          border-radius: 12px;
          font-size: 11px;
          font-weight: 600;
        }

        /* Urdu Translation */
        .rag-chatbot-translate-btn {
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 8px;
          font-size: 13px;
          font-weight: 600;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 6px;
          margin-top: 12px;
          transition: all 0.2s;
        }

        .rag-chatbot-translate-btn:hover {
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }

        .rag-chatbot-urdu-text {
          background: #f0fdf4;
          border: 1px solid #bbf7d0;
          border-radius: 8px;
          padding: 12px 16px;
          margin-top: 12px;
          font-size: 14px;
          line-height: 1.8;
          direction: rtl;
          display: none;
        }

        .rag-chatbot-urdu-text.show {
          display: block;
        }

        .rag-chatbot-toggle-lang {
          background: #f1f5f9;
          border: 1px solid #e2e8f0;
          padding: 6px 12px;
          border-radius: 6px;
          font-size: 12px;
          cursor: pointer;
          margin-top: 8px;
          display: none;
        }

        .rag-chatbot-toggle-lang.show {
          display: inline-block;
        }

        .rag-chatbot-toggle-lang:hover {
          background: #e2e8f0;
        }

        /* Diagram Container */
        .rag-chatbot-diagram-container {
          background: #fafafa;
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          padding: 16px;
          margin-top: 12px;
          overflow-x: auto;
        }

        .rag-chatbot-diagram-title {
          font-weight: 600;
          font-size: 14px;
          color: #1e293b;
          margin-bottom: 12px;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .rag-chatbot-diagram {
          display: flex;
          justify-content: center;
          padding: 16px 0;
        }

        .rag-chatbot-diagram-controls {
          display: flex;
          gap: 8px;
          margin-top: 12px;
          justify-content: flex-end;
        }

        .rag-chatbot-diagram-btn {
          background: #f1f5f9;
          border: 1px solid #e2e8f0;
          padding: 6px 12px;
          border-radius: 6px;
          font-size: 12px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 4px;
          transition: all 0.2s;
        }

        .rag-chatbot-diagram-btn:hover {
          background: #e2e8f0;
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
      </style>
    `;

    document.head.insertAdjacentHTML('beforeend', styles);
  }

  // Attach event listeners
  function attachEventListeners() {
    const toggleBtn = document.getElementById('rag-chatbot-toggle');
    const closeBtn = document.getElementById('rag-chatbot-close');
    const sendBtn = document.getElementById('rag-chatbot-send');
    const input = document.getElementById('rag-chatbot-input');
    const chatIcon = document.getElementById('rag-chatbot-icon-chat');
    const closeIcon = document.getElementById('rag-chatbot-icon-close');
    const levelSelect = document.getElementById('rag-chatbot-level');

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

    // Level selector change
    if (levelSelect) {
      levelSelect.addEventListener('change', (e) => {
        userLevel = e.target.value;
      });
    }
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
  function addMessage(content, isUser = false, query = '') {
    const messagesContainer = document.getElementById('rag-chatbot-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `rag-chatbot-message ${isUser ? 'rag-chatbot-user-message' : 'rag-chatbot-bot-message'}`;

    const messageId = 'msg-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);

    // Detect if we should show a diagram
    const diagramInfo = detectDiagram(query);

    messageDiv.innerHTML = `
      <div class="rag-chatbot-message-avatar">${isUser ? CONFIG.USER_AVATAR : CONFIG.BOT_AVATAR}</div>
      <div>
        <div class="rag-chatbot-message-content" id="${messageId}-text">${escapeHtml(content)}</div>
        ${!isUser ? `
          <button class="rag-chatbot-translate-btn" onclick="translateToUrdu('${messageId}', '${escapeHtml(content).replace(/'/g, "\\'")}')" style="margin-top: 8px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 8l6 6M11 8l-6 6M8 4v16M19 8l-6 6M13 8l6 6M16 4v16"/>
            </svg>
            Translate to Urdu
          </button>
          <div class="rag-chatbot-urdu-text" id="${messageId}-urdu"></div>
          <button class="rag-chatbot-toggle-lang" id="${messageId}-toggle" onclick="toggleLanguage('${messageId}')">
            Show Urdu
          </button>
          ${diagramInfo ? `
            <div class="rag-chatbot-diagram-container" id="${messageId}-diagram-container">
              <div class="rag-chatbot-diagram-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                  <polyline points="2 17 12 22 22 17"></polyline>
                  <polyline points="2 12 12 17 22 12"></polyline>
                </svg>
                ${diagramInfo.title}
              </div>
              <div class="rag-chatbot-diagram" id="${messageId}-diagram"></div>
              <div class="rag-chatbot-diagram-controls">
                <button class="rag-chatbot-diagram-btn" onclick="zoomDiagram('${messageId}', 0.1)">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    <line x1="11" y1="8" x2="11" y2="14"></line>
                    <line x1="8" y1="11" x2="14" y2="11"></line>
                  </svg>
                  Zoom In
                </button>
                <button class="rag-chatbot-diagram-btn" onclick="zoomDiagram('${messageId}', -0.1)">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    <line x1="8" y1="11" x2="14" y2="11"></line>
                  </svg>
                  Zoom Out
                </button>
              </div>
            </div>
          ` : ''}
        ` : ''}
      </div>
    `;

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Render diagram if detected
    if (!isUser && diagramInfo) {
      renderDiagram(messageId, diagramInfo.mermaid);
    }
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
  function showSources(sources, confidence) {
    const sourcesPanel = document.getElementById('rag-chatbot-sources');
    const sourcesList = document.getElementById('rag-chatbot-sources-list');

    if (!sources || sources.length === 0) {
      sourcesPanel.style.display = 'none';
      return;
    }

    // Extract unique chapters and format chapter number for URL
    const uniqueSources = [];
    const seen = new Set();

    sources.forEach(source => {
      const chapter = source.chapter || 'Unknown';
      if (!seen.has(chapter)) {
        seen.add(chapter);
        uniqueSources.push(source);
      }
    });

    // Format chapter number for URL
    const firstChapter = uniqueSources[0].chapter || 'Unknown';
    const chapterNum = firstChapter.replace(/Chapter\s*/gi, '');
    const chapterUrl = `/docs/chapter${chapterNum}`;
    const confidenceScore = confidence ? Math.round(confidence) : null;

    sourcesList.innerHTML = `
      <div class="rag-chatbot-source">
        <a href="${chapterUrl}" target="_blank" class="rag-chatbot-source-link">
          Source: ${firstChapter}
        </a>
        ${confidenceScore !== null ? `<span class="rag-chatbot-source-confidence">Confidence: ${confidenceScore}%</span>` : ''}
      </div>
    `;

    sourcesPanel.style.display = 'block';
  }

  // Send message
  async function sendMessage() {
    const input = document.getElementById('rag-chatbot-input');
    const query = input.value.trim();

    if (!query || isLoading) return;

    // Add user message
    addMessage(query, true, query);
    input.value = '';
    input.style.height = 'auto';

    // Show loading
    showLoading();
    isLoading = true;
    document.getElementById('rag-chatbot-send').disabled = true;

    try {
      // Call API with user level
      const response = await fetch(`${CONFIG.API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: query,
          level: userLevel,
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

      // Add bot response (handle both 'answer' and 'response' fields)
      const answerText = data.answer || data.response || "Sorry, I couldn't generate a response.";
      addMessage(answerText, false, query);

      // Show sources with confidence (handle different response formats)
      const sources = data.sources || [];
      const confidence = data.confidence || (data.sources && data.sources.length > 0 ? 0.85 : 0);
      showSources(sources, confidence);

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

  // Detect diagram based on query
  function detectDiagram(query) {
    if (!query) return null;

    const queryLower = query.toLowerCase();

    for (const [diagramType, keywords] of Object.entries(DIAGRAM_KEYWORDS)) {
      for (const keyword of keywords) {
        if (queryLower.includes(keyword)) {
          return {
            type: diagramType,
            title: DIAGRAM_TEMPLATES[diagramType]?.title || 'Architecture Diagram',
            mermaid: DIAGRAM_TEMPLATES[diagramType]?.mermaid || null
          };
        }
      }
    }

    // Check for generic architecture/diagram requests
    if (queryLower.includes('architecture') || queryLower.includes('diagram') || 
        queryLower.includes('flow') || queryLower.includes('structure')) {
      // Try to find the most relevant diagram
      if (queryLower.includes('ros')) return { type: 'ros2_pubsub', title: DIAGRAM_TEMPLATES.ros2_pubsub.title, mermaid: DIAGRAM_TEMPLATES.ros2_pubsub.mermaid };
      if (queryLower.includes('rag')) return { type: 'rag_pipeline', title: DIAGRAM_TEMPLATES.rag_pipeline.title, mermaid: DIAGRAM_TEMPLATES.rag_pipeline.mermaid };
      if (queryLower.includes('vla') || queryLower.includes('vision language')) return { type: 'vla_model', title: DIAGRAM_TEMPLATES.vla_model.title, mermaid: DIAGRAM_TEMPLATES.vla_model.mermaid };
      if (queryLower.includes('perception') || queryLower.includes('sensor')) return { type: 'robot_perception', title: DIAGRAM_TEMPLATES.robot_perception.title, mermaid: DIAGRAM_TEMPLATES.robot_perception.mermaid };
    }

    return null;
  }

  // Render Mermaid diagram
  function renderDiagram(messageId, mermaidCode) {
    const diagramEl = document.getElementById(`${messageId}-diagram`);
    if (!diagramEl) return;

    // Load Mermaid library if not already loaded
    if (typeof mermaid === 'undefined') {
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
      script.onload = () => {
        mermaid.initialize({ startOnLoad: false, theme: 'default' });
        renderMermaid(diagramEl, mermaidCode);
      };
      document.head.appendChild(script);
    } else {
      renderMermaid(diagramEl, mermaidCode);
    }
  }

  // Render Mermaid code
  function renderMermaid(element, mermaidCode) {
    try {
      // Create unique ID for this diagram
      const diagramId = 'mermaid-' + Date.now();
      element.innerHTML = `<div id="${diagramId}"></div>`;
      
      // Render the diagram
      mermaid.render(diagramId, mermaidCode).then(({ svg }) => {
        element.innerHTML = svg;
      }).catch(error => {
        console.error('Mermaid rendering error:', error);
        element.innerHTML = '<p style="color: #dc2626;">❌ Diagram rendering failed</p>';
      });
    } catch (error) {
      console.error('Diagram error:', error);
      element.innerHTML = '<p style="color: #dc2626;">❌ Diagram rendering failed</p>';
    }
  }

  // Zoom diagram
  window.zoomDiagram = function(messageId, delta) {
    const diagramEl = document.getElementById(`${messageId}-diagram`);
    if (!diagramEl) return;

    const svg = diagramEl.querySelector('svg');
    if (!svg) return;

    const currentScale = svg.getAttribute('data-scale') || 1;
    const newScale = Math.max(0.5, Math.min(2, parseFloat(currentScale) + delta));
    
    svg.setAttribute('data-scale', newScale);
    svg.style.transform = `scale(${newScale})`;
    svg.style.transformOrigin = 'center center';
  };

  // Escape HTML
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Translate to Urdu (global function)
  window.translateToUrdu = async function(messageId, text) {
    const urduTextEl = document.getElementById(`${messageId}-urdu`);
    const toggleBtn = document.getElementById(`${messageId}-toggle`);

    if (!urduTextEl || !toggleBtn) {
      console.error('Urdu elements not found for messageId:', messageId);
      return;
    }

    // Show loading
    urduTextEl.textContent = 'ترجمہ ہو رہا ہے...';
    urduTextEl.classList.add('show');
    toggleBtn.classList.add('show');

    try {
      const response = await fetch(`${CONFIG.API_URL}/api/translate/urdu`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: text,
          language: 'urdu'
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error('Translation failed: ' + errorText);
      }

      const data = await response.json();

      // Display Urdu translation
      if (data.translated) {
        urduTextEl.textContent = data.translated;
      } else {
        urduTextEl.textContent = '❌ Translation not available';
      }
      toggleBtn.textContent = 'Show Urdu';

    } catch (error) {
      console.error('Translation error:', error);
      urduTextEl.textContent = '❌ Translation failed. Please check backend.';
    }
  };

  // Toggle between English and Urdu (global function)
  window.toggleLanguage = function(messageId) {
    const urduTextEl = document.getElementById(`${messageId}-urdu`);
    const toggleBtn = document.getElementById(`${messageId}-toggle`);

    if (!urduTextEl || !toggleBtn) return;

    if (urduTextEl.style.display === 'none' || urduTextEl.style.display === '') {
      urduTextEl.style.display = 'block';
      toggleBtn.textContent = 'Show English';
    } else {
      urduTextEl.style.display = 'none';
      toggleBtn.textContent = 'Show Urdu';
    }
  };

  // Initialize widget when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createWidget);
  } else {
    createWidget();
  }
})();
