<script>
  import ValveCard from '../components/ValveCard.svelte';
  import { status } from '../api.js';

  let valves = $state({});
  async function load() { valves = await status(); }

  load();
  setInterval(load, 1000);

  let zones = $derived(Object.entries(valves).filter(([, v]) => v.role === 'zone'));
</script>

<div class="grid">
  {#each zones as [id, v] (id)}
    <ValveCard {id} valve={v} refresh={load} />
  {/each}
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
  }
</style>
