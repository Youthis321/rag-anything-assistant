<script lang="ts">
  import { onMount } from 'svelte';
  import HistoryTable from '../../lib/components/HistoryTable.svelte';
  import { backendAPI } from '../../lib/api/backend';
  import type { HistoryResponse } from '../../lib/api/backend';

  let selectedDate = '';
  let historyData: HistoryResponse | null = null;
  let isLoading = false;
  let error: string | null = null;

  // Set default date to today and load history automatically
  onMount(async () => {
    const today = new Date();
    selectedDate = today.toISOString().split('T')[0];
    
    // Auto-load history for today
    await loadHistory();
  });

  async function loadHistory() {
    if (!selectedDate) return;

    try {
      isLoading = true;
      error = null;
      historyData = await backendAPI.getHistory(selectedDate);
    } catch (err) {
      console.error('Failed to load history:', err);
      error = 'Failed to load chat history. Please try again.';
      historyData = null;
    } finally {
      isLoading = false;
    }
  }

  function handleDateChange() {
    if (selectedDate) {
      loadHistory();
    }
  }

  function formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString('id-ID', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
</script>

<svelte:head>
  <title>RAG Assistant - History</title>
</svelte:head>

<div class="history-page">
  <div class="history-header">
    <h1 class="page-title">📜 Chat History</h1>
    <p class="page-description">View your conversation history by date</p>
  </div>

  <!-- Date Picker Section -->
  <div class="date-picker-section">
    <div class="date-picker-container">
      <label for="date-input" class="date-label">
        📅 Select Date:
      </label>
      <input
        id="date-input"
        type="date"
        bind:value={selectedDate}
        on:change={handleDateChange}
        class="date-input"
        max={new Date().toISOString().split('T')[0]}
      />
      {#if isLoading}
        <div class="loading-indicator">
          ⏳ Loading...
        </div>
      {/if}
    </div>
    
    {#if selectedDate}
      <div class="selected-date-info">
        Showing history for: <strong>{formatDate(selectedDate)}</strong>
      </div>
    {/if}
  </div>

  <!-- Error Banner -->
  {#if error}
    <div class="error-banner">
      <span class="error-icon">❌</span>
      <span class="error-text">{error}</span>
      <button class="retry-button" on:click={loadHistory}>Retry</button>
    </div>
  {/if}

  <!-- History Table -->
  <div class="history-content">
    <HistoryTable 
      {historyData} 
      {isLoading} 
      selectedDate={selectedDate}
    />
  </div>

  <!-- Action Buttons -->
  <div class="history-actions">
    <a href="/" class="action-button primary">
      💬 Back to Chat
    </a>
    <a href="/dashboard" class="action-button secondary">
      📊 View Dashboard
    </a>
  </div>
</div>

<style>
  .history-page {
    padding: 2rem;
    height: 100%;
    width: 100%;
    background: #f8f9fa;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }

  .history-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .page-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #2d3748;
    margin: 0 0 0.5rem 0;
  }

  .page-description {
    font-size: 1.1rem;
    color: #718096;
    margin: 0;
  }

  .date-picker-section {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .date-picker-container {
    display: flex;
    align-items: center;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .date-label {
    font-weight: 600;
    color: #4a5568;
    font-size: 1rem;
  }

  .date-input {
    padding: 0.75rem;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
    color: #2d3748;
    background: white;
    transition: border-color 0.2s ease;
    min-width: 160px;
  }

  .date-input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  .loading-indicator {
    color: #667eea;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .selected-date-info {
    text-align: center;
    margin-top: 1rem;
    color: #4a5568;
    font-size: 0.9rem;
  }

  .error-banner {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #fed7d7;
    color: #c53030;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    font-weight: 500;
  }

  .error-icon {
    flex-shrink: 0;
  }

  .error-text {
    flex: 1;
  }

  .retry-button {
    background: #c53030;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .retry-button:hover {
    background: #9c2626;
  }

  .history-content {
    flex: 1;
    margin-bottom: 2rem;
    overflow-y: auto;
  }

  .history-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .action-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s ease;
    font-size: 0.9rem;
  }

  .action-button.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .action-button.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }

  .action-button.secondary {
    background: white;
    color: #4a5568;
    border: 2px solid #e2e8f0;
  }

  .action-button.secondary:hover {
    border-color: #667eea;
    color: #667eea;
    transform: translateY(-1px);
  }

  @media (max-width: 768px) {
    .history-page {
      padding: 1rem;
    }

    .page-title {
      font-size: 2rem;
    }

    .date-picker-container {
      flex-direction: column;
      align-items: stretch;
    }

    .date-input {
      width: 100%;
    }

    .history-actions {
      flex-direction: column;
      align-items: center;
    }

    .action-button {
      width: 100%;
      max-width: 300px;
      justify-content: center;
    }
  }
</style>
