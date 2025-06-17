// File: vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
// Removed @tailwindcss/vite plugin since it's no longer installed

export default defineConfig({
  plugins: [react()],
});
