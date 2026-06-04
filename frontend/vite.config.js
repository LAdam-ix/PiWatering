import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  server: {
    // dev: proxy API calls to the Flask backend
    proxy: {
      '/valve': 'http://localhost:5000',
      '/valves': 'http://localhost:5000',
    },
  },
  build: { outDir: 'dist' },
});
