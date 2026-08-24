<template>
  <div class="space-y-4">
    <div>
      <label class="block text-sm font-heading text-ink mb-2">输入古文</label>
      <textarea
        v-model="store.inputText"
        class="input-area h-32 resize-none"
        placeholder="粘贴一段诸子百家原文，如：子曰：学而时习之，不亦说乎"
      ></textarea>
    </div>

    <div class="flex items-center gap-2">
      <label class="text-sm text-ink-light">学派筛选：</label>
      <select
        v-model="store.school"
        class="bg-paper2 border border-border rounded-lg px-3 py-1.5 text-sm text-ink focus:outline-none focus:border-accent"
      >
        <option :value="null">全部</option>
        <option value="论语">论语</option>
        <option value="庄子">庄子</option>
        <option value="孟子">孟子</option>
        <option value="道德经">道德经</option>
        <option value="史记">史记</option>
      </select>
    </div>

    <div class="flex gap-3">
      <button
        @click="store.search()"
        :disabled="store.loading"
        class="btn-ghost"
      >
        <span v-if="store.loading">检索中...</span>
        <span v-else>检索素材</span>
      </button>
      <button
        @click="store.runGenerate()"
        :disabled="store.loading"
        class="btn-primary"
      >
        <span v-if="store.loading">生成中...</span>
        <span v-else>开始创作</span>
      </button>
    </div>

    <div v-if="store.error" class="text-shu text-sm bg-shu/5 border border-shu/20 rounded-lg p-3">
      {{ store.error }}
    </div>
  </div>
</template>

<script setup>
import { useWorkshopStore } from '../stores/workshop'
const store = useWorkshopStore()
</script>
