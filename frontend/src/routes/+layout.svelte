<script lang="ts">
  import { onMount } from 'svelte';

  let currentPath = '/';
  
  onMount(() => {
    // Check if we're in browser environment
    if (typeof window !== 'undefined') {
      currentPath = window.location.hash.slice(1) || '/';
      
      // Listen for hash changes
      const handleHashChange = () => {
        currentPath = window.location.hash.slice(1) || '/';
      };
      
      window.addEventListener('hashchange', handleHashChange);
      
      return () => {
        window.removeEventListener('hashchange', handleHashChange);
      };
    }
  });

  const navItems = [
    { path: '/', label: 'Chat', icon: '💬' },
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/history', label: 'History', icon: '📜' }
  ];

  function isActive(path: string): boolean {
    return currentPath === path;
  }

  function handleNavClick(path: string) {
    window.location.hash = path;
  }
</script>

<div class="app-layout">
  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1 class="app-title">
        <span class="app-icon">🤖</span>
        <span class="title-text">RAG Assistant</span>
      </h1>
    </div>
    
    <nav class="sidebar-nav">
      {#each navItems as item}
        <a 
          href="#{item.path}" 
          class="nav-item" 
          class:active={isActive(item.path)}
          title={item.label}
          on:click|preventDefault={() => handleNavClick(item.path)}
        >
          <span class="nav-icon">{item.icon}</span>
          <span class="nav-label">{item.label}</span>
        </a>
      {/each}
    </nav>

    <div class="sidebar-footer">
      <div class="footer-info">
        <p class="app-version">v1.0.0</p>
        <p class="app-description">AI-Powered Knowledge Assistant</p>
      </div>
    </div>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    <header class="main-header">
      <div class="breadcrumb">
        {#each navItems as item}
          {#if isActive(item.path)}
            <span class="breadcrumb-current">
              <span class="breadcrumb-icon">{item.icon}</span>
              {item.label}
            </span>
          {/if}
        {/each}
      </div>
      
      <div class="header-actions">
        <div class="connection-status">
          <span class="status-dot"></span>
          <span class="status-text">Connected</span>
        </div>
      </div>
    </header>

    <div class="content-area">
      <slot />
    </div>
  </main>
</div>

<style>
  .app-layout {
    display: flex;
    height: 100vh;
    background: #f8f9fa;
  }

  /* Sidebar Styles */
  .sidebar {
    width: 260px;
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    flex-direction: column;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    position: relative;
    z-index: 100;
  }

  .sidebar-header {
    padding: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .app-title {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.25rem;
    font-weight: 700;
    margin: 0;
    color: white;
  }

  .app-icon {
    font-size: 1.5rem;
  }

  .title-text {
    background: linear-gradient(45deg, #ffffff, #e2e8f0);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .sidebar-nav {
    flex: 1;
    padding: 1rem 0;
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: all 0.3s ease;
    font-weight: 500;
    border-right: 3px solid transparent;
  }

  .nav-item:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }

  .nav-item.active {
    background: rgba(255, 255, 255, 0.15);
    color: white;
    border-right-color: #ffffff;
  }

  .nav-icon {
    font-size: 1.2rem;
    width: 24px;
    text-align: center;
  }

  .nav-label {
    font-size: 0.95rem;
  }

  .sidebar-footer {
    padding: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .footer-info {
    text-align: center;
  }

  .app-version {
    font-size: 0.8rem;
    font-weight: 600;
    margin: 0 0 0.25rem 0;
    color: rgba(255, 255, 255, 0.9);
  }

  .app-description {
    font-size: 0.75rem;
    margin: 0;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.3;
  }

  /* Main Content Styles */
  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .main-header {
    background: white;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }

  .breadcrumb {
    display: flex;
    align-items: center;
  }

  .breadcrumb-current {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: #2d3748;
  }

  .breadcrumb-icon {
    font-size: 1.2rem;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .connection-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: #718096;
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #48bb78;
    animation: pulse 2s infinite;
  }

  .status-text {
    font-weight: 500;
  }

  .content-area {
    flex: 1;
    overflow: auto;
    background: #f8f9fa;
  }

  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .app-layout {
      flex-direction: column;
    }

    .sidebar {
      width: 100%;
      height: auto;
      flex-direction: row;
      padding: 0;
    }

    .sidebar-header {
      padding: 1rem;
      border-bottom: none;
      border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    .app-title {
      font-size: 1rem;
    }

    .title-text {
      display: none;
    }

    .sidebar-nav {
      flex: 1;
      padding: 0;
      display: flex;
      overflow-x: auto;
    }

    .nav-item {
      flex-direction: column;
      gap: 0.25rem;
      padding: 0.75rem 1rem;
      min-width: 80px;
      text-align: center;
      border-right: none;
      border-bottom: 3px solid transparent;
    }

    .nav-item.active {
      border-bottom-color: #ffffff;
      border-right-color: transparent;
    }

    .nav-icon {
      font-size: 1.1rem;
    }

    .nav-label {
      font-size: 0.75rem;
    }

    .sidebar-footer {
      display: none;
    }

    .main-header {
      padding: 0.75rem 1rem;
    }

    .breadcrumb-current {
      font-size: 1rem;
    }

    .connection-status {
      font-size: 0.8rem;
    }
  }
</style>
