<script>
  import Control from './views/Control.svelte';

  let tab = $state('control');
  const tabs = [
    { id: 'home', label: 'Home', icon: '🏠' },
    { id: 'control', label: 'Control', icon: '🎛️' },
    { id: 'data', label: 'Data', icon: '📊' },
    { id: 'logs', label: 'Logs', icon: '📜' },
    { id: 'settings', label: 'Settings', icon: '⚙️' },
  ];
  let current = $derived(tabs.find((t) => t.id === tab));
</script>

<header>PiWater</header>

<main>
  {#if tab === 'control'}
    <Control />
  {:else}
    <div class="placeholder">
      <div class="ph-icon">{current.icon}</div>
      <p>{current.label} — coming soon</p>
    </div>
  {/if}
</main>

<nav class="tabbar">
  {#each tabs as t}
    <button class:active={tab === t.id} onclick={() => (tab = t.id)}>
      <span class="icon">{t.icon}</span>
      <span class="tlabel">{t.label}</span>
    </button>
  {/each}
</nav>

<style>
  header {
    background: #15803d; color: #fff; padding: 14px 16px;
    font-size: 18px; font-weight: 700; position: sticky; top: 0; z-index: 1;
  }
  main { max-width: 720px; margin: 0 auto; padding: 12px 12px 84px; }
  .placeholder { text-align: center; color: #94a3b8; padding: 56px 12px; }
  .ph-icon { font-size: 40px; margin-bottom: 8px; }
  .tabbar {
    position: fixed; bottom: 0; left: 0; right: 0; display: flex;
    background: #fff; border-top: 1px solid #e2e8f0;
  }
  .tabbar button {
    flex: 1; border: 0; background: none; padding: 8px 0 10px;
    display: flex; flex-direction: column; align-items: center; gap: 2px;
    font-size: 11px; color: #94a3b8; cursor: pointer;
  }
  .tabbar button.active { color: #15803d; }
  .tabbar .icon { font-size: 20px; }
</style>
