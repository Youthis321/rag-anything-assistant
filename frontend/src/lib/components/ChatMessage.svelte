<script lang="ts">
  import type { ChatMessage } from '../stores/chatStore';

  export let message: ChatMessage;

  $: isUser = message.type === 'user';
  $: isAssistant = message.type === 'assistant';

  function formatTime(timestamp: Date): string {
    return timestamp.toLocaleTimeString('id-ID', {
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  function formatSources(sources: string[]): string {
    return sources.map(source => source.replace('.md', '')).join(', ');
  }
</script>

<div class="message-container" class:user={isUser} class:assistant={isAssistant}>
  <div class="message-bubble">
    <div class="message-header">
      <span class="message-author">
        {isUser ? '👤 You' : '🤖 RAG Assistant'}
      </span>
      <span class="message-time">
        {formatTime(message.timestamp)}
      </span>
    </div>
    
    <div class="message-content">
      {#if message.isLoading}
        <div class="loading-indicator">
          <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span class="loading-text">Thinking...</span>
        </div>
      {:else}
        <p class="message-text">{message.content}</p>
        
        {#if message.sources && message.sources.length > 0}
          <div class="sources">
            <strong>📚 Sources:</strong>
            <span class="sources-list">{formatSources(message.sources)}</span>
          </div>
        {/if}
      {/if}
    </div>
  </div>
</div>

<style>
  .message-container {
    margin-bottom: 1rem;
    display: flex;
    width: 100%;
  }

  .message-container.user {
    justify-content: flex-end;
  }

  .message-container.assistant {
    justify-content: flex-start;
  }

  .message-bubble {
    max-width: 70%;
    padding: 0.75rem 1rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    position: relative;
  }

  .user .message-bubble {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 4px;
  }

  .assistant .message-bubble {
    background: #f8f9fa;
    color: #2d3748;
    border: 1px solid #e2e8f0;
    border-bottom-left-radius: 4px;
  }

  .message-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
  }

  .message-author {
    font-weight: 600;
  }

  .message-time {
    opacity: 0.7;
    font-size: 0.75rem;
  }

  .message-content {
    line-height: 1.5;
  }

  .message-text {
    margin: 0;
    white-space: pre-wrap;
    word-wrap: break-word;
  }

  .sources {
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    font-size: 0.875rem;
  }

  .user .sources {
    border-top-color: rgba(255, 255, 255, 0.2);
  }

  .sources-list {
    color: #4a5568;
    font-style: italic;
  }

  .user .sources-list {
    color: rgba(255, 255, 255, 0.9);
  }

  .loading-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .typing-dots {
    display: flex;
    gap: 2px;
  }

  .typing-dots span {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background-color: #667eea;
    animation: typing 1.4s infinite ease-in-out;
  }

  .typing-dots span:nth-child(1) {
    animation-delay: -0.32s;
  }

  .typing-dots span:nth-child(2) {
    animation-delay: -0.16s;
  }

  .loading-text {
    color: #667eea;
    font-style: italic;
    font-size: 0.875rem;
  }

  @keyframes typing {
    0%, 80%, 100% {
      transform: scale(0.8);
      opacity: 0.5;
    }
    40% {
      transform: scale(1);
      opacity: 1;
    }
  }

  @media (max-width: 768px) {
    .message-bubble {
      max-width: 85%;
      padding: 0.5rem 0.75rem;
    }

    .message-header {
      font-size: 0.8rem;
    }

    .message-content {
      font-size: 0.9rem;
    }
  }
</style>
