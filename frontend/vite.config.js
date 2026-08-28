import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Dev server binds to localhost only, matching the Django backend's
// 127.0.0.1-only posture (see project ARCHITECTURE.md: "no LAN exposure").
export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: 5173,
    proxy: {
      // Once the DRF layer exists, uncomment so /api calls in dev
      // reach Django without CORS config:
      // '/api': 'http://127.0.0.1:8000',
    },
  },
})
