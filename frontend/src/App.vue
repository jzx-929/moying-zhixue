<template>
  <div class="min-h-screen bg-paper">
    <NavHeader />
    <main class="max-w-7xl mx-auto px-4 py-8">
      <router-view />
    </main>
    <footer class="border-t border-border mt-12">
      <div class="max-w-7xl mx-auto px-4 py-6 text-center text-sm text-ink-muted">
        <p class="font-heading">墨影智学 · 文本-漫画-动画跨媒介教学智能体</p>
        <p class="mt-1">古文入画 · 以画承文 · 以画研文</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import NavHeader from './components/NavHeader.vue'
</script>
