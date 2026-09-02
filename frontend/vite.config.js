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
      // Now that Django serves real /api/ routes (see config/urls.py),
      // forward dev-server requests there so the frontend can keep using
      // relative paths like fetch('/api/accounts/') without hardcoding
      // http://127.0.0.1:8000 or dealing with CORS.
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
