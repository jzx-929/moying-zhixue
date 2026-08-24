<template>
  <div>
    <div class="text-center mb-8">
      <h1 class="font-heading text-4xl font-bold text-ink tracking-widest mb-2">墨漫工坊</h1>
      <p class="text-ink-muted">古文 → 检索 → 分镜 → 水墨画面</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
      <div class="lg:col-span-2">
        <div class="card p-6">
          <InputPanel />
        </div>
      </div>
      <div class="lg:col-span-3">
        <div class="card p-6">
          <ResultPanel />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import InputPanel from '../components/InputPanel.vue'
import ResultPanel from '../components/ResultPanel.vue'
</script>
