<script lang="ts">
  export let title: string;
  export let value: number | string;
  export let icon: string;
  export let description: string;
  export let isLoading = false;
  export let color: 'blue' | 'green' | 'purple' | 'orange' = 'blue';

  const colorClasses = {
    blue: 'border-blue-200 bg-blue-50',
    green: 'border-green-200 bg-green-50',
    purple: 'border-purple-200 bg-purple-50',
    orange: 'border-orange-200 bg-orange-50'
  };

  const iconColorClasses = {
    blue: 'text-blue-600',
    green: 'text-green-600',
    purple: 'text-purple-600',
    orange: 'text-orange-600'
  };

  function formatValue(val: number | string): string {
    if (typeof val === 'number') {
      return val.toLocaleString('id-ID');
    }
    return val;
  }
</script>

<div class="dashboard-card {colorClasses[color]}" class:loading={isLoading}>
  <div class="card-header">
    <div class="icon-container {iconColorClasses[color]}">
      <span class="icon">{icon}</span>
    </div>
    <div class="card-info">
      <h3 class="card-title">{title}</h3>
      <p class="card-description">{description}</p>
    </div>
  </div>
  
  <div class="card-value">
    {#if isLoading}
      <div class="loading-skeleton"></div>
    {:else}
      <span class="value-number">{formatValue(value)}</span>
    {/if}
  </div>
</div>

<style>
  .dashboard-card {
    background: white;
    border: 2px solid;
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .dashboard-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  }

  .dashboard-card.loading {
    opacity: 0.7;
  }

  .card-header {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .icon-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.8);
    flex-shrink: 0;
  }

  .icon {
    font-size: 1.5rem;
  }

  .card-info {
    flex: 1;
    min-width: 0;
  }

  .card-title {
    font-size: 1rem;
    font-weight: 600;
    color: #2d3748;
    margin: 0 0 0.25rem 0;
    line-height: 1.2;
  }

  .card-description {
    font-size: 0.875rem;
    color: #718096;
    margin: 0;
    line-height: 1.3;
  }

  .card-value {
    display: flex;
    align-items: center;
    min-height: 48px;
  }

  .value-number {
    font-size: 2rem;
    font-weight: 700;
    color: #2d3748;
    line-height: 1;
  }

  .loading-skeleton {
    width: 80px;
    height: 32px;
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    border-radius: 6px;
    animation: shimmer 1.5s infinite;
  }

  @keyframes shimmer {
    0% {
      background-position: -200% 0;
    }
    100% {
      background-position: 200% 0;
    }
  }

  /* Color variations */
  .border-blue-200 { border-color: #bee3f8; }
  .bg-blue-50 { background-color: #ebf8ff; }
  .text-blue-600 { color: #3182ce; }

  .border-green-200 { border-color: #c6f6d5; }
  .bg-green-50 { background-color: #f0fff4; }
  .text-green-600 { color: #38a169; }

  .border-purple-200 { border-color: #e9d8fd; }
  .bg-purple-50 { background-color: #faf5ff; }
  .text-purple-600 { color: #805ad5; }

  .border-orange-200 { border-color: #fbd38d; }
  .bg-orange-50 { background-color: #fffaf0; }
  .text-orange-600 { color: #dd6b20; }

  @media (max-width: 768px) {
    .dashboard-card {
      padding: 1rem;
    }

    .card-header {
      gap: 0.75rem;
      margin-bottom: 0.75rem;
    }

    .icon-container {
      width: 40px;
      height: 40px;
    }

    .icon {
      font-size: 1.25rem;
    }

    .card-title {
      font-size: 0.9rem;
    }

    .card-description {
      font-size: 0.8rem;
    }

    .value-number {
      font-size: 1.5rem;
    }
  }
</style>
