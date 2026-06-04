<script>
  import { action } from '../api.js';

  let { id, valve, refresh } = $props();
  let duration = $state('');

  async function act(path, body) {
    await action(id, path, body);
    refresh?.();
  }
</script>

<div class="valve" class:unwired={!valve.wired}>
  <div class="row">
    <span class="name">{valve.label}</span>
    <span class="state">
      {#if !valve.wired}not wired{:else}{valve.open ? 'OPEN' : 'closed'}{/if}
      {#if valve.timer_remaining > 0} · {valve.timer_remaining}s left{/if}
    </span>
  </div>
  <div class="btns">
    <button class="on" onclick={() => act('open')}>On</button>
    <button class="off" onclick={() => act('close')}>Off</button>
  </div>
  <div class="timerrow">
    <input type="number" min="1" placeholder="seconds" bind:value={duration} />
    <button class="timer" onclick={() => duration && act('timer', new URLSearchParams({ duration }))}>Timer</button>
    <button class="stop" onclick={() => act('timer/stop')}>Stop</button>
  </div>
</div>

<style>
  .valve { background: #fff; border-radius: 12px; padding: 14px; margin: 10px 0; box-shadow: 0 1px 3px rgba(0,0,0,.12); }
  .valve.unwired { opacity: .55; }
  .row { display: flex; align-items: center; justify-content: space-between; }
  .name { font-weight: 600; font-size: 16px; }
  .state { font-size: 13px; color: #777; }
  .btns, .timerrow { display: flex; gap: 8px; margin-top: 10px; }
  button { flex: 1; padding: 11px; border: 0; border-radius: 8px; font-size: 15px; color: #fff; cursor: pointer; }
  .on { background: #2e7d32; }
  .off { background: #c62828; }
  .timer { background: #1565c0; }
  .stop { background: #ef6c00; }
  input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; }
</style>
