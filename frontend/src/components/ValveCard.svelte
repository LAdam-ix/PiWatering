<script>
  import { slide } from 'svelte/transition';
  import { action } from '../api.js';

  let { id, valve, refresh } = $props();
  let showTimer = $state(false);
  let mins = $state(5); // minutes, typed directly

  async function act(path, body) {
    await action(id, path, body);
    refresh?.();
  }
  function start() {
    const secs = Math.max(1, Math.round(mins * 60));
    showTimer = false;
    act('timer', new URLSearchParams({ duration: secs }));
  }
  function fmt(s) {
    const m = Math.floor(s / 60);
    return `${String(m).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
  }
</script>

<div class="card" class:unwired={!valve.wired}>
  <div class="head">
    <span class="label">{valve.label}</span>
    <span class="led" class:on={valve.open}></span>
  </div>

  {#if valve.timer_running}
    <div class="timerview">
      <div class="pausedtag">{valve.timer_paused ? 'Paused' : ''}</div>
      <div class="count">{fmt(valve.timer_remaining)}</div>
    </div>
    <div class="bar">
      {#if valve.timer_paused}
        <button class="t resume" onclick={() => act('timer/resume')}>Resume</button>
        <button class="t reset" onclick={() => act('timer/stop')}>Reset</button>
      {:else}
        <button class="t pause" onclick={() => act('timer/pause')}>Pause</button>
        <button class="t stop" onclick={() => act('timer/stop')}>Stop</button>
      {/if}
    </div>
  {:else}
    <div class="onoff">
      <button class="off" class:active={!valve.open} onclick={() => act('close')}>Off</button>
      <button class="on" class:active={valve.open} onclick={() => act('open')}>On</button>
    </div>

    <button class="handle" onclick={() => (showTimer = !showTimer)}>
      {#if !showTimer}<span class="chev">⌃</span>{/if}
      <span class="htxt">Timer</span>
      {#if showTimer}<span class="chev">⌄</span>{/if}
    </button>

    {#if showTimer}
      <div class="drawer" transition:slide={{ duration: 200 }}>
        <div class="valwrap">
          <span class="vlabel">Minutes</span>
          <input class="val" type="number" min="1" list="p-{id}" bind:value={mins} />
        </div>
        <datalist id="p-{id}">
          <option value="1"></option><option value="5"></option>
          <option value="10"></option><option value="15"></option>
          <option value="30"></option><option value="60"></option>
        </datalist>
        <button class="go" onclick={start}>Start<br />timer</button>
      </div>
    {/if}
  {/if}
</div>

<style>
  .card {
    background: linear-gradient(#aab2bb, #97a0aa);
    border: 2px solid #6c747d; border-radius: 2px;
    padding: 8px; aspect-ratio: 1; overflow: hidden;   /* fixed box, scales with width */
    display: flex; flex-direction: column; gap: 6px;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, .25);
  }
  .card.unwired { opacity: .6; }

  .head { display: flex; align-items: center; justify-content: space-between; flex: none; }
  .label { font-weight: 800; font-size: 13px; text-transform: uppercase; letter-spacing: .06em; color: #111; }

  .led {
    width: 16px; height: 16px; border-radius: 50%; flex: none;
    background: radial-gradient(circle at 35% 28%, #ff9a9a 0%, #e11d1d 45%, #7f1010 100%);
    box-shadow: inset 0 -1px 2px rgba(0, 0, 0, .45), 0 0 2px rgba(0, 0, 0, .35);
  }
  .led.on {
    background: radial-gradient(circle at 35% 28%, #d6ffe2 0%, #00e676 42%, #008f43 100%);
    box-shadow: inset 0 -1px 2px rgba(0, 0, 0, .35), 0 0 4px 1px #00e676, 0 0 10px 2px rgba(0, 230, 118, .7);
  }

  .timerview { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; }
  .pausedtag { height: 22px; line-height: 22px; font-size: 20px; font-weight: 800; text-transform: uppercase; letter-spacing: .08em; color: #ff5722; }
  .count { font-size: 34px; font-weight: 800; line-height: 1; color: #0a3d18; font-variant-numeric: tabular-nums; }

  /* On/Off: flex:1 so it shrinks to absorb the drawer => card box never changes */
  .onoff { display: flex; gap: 4px; flex: 1; min-height: 22px; }
  .onoff button {
    flex: 1; border: 0; border-radius: 2px; cursor: pointer; font-weight: 800;
    font-size: 18px; text-transform: uppercase; letter-spacing: .05em; color: #000;
    box-shadow: inset 2px 2px 0 rgba(255, 255, 255, .35),
                inset -2px -2px 0 rgba(0, 0, 0, .4),
                2px 2px 3px rgba(0, 0, 0, .35);
  }
  .onoff button.active {
    color: #fff; text-shadow: 0 1px 2px rgba(0, 0, 0, .5);
    box-shadow: inset 3px 3px 6px rgba(0, 0, 0, .55);
  }
  .onoff .off { background: #ff0000; }
  .onoff .on { background: #00d800; }

  /* small text pull-up handle; chevron above when closed, below when open */
  .handle {
    flex: none; border: 0; background: transparent; cursor: pointer; width: 100%;
    display: flex; flex-direction: column; align-items: center; gap: 0;
    color: #3a4250; font-size: 9px; font-weight: 700;
    text-transform: uppercase; letter-spacing: .08em; padding: 0;
  }
  .handle .htxt { line-height: 9px; }
  .handle .chev { font-size: 11px; line-height: 6px; }

  /* timer settings: small unstyled field + square Start, animates in */
  .drawer { flex: none; display: flex; align-items: flex-end; gap: 6px; }
  .valwrap { position: relative; flex: 1; min-width: 0; display: flex; }
  .vlabel {
    position: absolute; top: -5px; left: 1px; pointer-events: none;
    font-size: 9px; font-weight: 700; line-height: 1; color: #2f5d8a; text-transform: uppercase;
  }
  .val {
    width: 100%; border: 0; border-radius: 3px;
    background: rgba(255, 255, 255, .5);
    box-shadow: inset 0 0 0 1px rgba(0, 0, 0, .12);
    padding: 5px 7px; font-size: 13px; text-align: right;
    -moz-appearance: textfield; appearance: textfield;   /* no spinner */
  }
  .val::-webkit-outer-spin-button, .val::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
  .go {
    flex: none; width: 40px; border: 0; border-radius: 2px;
    background: #00b800; color: #fff; cursor: pointer;
    font-size: 9px; font-weight: 800; text-transform: uppercase; line-height: 1.1; text-align: center;
    display: flex; align-items: center; justify-content: center; padding: 6px 2px;
    box-shadow: inset 2px 2px 0 rgba(255, 255, 255, .35),
                inset -2px -2px 0 rgba(0, 0, 0, .4),
                2px 2px 3px rgba(0, 0, 0, .35);
  }
  .go:active { box-shadow: inset 3px 3px 6px rgba(0, 0, 0, .55); }

  .bar { display: flex; gap: 6px; flex: none; }
  .t {
    flex: 1; border: 0; border-radius: 2px; color: #fff; font-size: 13px; font-weight: 700;
    text-transform: uppercase; cursor: pointer; padding: 8px;
    box-shadow: inset 2px 2px 0 rgba(255, 255, 255, .15),
                inset -2px -2px 0 rgba(0, 0, 0, .5),
                2px 2px 3px rgba(0, 0, 0, .35);
  }
  .t:active { box-shadow: inset 3px 3px 6px rgba(0, 0, 0, .6); }
  .pause { background: #ff5722; }
  .resume { background: #00b800; }
  .stop, .reset { background: #e11d1d; }
</style>
