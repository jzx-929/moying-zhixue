<template>
  <div class="space-y-6">
    <div v-if="store.ragResults.length > 0">
      <h3 class="font-heading text-base text-ink mb-3">RAG 检索结果</h3>
      <div class="space-y-2">
        <div
          v-for="(item, i) in store.ragResults"
          :key="i"
          class="card p-4"
        >
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs px-2 py-0.5 bg-olive-soft text-olive rounded-full font-body">{{ item.school }}</span>
            <span class="text-xs text-ink-muted">相似度 {{ (item.similarity * 100).toFixed(1) }}%</span>
          </div>
          <p class="text-sm text-ink leading-relaxed">{{ item.text }}</p>
          <p class="text-xs text-ink-muted mt-1">{{ item.source }}{{ item.chapter ? ' · ' + item.chapter : '' }}</p>
        </div>
      </div>
    </div>

    <div v-if="store.textOutput">
      <h3 class="font-heading text-base text-ink mb-3">文改 Agent 输出</h3>
      <div class="card p-4 space-y-3">
        <div>
          <span class="text-xs text-ink-muted">出处</span>
          <p class="text-sm text-ink mt-1">{{ store.textOutput.source }}</p>
        </div>
        <div>
          <span class="text-xs text-ink-muted">白话翻译</span>
          <p class="text-sm text-ink mt-1">{{ store.textOutput.translation }}</p>
        </div>
        <div v-if="store.textOutput.storyboard">
          <span class="text-xs text-ink-muted">分镜</span>
          <div class="grid grid-cols-2 gap-2 mt-2">
            <div
              v-for="(shot, i) in store.textOutput.storyboard"
              :key="i"
              class="bg-paper2 border border-border rounded-lg p-3"
            >
              <div class="text-xs text-ink-muted mb-1">第 {{ shot.shot }} 格</div>
              <div class="text-sm text-ink">{{ shot.visual }}</div>
              <div class="text-xs text-ink-light mt-1">「{{ shot.text }}」</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="store.visualOutput">
      <h3 class="font-heading text-base text-ink mb-3">墨影画风 Agent 输出</h3>
      <div class="card p-4">
        <div v-if="store.visualOutput.frames" class="grid grid-cols-2 gap-3">
          <div
            v-for="(frame, i) in store.visualOutput.frames"
            :key="i"
            class="bg-paper2 border border-border rounded-lg p-3"
          >
            <div class="text-xs text-ink-muted mb-1">第 {{ frame.shot }} 帧</div>
            <div class="text-sm text-ink">{{ frame.composition }}</div>
            <div class="text-xs text-ink-light mt-1">墨色：{{ frame.ink_density }}</div>
            <div class="text-xs text-ink-muted">留白：{{ frame.whitespace }}</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!store.ragResults.length && !store.textOutput && !store.visualOutput && !store.loading" class="text-center py-12">
      <div class="text-5xl mb-4 opacity-20">墨</div>
      <p class="text-ink-muted text-sm">输入古文后点击"检索素材"或"开始创作"</p>
    </div>
  </div>
</template>

<script setup>
import { useWorkshopStore } from '../stores/workshop'
const store = useWorkshopStore()
</script>
