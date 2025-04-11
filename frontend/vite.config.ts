import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import { appConfig } from './app.config';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: appConfig().host,
    port: appConfig().port,
    watch: {
      usePolling: true,
    },
  },
});
