<script>
  import { onDestroy } from 'svelte';
  import ValveCard from '../components/ValveCard.svelte';
  import { status } from '../api.js';

  let valves = $state({});
  let timer;

  // Adaptive polling: 1s while a timer is actively counting (smooth countdown),
  // 5s otherwise. Future automation runs via timers/valve state too, so it
  // auto-speeds-up whenever something is active.
  async function tick() {
    clearTimeout(timer);
    valves = await status();
    const active = Object.values(valves).some((v) => v.timer_running && !v.timer_paused);
    timer = setTimeout(tick, active ? 500 : 5000);
  }
  tick();
  onDestroy(() => clearTimeout(timer));

  let zones = $derived(Object.entries(valves).filter(([, v]) => v.role === 'zone'));
</script>

<div class="grid">
  {#each zones as [id, v] (id)}
    <ValveCard {id} valve={v} refresh={tick} />
  {/each}
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
  }
</style>
