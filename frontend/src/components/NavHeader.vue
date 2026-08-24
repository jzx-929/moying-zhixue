<template>
  <header class="bg-ink text-paper2 border-b border-ink/light">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      <router-link to="/" class="flex items-center gap-3">
        <span class="w-10 h-10 bg-shu text-white rounded flex items-center justify-center font-heading text-lg">墨</span>
        <div>
          <div class="font-heading text-xl font-bold tracking-wider">墨影智学</div>
          <div class="text-xs text-ink-muted -mt-1">文本 · 漫画 · 动画</div>
        </div>
      </router-link>

      <nav class="flex items-center gap-1">
        <router-link
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="px-4 py-2 rounded-lg text-sm font-body transition-colors"
          :class="$route.name === link.name ? 'bg-accent text-white' : 'text-paper2/80 hover:bg-ink/light hover:text-paper2'"
        >
          {{ link.label }}
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const navLinks = [
  { to: '/', name: 'Home', label: '首页' },
  { to: '/workshop', name: 'Workshop', label: '墨漫工坊' },
  { to: '/about', name: 'About', label: '关于' },
]
</script>
