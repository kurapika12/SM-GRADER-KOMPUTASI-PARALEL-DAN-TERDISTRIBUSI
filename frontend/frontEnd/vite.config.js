import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  plugins: [svelte()],
  server: {
    proxy: {
      '/getAnswerParticipant': 'http://localhost:3000',
      '/api': 'http://localhost:3000'
    }
  }
})