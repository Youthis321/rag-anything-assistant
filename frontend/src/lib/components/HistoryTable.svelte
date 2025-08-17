<script lang="ts">
  import type { HistoryResponse } from '../api/backend';

  export let historyData: HistoryResponse | null = null;
  export let isLoading = false;
  export let selectedDate = '';

  function formatTime(timestamp: string): string {
    return new Date(timestamp).toLocaleTimeString('id-ID', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  }

  function truncateText(text: string, maxLength = 100): string {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  }

  function formatSources(sources: string[]): string {
    return sources.map(source => source.replace('.md', '')).join(', ');
  }
</script>

<div class="history-table-container">
  <div class="table-header">
    <h2 class="table-title">
      📜 Chat History
      {#if selectedDate}
        <span class="date-badge">{selectedDate}</span>
      {/if}
    </h2>
    
    {#if historyData && historyData.conversations.length > 0}
      <div class="conversation-count">
        {historyData.conversations.length} conversation{historyData.conversations.length !== 1 ? 's' : ''}
      </div>
    {/if}
  </div>

  {#if isLoading}
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">Loading chat history...</p>
    </div>
  {:else if !historyData || historyData.conversations.length === 0}
    <div class="empty-state">
      <div class="empty-icon">💬</div>
      <h3 class="empty-title">No conversations found</h3>
      <p class="empty-description">
        {selectedDate 
          ? `No chat history available for ${selectedDate}` 
          : 'Select a date to view chat history'}
      </p>
    </div>
  {:else}
    <div class="table-wrapper">
      <table class="history-table">
        <thead>
          <tr>
            <th class="col-time">Time</th>
            <th class="col-question">Question</th>
            <th class="col-answer">Answer</th>
            <th class="col-sources">Sources</th>
          </tr>
        </thead>
        <tbody>
          {#each historyData.conversations as conversation, index}
            <tr class="conversation-row" class:even={index % 2 === 0}>
              <td class="cell-time">
                <span class="time-badge">{formatTime(conversation.timestamp)}</span>
              </td>
              <td class="cell-question">
                <div class="question-content">
                  <span class="user-icon">👤</span>
                  <p class="question-text">{conversation.question}</p>
                </div>
              </td>
              <td class="cell-answer">
                <div class="answer-content">
                  <span class="bot-icon">🤖</span>
                  <p class="answer-text" title={conversation.answer}>
                    {truncateText(conversation.answer, 150)}
                  </p>
                </div>
              </td>
              <td class="cell-sources">
                {#if conversation.sources && conversation.sources.length > 0}
                  <div class="sources-list">
                    {#each conversation.sources as source}
                      <span class="source-badge">{source.replace('.md', '')}</span>
                    {/each}
                  </div>
                {:else}
                  <span class="no-sources">No sources</span>
                {/if}
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<style>
  .history-table-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    overflow: hidden;
  }

  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    background: #f8f9fa;
    border-bottom: 1px solid #e2e8f0;
  }

  .table-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #2d3748;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .date-badge {
    background: #667eea;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .conversation-count {
    color: #718096;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    gap: 1rem;
  }

  .loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #e2e8f0;
    border-top: 3px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  .loading-text {
    color: #718096;
    font-size: 0.9rem;
    margin: 0;
  }

  .empty-state {
    text-align: center;
    padding: 3rem;
  }

  .empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .empty-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #4a5568;
    margin: 0 0 0.5rem 0;
  }

  .empty-description {
    color: #718096;
    font-size: 0.9rem;
    margin: 0;
  }

  .table-wrapper {
    overflow-x: auto;
  }

  .history-table {
    width: 100%;
    border-collapse: collapse;
  }

  .history-table th {
    background: #f8f9fa;
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    color: #4a5568;
    border-bottom: 2px solid #e2e8f0;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .col-time { width: 10%; min-width: 80px; }
  .col-question { width: 30%; min-width: 200px; }
  .col-answer { width: 45%; min-width: 300px; }
  .col-sources { width: 15%; min-width: 120px; }

  .conversation-row {
    border-bottom: 1px solid #e2e8f0;
    transition: background-color 0.2s ease;
  }

  .conversation-row:hover {
    background: #f8f9fa;
  }

  .conversation-row.even {
    background: #fdfdfd;
  }

  .history-table td {
    padding: 1rem;
    vertical-align: top;
  }

  .time-badge {
    background: #edf2f7;
    color: #4a5568;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 500;
    font-family: monospace;
  }

  .question-content,
  .answer-content {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .user-icon,
  .bot-icon {
    flex-shrink: 0;
    font-size: 1rem;
  }

  .question-text,
  .answer-text {
    margin: 0;
    line-height: 1.4;
    font-size: 0.875rem;
    color: #2d3748;
  }

  .answer-text {
    cursor: help;
  }

  .sources-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
  }

  .source-badge {
    background: #667eea;
    color: white;
    padding: 0.125rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
  }

  .no-sources {
    color: #a0aec0;
    font-style: italic;
    font-size: 0.8rem;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  @media (max-width: 768px) {
    .table-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
      padding: 1rem;
    }

    .table-title {
      font-size: 1.1rem;
    }

    .history-table th,
    .history-table td {
      padding: 0.75rem 0.5rem;
    }

    .col-time { width: 15%; }
    .col-question { width: 35%; }
    .col-answer { width: 35%; }
    .col-sources { width: 15%; }

    .question-text,
    .answer-text {
      font-size: 0.8rem;
    }
  }
</style>
