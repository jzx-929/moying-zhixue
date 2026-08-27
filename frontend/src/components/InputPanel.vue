<template>
  <div class="space-y-4">
    <div>
      <div class="flex items-center justify-between mb-2">
        <label class="block text-sm font-heading text-ink">输入古文</label>
        <button
          @click="triggerUpload"
          :disabled="ocrLoading"
          class="text-xs text-accent hover:underline"
        >
          {{ ocrLoading ? '识别中...' : '图片识别文字' }}
        </button>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleUpload"
        />
      </div>
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
        <option value="儒家">儒家</option>
        <option value="道家">道家</option>
        <option value="史家">史家</option>
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

    <div v-if="ocrError" class="text-shu text-sm bg-shu/5 border border-shu/20 rounded-lg p-3">
      {{ ocrError }}
    </div>

    <div v-if="store.error" class="text-shu text-sm bg-shu/5 border border-shu/20 rounded-lg p-3">
      {{ store.error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useWorkshopStore } from '../stores/workshop'
import { recognizeImage } from '../api/ocr'

const store = useWorkshopStore()
const fileInput = ref(null)
const ocrLoading = ref(false)
const ocrError = ref(null)

function triggerUpload() {
  fileInput.value?.click()
}

async function handleUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  ocrLoading.value = true
  ocrError.value = null
  try {
    const data = await recognizeImage(file, false)
    if (data.text) {
      store.inputText = data.text
    } else if (data.error) {
      ocrError.value = data.error
    }
  } catch (err) {
    ocrError.value = '图片识别失败：' + (err.message || '未知错误')
  } finally {
    ocrLoading.value = false
    e.target.value = ''
  }
}
</script>
