<script lang="ts">
  import { onMount } from 'svelte';
  import ChatMessage from './lib/components/ChatMessage.svelte';
  import ChatInput from './lib/components/ChatInput.svelte';
  import { chatStore, chatActions } from './lib/stores/chatStore';
  import { backendAPI } from './lib/api/backend';

  // Import page components
  import Dashboard from './routes/dashboard/+page.svelte';
  import History from './routes/history/+page.svelte';

  let messagesContainer: HTMLDivElement | null = null;
  let isConnected = false;
  let currentPage = 'chat';

  // Auto-scroll to bottom when new messages arrive
  $: if ($chatStore.messages.length > 0 && currentPage === 'chat') {
    scrollToBottom();
  }

  function scrollToBottom() {
    if (messagesContainer) {
      try {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      } catch (error) {
        console.error('Error scrolling to bottom:', error);
      }
    }
  }

  // Check backend connection and handle routing
  onMount(() => {
    // Check backend connection
    const checkConnection = async () => {
      try {
        const health = await backendAPI.health();
        isConnected = true;
      } catch (error) {
        console.error('Backend not available:', error);
        isConnected = false;
      }
    };

    checkConnection();

    // Handle routing
    if (typeof window !== 'undefined') {
      const updatePage = () => {
        const hash = window.location.hash.slice(1);
        currentPage = hash || 'chat';
      };
      
      updatePage();
      window.addEventListener('hashchange', updatePage);
      
      return () => {
        window.removeEventListener('hashchange', updatePage);
      };
    }
  });

  // Handle sending messages
  async function handleSendMessage(message: string) {
    if (!message.trim() || $chatStore.isLoading) return;

    // Add user message
    chatActions.addUserMessage(message);
    
    // Add loading message
    const loadingId = chatActions.addLoadingMessage();

    try {
      // Send to backend
      const response = await backendAPI.chat(message);
      
      // Update loading message with response
      chatActions.updateLoadingMessage(loadingId, response);
    } catch (error) {
      console.error('Chat error:', error);
      chatActions.setError('Failed to get response from assistant');
    }
  }

  // Navigation functions
  function navigateTo(page: string) {
    if (typeof window !== 'undefined') {
      window.location.hash = page;
    }
  }

  // Start new chat
  function startNewChat() {
    // Add a smooth transition effect
    if (messagesContainer) {
      messagesContainer.style.opacity = '0.5';
      setTimeout(() => {
        chatActions.clearChat();
        if (messagesContainer) {
          messagesContainer.style.opacity = '1';
        }
      }, 150);
    } else {
      chatActions.clearChat();
    }
  }
</script>

