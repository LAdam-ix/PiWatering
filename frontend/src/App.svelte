<script>
  import ValveCard from './components/ValveCard.svelte';
  import { status } from './api.js';

  let valves = $state({});
  async function load() { valves = await status(); }

  load();
  setInterval(load, 2000);

  let zones = $derived(Object.entries(valves).filter(([, v]) => v.role === 'zone'));
</script>

<header>PiWater · Control</header>
<main>
  {#each zones as [id, v] (id)}
    <ValveCard {id} valve={v} refresh={load} />
  {/each}
</main>
