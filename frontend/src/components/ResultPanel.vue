<template>
  <div class="space-y-6">
    <!-- AI 生成内容标识 -->
    <div v-if="store.textOutput || store.visualOutput" class="flex items-center gap-2 px-3 py-2 bg-gold/5 border border-gold/20 rounded-lg">
      <span class="text-xs font-bold text-gold">AI</span>
      <span class="text-xs text-ink-light">以上内容由 AI 生成，仅供参考，请以原文为准</span>
    </div>

    <!-- 对话历史 -->
    <div v-if="store.chatHistory.length > 0" class="space-y-3 mb-4">
      <div
        v-for="(msg, i) in store.chatHistory"
        :key="i"
        class="flex gap-3"
      >
        <div
          class="w-8 h-8 rounded-full flex items-center justify-center text-xs flex-shrink-0"
          :class="msg.role === 'user' ? 'bg-accent text-white' : 'bg-olive/10 text-olive'"
        >
          {{ msg.role === 'user' ? '我' : '墨' }}
        </div>
        <div class="flex-1">
          <div class="text-xs text-ink-muted mb-1">{{ msg.role === 'user' ? '用户' : '墨影助手' }}</div>
          <div class="text-sm text-ink leading-relaxed bg-paper2 border border-border rounded-lg p-3">
            {{ msg.content }}
          </div>
        </div>
      </div>
    </div>

    <!-- 多轮对话输入 -->
    <div v-if="store.textOutput" class="flex gap-2">
      <input
        v-model="store.followUpText"
        @keyup.enter="store.followUp()"
        type="text"
        class="input-area h-10 flex-1 text-sm"
        placeholder="继续提问，如：第二格的画面能更详细吗？"
      />
      <button
        @click="store.followUp()"
        :disabled="store.loading"
        class="btn-ghost text-sm whitespace-nowrap"
      >
        追问
      </button>
    </div>

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
          <div class="flex items-center gap-1 mt-1">
            <span class="text-xs text-accent">📄 出处</span>
            <span class="text-xs text-ink-muted">{{ item.source }}{{ item.chapter ? ' · ' + item.chapter : '' }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="store.textOutput">
      <h3 class="font-heading text-base text-ink mb-3">文改 Agent 输出</h3>
      <div class="card p-4 space-y-3">
        <div>
          <span class="text-xs text-ink-muted">出处</span>
          <div class="flex items-center gap-1 mt-1">
            <span class="text-xs text-accent">📄</span>
            <p class="text-sm text-ink">{{ store.textOutput.source }}</p>
          </div>
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
        <!-- 可追溯标注 -->
        <div class="pt-2 border-t border-border">
          <div class="text-xs text-ink-muted">
            <span class="text-accent">🔖 知识来源：</span>
            RAG 检索自国学文本库（ChromaDB · {{ store.ragResults.length }} 条匹配）
            <span v-if="store.textOutput.source"> · 典籍出处：{{ store.textOutput.source }}</span>
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
        <!-- 可追溯标注 -->
        <div class="mt-3 pt-2 border-t border-border">
          <div class="text-xs text-ink-muted">
            <span class="text-accent">🔖 风格依据：</span>
            蔡志忠漫画范式五原则（线条≤5、留白≥40%、纯水墨、无五官、空灵构图）
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