<div class="app">
  <!-- Sidebar Navigation -->
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1 class="app-title">
        <span class="app-icon">🤖</span>
        <span class="title-text">RAG Assistant</span>
      </h1>
    </div>

    <nav class="nav-menu">
      <button 
        class="nav-item {currentPage === 'chat' ? 'active' : ''}"
        on:click={() => navigateTo('chat')}
      >
        <span class="nav-icon">💬</span>
        <span class="nav-text">Chat</span>
      </button>
      
      <button 
        class="nav-item {currentPage === 'dashboard' ? 'active' : ''}"
        on:click={() => navigateTo('dashboard')}
      >
        <span class="nav-icon">📊</span>
        <span class="nav-text">Dashboard</span>
      </button>
      
      <button 
        class="nav-item {currentPage === 'history' ? 'active' : ''}"
        on:click={() => navigateTo('history')}
      >
        <span class="nav-icon">📝</span>
        <span class="nav-text">History</span>
      </button>
    </nav>

    <div class="sidebar-footer">
      <div class="connection-status {isConnected ? 'connected' : 'disconnected'}">
        <span class="status-indicator"></span>
        <span class="status-text">{isConnected ? 'Connected' : 'Offline'}</span>
      </div>
    </div>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    {#if currentPage === 'chat'}
      <div class="chat-container">
        <div class="chat-header">
          <div class="header-content">
            <div class="header-text">
              <h2>Chat Assistant</h2>
              <p>Ask me anything about your knowledge base</p>
            </div>
            <button class="new-chat-btn" on:click={startNewChat} title="Start New Chat">
              <span class="new-chat-icon">✨</span>
              <span class="new-chat-text">New Chat</span>
            </button>
          </div>
        </div>

        <div class="messages-container" bind:this={messagesContainer}>
          {#if $chatStore.messages.length === 0}
            <div class="welcome-message">
              <div class="welcome-icon">🤖</div>
              <h3>Welcome to RAG Assistant!</h3>
              <p>I can help you find information from your knowledge base. Just ask me anything!</p>
              
              <div class="sample-questions">
                <h4>💡 Try asking:</h4>
                <div class="question-cards">
                  <button class="question-card" on:click={() => handleSendMessage("Apa itu FastAPI?")}>
                    <span class="question-icon">🔗</span>
                    <span class="question-text">Apa itu FastAPI?</span>
                  </button>
                  
                  <button class="question-card" on:click={() => handleSendMessage("Bagaimana cara implementasi RAG?")}>
                    <span class="question-icon">🤖</span>
                    <span class="question-text">Bagaimana cara implementasi RAG?</span>
                  </button>
                  
                  <button class="question-card" on:click={() => handleSendMessage("Jelaskan tentang Python untuk AI")}>
                    <span class="question-icon">🌐</span>
                    <span class="question-text">Jelaskan tentang Python untuk AI</span>
                  </button>
                  
                  <button class="question-card" on:click={() => handleSendMessage("Apa perbedaan frontend dan backend?")}>
                    <span class="question-icon">⚡</span>
                    <span class="question-text">Apa perbedaan frontend dan backend?</span>
                  </button>
                </div>
              </div>
            </div>
          {/if}

          {#each $chatStore.messages as message, index (index)}
            <ChatMessage {message} />
          {/each}

          {#if $chatStore.isLoading}
            <div class="loading-message">
              <div class="loading-avatar">🤖</div>
              <div class="loading-content">
                <div class="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          {/if}
        </div>

        <div class="chat-input-container">
          <ChatInput 
            on:submit={(e) => handleSendMessage(e.detail.question)} 
            isLoading={!isConnected || $chatStore.isLoading}
          />
        </div>
      </div>
    {:else if currentPage === 'dashboard'}
      <div class="page-container">
        <Dashboard />
      </div>
    {:else if currentPage === 'history'}
      <div class="page-container">
        <History />
      </div>
    {/if}
  </main>
</div>

<style>
  :global(*) {
    box-sizing: border-box;
  }

  :global(html) {
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
  }

  :global(body) {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #f5f5f5;
    height: 100vh;
    width: 100vw;
    overflow: hidden;
  }

  :global(#app) {
    height: 100vh;
    width: 100vw;
    margin: 0;
    padding: 0;
  }

  .app {
    display: flex;
    height: 100vh;
    width: 100vw;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    overflow: hidden;
  }

  /* Sidebar Styles */
  .sidebar {
    width: 280px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.2);
    display: flex;
    flex-direction: column;
    box-shadow: 2px 0 20px rgba(0, 0, 0, 0.1);
  }

  .sidebar-header {
    padding: 2rem 1.5rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  }

  .app-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 0;
    font-size: 1.5rem;
    font-weight: 700;
    color: #2d3748;
  }

  .app-icon {
    font-size: 2rem;
  }

  .title-text {
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .nav-menu {
    flex: 1;
    padding: 1rem 0;
  }

  .nav-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.5rem;
    border: none;
    background: none;
    color: #4a5568;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
  }

  .nav-item:hover {
    background: rgba(102, 126, 234, 0.1);
    color: #667eea;
  }

  .nav-item.active {
    background: rgba(102, 126, 234, 0.15);
    color: #667eea;
    border-left-color: #667eea;
    font-weight: 600;
  }

  .nav-icon {
    font-size: 1.25rem;
    width: 24px;
    text-align: center;
  }

  .sidebar-footer {
    padding: 1.5rem;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
  }

  .connection-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    animation: pulse 2s infinite;
  }

  .connection-status.connected .status-indicator {
    background: #10b981;
  }

  .connection-status.disconnected .status-indicator {
    background: #ef4444;
  }

  .connection-status.connected .status-text {
    color: #10b981;
  }

  .connection-status.disconnected .status-text {
    color: #ef4444;
  }

  /* Main Content Styles */
  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
  }

  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    background: white;
    overflow: hidden;
  }

  .page-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    background: white;
    overflow: hidden;
  }

  .chat-header {
    padding: 2rem;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
  }

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 2rem;
  }

  .header-text {
    flex: 1;
    text-align: left;
  }

  .chat-header h2 {
    margin: 0 0 0.5rem 0;
    font-size: 1.75rem;
    font-weight: 700;
  }

  .chat-header p {
    margin: 0;
    opacity: 0.9;
    font-size: 1rem;
  }

  .new-chat-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.25rem;
    background: rgba(255, 255, 255, 0.15);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    color: white;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s ease;
    backdrop-filter: blur(10px);
    flex-shrink: 0;
  }

  .new-chat-btn:hover {
    background: rgba(255, 255, 255, 0.25);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .new-chat-btn:active {
    transform: translateY(0);
  }

  .new-chat-icon {
    font-size: 1.1rem;
  }

  .new-chat-text {
    font-weight: 600;
  }

  .messages-container {
    flex: 1;
    padding: 1.5rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: opacity 0.15s ease;
  }

  .welcome-message {
    text-align: center;
    padding: 3rem 2rem;
    color: #6b7280;
  }

  .welcome-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
  }

  .welcome-message h3 {
    margin: 0 0 1rem 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #374151;
  }

  .welcome-message p {
    margin: 0 0 2rem 0;
    font-size: 1.1rem;
    line-height: 1.6;
  }

  .sample-questions {
    margin-top: 2rem;
  }

  .sample-questions h4 {
    margin: 0 0 1.5rem 0;
    font-size: 1.2rem;
    font-weight: 600;
    color: #4a5568;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .question-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
    max-width: 800px;
    margin: 0 auto;
  }

  .question-card {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    font-size: 0.95rem;
    font-weight: 500;
    color: #2d3748;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }

  .question-card:hover {
    border-color: #667eea;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
    background: linear-gradient(135deg, #f8faff, #ffffff);
  }

  .question-card:active {
    transform: translateY(0);
  }

  .question-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
  }

  .question-text {
    flex: 1;
    line-height: 1.4;
  }

  .loading-message {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    align-items: flex-start;
  }

  .loading-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
  }

  .loading-content {
    flex: 1;
    padding: 1rem;
    background: #f8fafc;
    border-radius: 18px;
    border-top-left-radius: 4px;
  }

  .loading-dots {
    display: flex;
    gap: 4px;
  }

  .loading-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #667eea;
    animation: bounce 1.4s infinite;
  }

  .loading-dots span:nth-child(2) {
    animation-delay: 0.2s;
  }

  .loading-dots span:nth-child(3) {
    animation-delay: 0.4s;
  }

  .chat-input-container {
    padding: 1.5rem;
    border-top: 1px solid #e5e7eb;
    background: #fafafa;
  }

  /* Scrollbar Styles */
  .messages-container::-webkit-scrollbar {
    width: 6px;
  }

  .messages-container::-webkit-scrollbar-track {
    background: transparent;
  }

  .messages-container::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 3px;
  }

  .messages-container::-webkit-scrollbar-thumb:hover {
    background: #9ca3af;
  }

  /* Animations */
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }

  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-8px);
    }
    60% {
      transform: translateY(-4px);
    }
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .app {
      flex-direction: column;
    }
    
    .sidebar {
      width: 100%;
      height: auto;
      flex-direction: row;
      overflow-x: auto;
    }
    
    .sidebar-header {
      flex-shrink: 0;
    }
    
    .nav-menu {
      display: flex;
      flex-direction: row;
      padding: 0;
    }
    
    .nav-item {
      flex-direction: column;
      gap: 0.25rem;
      padding: 0.75rem;
      min-width: 80px;
      border-left: none;
      border-bottom: 3px solid transparent;
    }
    
    .nav-item.active {
      border-left: none;
      border-bottom-color: #667eea;
    }
    
    .nav-text {
      font-size: 0.75rem;
    }
    
    .sidebar-footer {
      flex-shrink: 0;
      padding: 1rem;
    }
    
    .chat-container {
      margin: 0.5rem;
      border-radius: 15px;
    }
    
    .chat-header {
      padding: 1.5rem;
    }

    .header-content {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }

    .header-text {
      text-align: center;
    }

    .new-chat-btn {
      align-self: center;
    }

    .messages-container {
      padding: 1rem;
    }    .chat-input-container {
      padding: 1rem;
    }
  }
</style>
