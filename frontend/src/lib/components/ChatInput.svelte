<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let isLoading = false;
  export let placeholder = "Ask anything about your knowledge base...";

  const dispatch = createEventDispatcher<{
    submit: { question: string };
  }>();

  let question = '';
  let textareaEl: HTMLTextAreaElement;

  function handleSubmit() {
    const trimmedQuestion = question.trim();
    if (trimmedQuestion && !isLoading) {
      dispatch('submit', { question: trimmedQuestion });
      question = '';
      autoResize();
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  }

  function autoResize() {
    if (textareaEl) {
      textareaEl.style.height = 'auto';
      textareaEl.style.height = Math.min(textareaEl.scrollHeight, 150) + 'px';
    }
  }

  function handleInput() {
    autoResize();
  }

  // Auto-resize on mount
  $: if (textareaEl && question) {
    autoResize();
  }
</script>

<div class="chat-input-container">
  <form on:submit|preventDefault={handleSubmit} class="chat-form">
    <div class="input-wrapper">
      <textarea
        bind:this={textareaEl}
        bind:value={question}
        on:keydown={handleKeydown}
        on:input={handleInput}
        disabled={isLoading}
        placeholder={placeholder}
        rows="1"
        class="chat-textarea"
        class:loading={isLoading}
      ></textarea>
      
      <button
        type="submit"
        disabled={!question.trim() || isLoading}
        class="send-button"
        class:loading={isLoading}
        title="Send message (Enter)"
      >
        {#if isLoading}
          <div class="spinner"></div>
        {:else}
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="m22 2-7 20-4-9-9-4 20-7z"/>
          </svg>
        {/if}
      </button>
    </div>
  </form>
  
  <div class="input-hint">
    Press <kbd>Enter</kbd> to send, <kbd>Shift + Enter</kbd> for new line
  </div>
</div>

<style>
  .chat-input-container {
    background: white;
    border-top: 1px solid #e2e8f0;
    padding: 1rem;
    position: sticky;
    bottom: 0;
    z-index: 10;
  }

  .chat-form {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
  }

  .input-wrapper {
    display: flex;
    align-items: flex-end;
    background: #f7fafc;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 0.5rem;
    transition: all 0.2s ease;
  }

  .input-wrapper:focus-within {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  .chat-textarea {
    flex: 1;
    border: none;
    background: transparent;
    resize: none;
    outline: none;
    font-family: inherit;
    font-size: 1rem;
    line-height: 1.5;
    padding: 0.5rem;
    min-height: 40px;
    max-height: 150px;
    overflow-y: auto;
  }

  .chat-textarea::placeholder {
    color: #a0aec0;
  }

  .chat-textarea:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .send-button {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    width: 40px;
    height: 40px;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
    margin-left: 0.5rem;
  }

  .send-button:hover:not(:disabled) {
    background: #5a67d8;
    transform: translateY(-1px);
  }

  .send-button:active:not(:disabled) {
    transform: translateY(0);
  }

  .send-button:disabled {
    background: #cbd5e0;
    cursor: not-allowed;
    transform: none;
  }

  .send-button.loading {
    background: #667eea;
    cursor: wait;
  }

  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  .input-hint {
    text-align: center;
    font-size: 0.75rem;
    color: #718096;
    margin-top: 0.5rem;
  }

  kbd {
    background: #edf2f7;
    border: 1px solid #cbd5e0;
    border-radius: 3px;
    padding: 1px 4px;
    font-size: 0.7rem;
    font-family: monospace;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  @media (max-width: 768px) {
    .chat-input-container {
      padding: 0.75rem;
    }

    .input-wrapper {
      padding: 0.375rem;
    }

    .chat-textarea {
      font-size: 0.9rem;
      padding: 0.375rem;
    }

    .send-button {
      width: 36px;
      height: 36px;
    }

    .input-hint {
      font-size: 0.7rem;
    }
  }
</style>
