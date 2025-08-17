<script lang="ts">
  import { onMount } from 'svelte';
  import DashboardCard from '../../lib/components/DashboardCard.svelte';
  import { dashboardStore, dashboardActions } from '../../lib/stores/dashboardStore';
  import { backendAPI } from '../../lib/api/backend';

  onMount(async () => {
    await loadStats();
  });

  async function loadStats() {
    try {
      dashboardActions.setLoading(true);
      const stats = await backendAPI.getStats();
      dashboardActions.setStats(stats);
    } catch (error) {
      console.error('Failed to load stats:', error);
      dashboardActions.setError('Failed to load dashboard statistics');
    }
  }

  function formatLastUpdated(dateString: string): string {
    return new Date(dateString).toLocaleString('id-ID');
  }
</script>

<svelte:head>
  <title>RAG Assistant - Dashboard</title>
</svelte:head>

<div class="dashboard-page">
  <div class="dashboard-header">
    <h1 class="page-title">📊 Dashboard</h1>
    <p class="page-description">Overview of your knowledge base and activity</p>
    
    {#if $dashboardStore.stats}
      <div class="last-updated">
        Last updated: {formatLastUpdated($dashboardStore.stats.last_updated)}
      </div>
    {/if}
  </div>

  {#if $dashboardStore.error}
    <div class="error-banner">
      <span class="error-icon">❌</span>
      <span class="error-text">{$dashboardStore.error}</span>
      <button class="retry-button" on:click={loadStats}>Retry</button>
    </div>
  {/if}

  <div class="dashboard-grid">
    <DashboardCard
      title="Articles"
      value={$dashboardStore.stats?.total_articles ?? 0}
      icon="📄"
      description="Total articles in knowledge base"
      color="blue"
      isLoading={$dashboardStore.isLoading}
    />
    
    <DashboardCard
      title="Projects"
      value={$dashboardStore.stats?.total_projects ?? 0}
      icon="📁"
      description="GitHub repositories cloned"
      color="green"
      isLoading={$dashboardStore.isLoading}
    />
    
    <DashboardCard
      title="Conversations"
      value={$dashboardStore.stats?.total_conversations ?? 0}
      icon="💬"
      description="Total chat conversations"
      color="purple"
      isLoading={$dashboardStore.isLoading}
    />
  </div>

  <div class="dashboard-actions">
    <button class="action-button primary" on:click={loadStats}>
      🔄 Refresh Data
    </button>
    <a href="/" class="action-button secondary">
      💬 Go to Chat
    </a>
    <a href="/history" class="action-button secondary">
      📜 View History
    </a>
  </div>
</div>

<style>
  .dashboard-page {
    padding: 2rem;
    height: 100%;
    width: 100%;
    background: #f8f9fa;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }

  .dashboard-header {
    text-align: center;
    margin-bottom: 3rem;
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
    margin: 0 0 1rem 0;
  }

  .last-updated {
    font-size: 0.875rem;
    color: #a0aec0;
    font-style: italic;
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

  .dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
    flex: 1;
    align-content: start;
  }

  .dashboard-actions {
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
    border: none;
    cursor: pointer;
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
    .dashboard-page {
      padding: 1rem;
    }

    .page-title {
      font-size: 2rem;
    }

    .dashboard-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .dashboard-actions {
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
