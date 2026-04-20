import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/uploads': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/monitor': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/monitor/, ''),   // 关键：去掉 /monitor 前缀
      },
      '/tools': {
        target: 'http://localhost:5002',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/tools/, ''),     // Streamlit 不需要子路径
      },
      // 新增：代理监测服务的静态文件
      '/static': {
        target: 'http://localhost:5001',
        changeOrigin: true
      },
      '/tools': {
        target: 'http://localhost:5002',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/tools/, '')
      }
    },
  },
  build: {
    outDir: 'dist',
  },
})