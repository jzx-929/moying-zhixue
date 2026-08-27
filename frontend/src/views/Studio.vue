<template>
  <div>
    <div class="text-center mb-8">
      <h1 class="font-heading text-4xl font-bold text-ink tracking-widest mb-2">文影创作坊</h1>
      <p class="text-ink-muted">白话小说 → 剧本改编 → 多风格影视短片</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        class="card p-6 text-left transition-all"
        :class="activeTab === tab.key ? 'ring-2 ring-accent bg-accent/5' : 'hover:bg-paper2'"
      >
        <div class="text-3xl mb-3">{{ tab.icon }}</div>
        <h3 class="font-heading text-lg text-ink mb-2">{{ tab.label }}</h3>
        <p class="text-sm text-ink-light leading-relaxed">{{ tab.desc }}</p>
      </button>
    </div>

    <!-- 小说改编 -->
    <div v-if="activeTab === 'adapt'" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card p-6">
        <h2 class="font-heading text-xl text-ink mb-4">输入小说原文</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-heading text-ink mb-2">小说标题</label>
            <input
              v-model="novelTitle"
              type="text"
              class="input-area h-10"
              placeholder="输入小说标题"
            />
          </div>

          <div>
            <label class="block text-sm font-heading text-ink mb-2">
              故事内容
              <span class="text-ink-muted font-body ml-1">{{ novelText.length }} 字</span>
            </label>
            <textarea
              v-model="novelText"
              class="input-area h-64 resize-none"
              placeholder="粘贴你的短篇小说内容..."
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-heading text-ink mb-2">目标风格</label>
            <div class="grid grid-cols-2 gap-2">
              <button
                v-for="style in styles"
                :key="style.key"
                @click="selectedStyle = style.key"
                class="p-3 rounded-lg text-left transition-colors text-sm"
                :class="selectedStyle === style.key ? 'bg-accent text-white' : 'bg-paper2 border border-border hover:bg-paper text-ink'"
              >
                <span class="text-lg">{{ style.icon }}</span>
                <span class="ml-2">{{ style.label }}</span>
              </button>
            </div>
          </div>

          <button
            @click="adaptNovel"
            :disabled="adapting"
            class="btn-primary w-full"
          >
            <span v-if="adapting">改编中...</span>
            <span v-else>开始改编剧本</span>
          </button>
        </div>
      </div>

      <div class="card p-6">
        <h2 class="font-heading text-xl text-ink mb-4">剧本输出</h2>
        <div v-if="!scriptResult" class="text-center py-16">
          <div class="text-5xl mb-4 opacity-20">剧</div>
          <p class="text-ink-muted text-sm">输入小说后点击"开始改编剧本"</p>
        </div>
        <div v-else class="space-y-4">
          <div v-if="scriptIsMock || scriptSaved" class="flex items-center justify-between gap-2 px-3 py-2 bg-gold/5 border border-gold/20 rounded-lg">
            <div v-if="scriptIsMock" class="flex items-center gap-2">
              <span class="text-xs font-bold text-gold">AI</span>
              <span class="text-xs text-ink-light">以上内容由 AI 生成，仅供参考</span>
            </div>
            <div v-if="scriptSaved" class="text-xs text-ink-muted flex items-center gap-1">
              <span class="text-accent">🔖</span> 已保存到历史记录
            </div>
          </div>

          <div class="bg-paper2 border border-border rounded-lg p-4">
            <div class="text-xs text-ink-muted mb-1">片名</div>
            <div class="font-heading text-lg text-ink">{{ scriptResult.title }}</div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div class="bg-paper2 border border-border rounded-lg p-3">
              <div class="text-xs text-ink-muted mb-1">类型</div>
              <div class="text-sm text-ink">{{ scriptResult.genre }}</div>
            </div>
            <div class="bg-paper2 border border-border rounded-lg p-3">
              <div class="text-xs text-ink-muted mb-1">时长</div>
              <div class="text-sm text-ink">{{ scriptResult.duration }}</div>
            </div>
          </div>

          <div v-if="scriptResult.characters" class="bg-paper2 border border-border rounded-lg p-4">
            <div class="text-xs text-ink-muted mb-1">主要角色</div>
            <div class="flex flex-wrap gap-2 mt-2">
              <span
                v-for="char in scriptResult.characters"
                :key="char"
                class="px-3 py-1 bg-accent/10 text-accent rounded-full text-sm"
              >
                {{ char }}
              </span>
            </div>
          </div>

          <div v-if="scriptResult.scenes" class="bg-paper2 border border-border rounded-lg p-4">
            <div class="text-xs text-ink-muted mb-2">场景分镜</div>
            <div class="space-y-3">
              <div
                v-for="(scene, i) in scriptResult.scenes"
                :key="i"
                class="p-3 bg-white border border-border rounded-lg"
              >
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-xs px-2 py-0.5 bg-olive-soft text-olive rounded-full">第{{ i + 1 }}场</span>
                  <span class="text-xs text-ink-muted">{{ scene.location }}</span>
                </div>
                <div class="text-sm text-ink mb-1">【{{ scene.action }}】</div>
                <div class="text-sm text-ink-light italic">"{{ scene.dialogue }}"</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 跨版本对照 -->
    <div v-if="activeTab === 'compare'" class="space-y-6">
      <div class="card p-6">
        <h2 class="font-heading text-xl text-ink mb-4">跨版本对照</h2>
        <p class="text-sm text-ink-light mb-6">同一故事的两种影视化呈现：写实风格 vs 水墨漫画风格</p>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <div class="text-center mb-3">
              <span class="px-3 py-1 bg-accent/10 text-accent rounded-full text-sm font-heading">写实影视版</span>
            </div>
            <div class="bg-paper2 border border-border rounded-lg aspect-video flex items-center justify-center">
              <div class="text-center text-ink-muted">
                <div class="text-5xl mb-3">🎬</div>
                <p class="text-sm">写实风格短片</p>
                <p class="text-xs mt-1">真人实拍质感</p>
              </div>
            </div>
            <div class="mt-3 text-sm text-ink-light">
              <p><strong>特点：</strong>真实场景、真人表演、自然光影</p>
              <p><strong>适用：</strong>现代题材、现实主义叙事</p>
            </div>
          </div>

          <div>
            <div class="text-center mb-3">
              <span class="px-3 py-1 bg-olive/10 text-olive rounded-full text-sm font-heading">水墨漫画版</span>
            </div>
            <div class="bg-paper2 border border-border rounded-lg aspect-video flex items-center justify-center">
              <div class="text-center text-ink-muted">
                <div class="text-5xl mb-3">🖼</div>
                <p class="text-sm">蔡志忠水墨风格</p>
                <p class="text-xs mt-1">极简线条 · 大量留白</p>
              </div>
            </div>
            <div class="mt-3 text-sm text-ink-light">
              <p><strong>特点：</strong>水墨晕染、极简线条、诗意留白</p>
              <p><strong>适用：</strong>国学经典、哲思故事</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 配音功能 -->
    <div v-if="activeTab === 'dub'" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card p-6">
        <h2 class="font-heading text-xl text-ink mb-4">配音复刻</h2>
        <p class="text-sm text-ink-light mb-4">为你的漫画动画添加蔡志忠风格简洁旁白</p>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-heading text-ink mb-2">配音风格</label>
            <select
              v-model="dubStyle"
              class="w-full bg-paper2 border border-border rounded-lg px-3 py-2 text-ink focus:outline-none focus:border-accent"
            >
              <option value="caizhizhong">蔡志忠旁白风格（简洁睿智）</option>
              <option value="gentle">温柔男声</option>
              <option value="clear">清澈女声</option>
              <option value="story">故事讲述者</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-heading text-ink mb-2">旁白文案</label>
            <textarea
              v-model="dubText"
              class="input-area h-32 resize-none"
              placeholder="输入需要配音的旁白文字..."
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-heading text-ink mb-2">语速调节</label>
            <input type="range" v-model="dubSpeed" min="0.5" max="2" step="0.1" class="w-full" />
            <div class="flex justify-between text-xs text-ink-muted">
              <span>慢</span><span>{{ dubSpeed }}x</span><span>快</span>
            </div>
          </div>

          <button
            @click="generateDub"
            :disabled="dubbing"
            class="btn-primary w-full"
          >
            <span v-if="dubbing">生成配音中...</span>
            <span v-else>生成配音</span>
          </button>
        </div>
      </div>

      <div class="card p-6">
        <h2 class="font-heading text-xl text-ink mb-4">配音预览</h2>
        <div v-if="!dubResult" class="text-center py-16">
          <div class="text-5xl mb-4 opacity-20">音</div>
          <p class="text-ink-muted text-sm">点击"生成配音"试听效果</p>
        </div>
        <div v-else class="space-y-6">
          <div v-if="dubSaved" class="flex items-center justify-end gap-2 px-3 py-2 bg-gold/5 border border-gold/20 rounded-lg">
            <div class="text-xs text-ink-muted flex items-center gap-1">
              <span class="text-accent">🔖</span> 已保存到历史记录
            </div>
          </div>

          <div class="bg-paper2 border border-border rounded-lg aspect-video flex items-center justify-center">
            <div class="text-center">
              <div class="text-5xl mb-3">🔊</div>
              <p class="text-sm text-ink-muted">配音已生成</p>
            </div>
          </div>

          <div class="bg-paper2 border border-border rounded-lg p-4">
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-heading text-ink">{{ dubResult.style }}</span>
              <span class="text-xs text-ink-muted">{{ dubResult.speed }}</span>
            </div>
            <div class="flex items-center gap-3">
              <button class="w-12 h-12 bg-accent text-white rounded-full flex items-center justify-center">
                ▶
              </button>
              <div class="flex-1 h-2 bg-border rounded-full overflow-hidden">
                <div class="h-full bg-accent w-1/3 rounded-full"></div>
              </div>
              <span class="text-xs text-ink-muted">{{ dubResult.duration_estimate }}</span>
            </div>
          </div>

          <div class="bg-paper2 border border-border rounded-lg p-4">
            <div class="text-xs text-ink-muted mb-2">配音文案</div>
            <p class="text-sm text-ink leading-relaxed">{{ dubResult.text }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { saveHistory } from '../api/history'

const activeTab = ref('adapt')

const tabs = [
  { key: 'adapt', icon: '📖', label: '小说改编', desc: '白话小说→剧本→多风格短片的完整创作流' },
  { key: 'compare', icon: '🎭', label: '跨版本对照', desc: '写实影视 vs 水墨漫画，同屏对比体验' },
  { key: 'dub', icon: '🎙', label: '配音复刻', desc: '蔡志忠简洁旁白风格配音生成' },
]

const styles = [
  { key: 'realistic', icon: '🎬', label: '写实风格' },
  { key: 'ink', icon: '🖌', label: '水墨风格' },
  { key: 'anime', icon: '🎨', label: '动漫风格' },
  { key: 'silent', icon: '🎞', label: '默片风格' },
]

const novelTitle = ref('')
const novelText = ref('')
const selectedStyle = ref('ink')
const adapting = ref(false)
const scriptResult = ref(null)
const scriptIsMock = ref(false)
const scriptSaved = ref(false)

async function adaptNovel() {
  if (!novelText.value.trim()) return
  adapting.value = true
  scriptSaved.value = false
  try {
    const res = await axios.post('/api/studio/adapt', {
      title: novelTitle.value,
      text: novelText.value,
      style: selectedStyle.value,
    })
    scriptResult.value = res.data.data.script
    scriptIsMock.value = res.data.data.mock || false

    try {
      await saveHistory({
        title: `剧本改编 · ${novelTitle.value || '未命名'}`,
        input_text: novelText.value,
        output_data: scriptResult.value,
        module: 'studio',
      })
      scriptSaved.value = true
    } catch (e) {
      console.error('历史记录保存失败', e)
    }
  } catch (e) {
    console.error('改编失败', e)
  } finally {
    adapting.value = false
  }
}

const dubStyle = ref('caizhizhong')
const dubText = ref('孔子说，学习是一件快乐的事情。有朋友从远方来，更是值得高兴。别人不了解自己，却不生气，这就是君子的风范。')
const dubSpeed = ref(1.0)
const dubbing = ref(false)
const dubResult = ref(null)
const dubSaved = ref(false)

async function generateDub() {
  if (!dubText.value.trim()) return
  dubbing.value = true
  dubSaved.value = false
  try {
    const res = await axios.post('/api/studio/dub', {
      text: dubText.value,
      style: dubStyle.value,
      speed: parseFloat(dubSpeed.value),
    })
    dubResult.value = res.data.data

    try {
      await saveHistory({
        title: `配音 · ${dubStyle.value}`,
        input_text: dubText.value,
        output_data: dubResult.value,
        module: 'studio',
      })
      dubSaved.value = true
    } catch (e) {
      console.error('历史记录保存失败', e)
    }
  } catch (e) {
    console.error('配音生成失败', e)
  } finally {
    dubbing.value = false
  }
}
</script>
