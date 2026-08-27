<template>
  <div>
    <div class="text-center mb-8">
      <h1 class="font-heading text-4xl font-bold text-ink tracking-widest mb-2">教学工作台</h1>
      <p class="text-ink-muted">助教课件生成 · 助学写作训练</p>
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

    <!-- 课件生成 -->
    <div v-if="activeTab === 'courseware'" class="space-y-6">
      <div class="card p-6">
        <h2 class="font-heading text-xl text-ink mb-4">课件一键生成</h2>
        <p class="text-sm text-ink-light mb-4">输入古文原文，自动生成白话文剧本 + 分格漫画 + 水墨动画三件套</p>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-heading text-ink mb-2">古文原文</label>
            <textarea
              v-model="coursewareInput"
              class="input-area h-24 resize-none"
              placeholder="粘贴一段古文，如：子曰：学而时习之，不亦说乎"
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-heading text-ink mb-2">篇目</label>
              <select
                v-model="coursewareSource"
                class="w-full bg-paper2 border border-border rounded-lg px-3 py-2 text-ink focus:outline-none focus:border-accent"
              >
                <option value="论语·学而">论语·学而</option>
                <option value="论语·为政">论语·为政</option>
                <option value="孟子·梁惠王">孟子·梁惠王</option>
                <option value="道德经·第一章">道德经·第一章</option>
                <option value="庄子·逍遥游">庄子·逍遥游</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-heading text-ink mb-2">适用年级</label>
              <select
                v-model="coursewareGrade"
                class="w-full bg-paper2 border border-border rounded-lg px-3 py-2 text-ink focus:outline-none focus:border-accent"
              >
                <option value="初中">初中</option>
                <option value="高中">高中</option>
                <option value="大学通识">大学通识</option>
              </select>
            </div>
          </div>

          <button
            @click="generateCourseware"
            :disabled="generating"
            class="btn-primary w-full"
          >
            <span v-if="generating">生成中...</span>
            <span v-else>生成教学课件</span>
          </button>
        </div>
      </div>

      <div v-if="coursewareResult" class="space-y-6">
        <div v-if="coursewareIsMock || coursewareSaved" class="flex items-center justify-between gap-2 px-3 py-2 bg-gold/5 border border-gold/20 rounded-lg">
          <div v-if="coursewareIsMock" class="flex items-center gap-2">
            <span class="text-xs font-bold text-gold">AI</span>
            <span class="text-xs text-ink-light">以上内容由 AI 生成，仅供参考，请以原文为准</span>
          </div>
          <div v-if="coursewareSaved" class="text-xs text-ink-muted flex items-center gap-1">
            <span class="text-accent">🔖</span> 已保存到历史记录
          </div>
        </div>

        <div class="card p-6">
          <h3 class="font-heading text-lg text-ink mb-4">📜 白话译文</h3>
          <div class="bg-paper2 border border-border rounded-lg p-4">
            <p class="text-ink leading-relaxed">{{ coursewareResult.translation }}</p>
          </div>
        </div>

        <div class="card p-6">
          <h3 class="font-heading text-lg text-ink mb-4">🎬 分格漫画</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div
              v-for="(panel, i) in coursewareResult.panels"
              :key="i"
              class="bg-paper2 border border-border rounded-lg overflow-hidden"
            >
              <div class="aspect-[4/3] bg-gradient-to-br from-paper to-paper2 flex items-center justify-center border-b border-border">
                <div class="text-center text-ink-muted">
                  <div class="text-4xl mb-2">🖼</div>
                  <div class="text-xs">第{{ i + 1 }}格</div>
                </div>
              </div>
              <div class="p-3">
                <div class="text-xs text-ink-muted mb-1">画面：{{ panel.visual }}</div>
                <div class="text-sm text-ink">「{{ panel.text }}」</div>
              </div>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <h3 class="font-heading text-lg text-ink mb-4">🎞 水墨动画</h3>
          <div class="bg-paper2 border border-border rounded-lg aspect-video flex items-center justify-center">
            <div class="text-center text-ink-muted">
              <div class="text-5xl mb-3">▶</div>
              <p class="text-sm">点击播放水墨动画短片</p>
              <p class="text-xs mt-1">时长：约 15 秒</p>
            </div>
          </div>
        </div>

        <div v-if="coursewareResult.teaching_plan" class="card p-6">
          <h3 class="font-heading text-lg text-ink mb-4">📝 教学设计建议</h3>
          <ul class="space-y-3 text-sm text-ink-light">
            <li v-for="(step, i) in coursewareResult.teaching_plan" :key="i" class="flex gap-3">
              <span class="text-accent font-bold">{{ i + 1 }}.</span>
              <span><strong>{{ step.phase }}（{{ step.duration }}）：</strong>{{ step.action }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 写作训练 -->
    <div v-if="activeTab === 'writing'" class="space-y-6">
      <div class="card p-6">
        <h2 class="font-heading text-xl text-ink mb-4">漫画式写作训练</h2>
        <p class="text-sm text-ink-light mb-4">根据漫画分镜搭建故事框架，填充文字剧本，双维度写作辅导</p>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-heading text-ink mb-2">选择主题</label>
            <select
              v-model="writingTheme"
              class="w-full bg-paper2 border border-border rounded-lg px-3 py-2 text-ink focus:outline-none focus:border-accent"
            >
              <option value="学习">学习与求知</option>
              <option value="友谊">友谊与交往</option>
              <option value="坚持">坚持与毅力</option>
              <option value="诚信">诚信与道德</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-heading text-ink mb-2">分镜格数</label>
            <div class="flex gap-2">
              <button
                v-for="n in [3, 4, 5, 6]"
                :key="n"
                @click="panelCount = n"
                class="px-4 py-2 rounded-lg text-sm transition-colors"
                :class="panelCount === n ? 'bg-accent text-white' : 'bg-paper2 text-ink border border-border hover:bg-paper'"
              >
                {{ n }} 格
              </button>
            </div>
          </div>

          <button
            @click="generateWritingFrame"
            :disabled="generating"
            class="btn-ghost w-full"
          >
            <span v-if="generating">生成中...</span>
            <span v-else>生成分镜框架</span>
          </button>
        </div>
      </div>

      <div v-if="writingPanels.length > 0" class="card p-6">
        <h3 class="font-heading text-lg text-ink mb-4">填写你的故事</h3>
        <div class="space-y-6">
          <div
            v-for="(panel, i) in writingPanels"
            :key="i"
            class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-paper2 border border-border rounded-lg"
          >
            <div>
              <label class="block text-xs text-ink-muted mb-1">第 {{ i + 1 }} 格 · 画面描述</label>
              <textarea
                v-model="panel.visual"
                class="input-area h-20 resize-none text-sm"
                placeholder="描述这一格的画面..."
              ></textarea>
            </div>
            <div>
              <label class="block text-xs text-ink-muted mb-1">第 {{ i + 1 }} 格 · 台词/旁白</label>
              <textarea
                v-model="panel.text"
                class="input-area h-20 resize-none text-sm"
                placeholder="填写人物台词或旁白..."
              ></textarea>
            </div>
          </div>
        </div>

        <div class="mt-6 flex gap-3">
          <button @click="getWritingFeedback" :disabled="generating" class="btn-primary flex-1">
            <span v-if="generating">分析中...</span>
            <span v-else>获取写作辅导</span>
          </button>
        </div>
      </div>

      <div v-if="writingFeedback" class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-heading text-lg text-ink">💡 写作辅导建议</h3>
          <div v-if="writingSaved" class="text-xs text-ink-muted flex items-center gap-1">
            <span class="text-accent">🔖</span> 已保存到历史记录
          </div>
        </div>
        <div class="space-y-4 text-sm text-ink-light">
          <div v-if="writingFeedback.strengths?.length" class="p-4 bg-olive-soft/30 border border-olive/20 rounded-lg">
            <p class="font-heading text-olive mb-1">✓ 做得好的地方</p>
            <ul class="space-y-1 ml-4 list-disc">
              <li v-for="s in writingFeedback.strengths" :key="s">{{ s }}</li>
            </ul>
          </div>
          <div v-if="writingFeedback.suggestions?.length" class="p-4 bg-accent/5 border border-accent/20 rounded-lg">
            <p class="font-heading text-accent mb-1">🔄 改进建议</p>
            <ul class="space-y-1 ml-4 list-disc">
              <li v-for="s in writingFeedback.suggestions" :key="s">{{ s }}</li>
            </ul>
          </div>
          <div v-if="writingFeedback.fill_rate !== undefined" class="text-xs text-ink-muted">
            完成率：{{ (writingFeedback.fill_rate * 100).toFixed(0) }}%
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

const activeTab = ref('courseware')

const tabs = [
  { key: 'courseware', icon: '📚', label: '课件生成', desc: '古文→白话文+分格漫画+水墨动画，一键生成教学三件套' },
  { key: 'writing', icon: '✍️', label: '写作训练', desc: '漫画分镜搭建故事框架，双维度写作辅导' },
]

const coursewareInput = ref('子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？')
const coursewareSource = ref('论语·学而')
const coursewareGrade = ref('高中')
const generating = ref(false)
const coursewareResult = ref(null)
const coursewareIsMock = ref(false)
const coursewareSaved = ref(false)

async function generateCourseware() {
  if (!coursewareInput.value.trim()) return
  generating.value = true
  coursewareSaved.value = false
  try {
    const res = await axios.post('/api/workbench/courseware', {
      text: coursewareInput.value,
      source: coursewareSource.value,
      grade: coursewareGrade.value,
    })
    coursewareResult.value = res.data.data.courseware
    coursewareIsMock.value = res.data.data.mock || false

    try {
      await saveHistory({
        title: `${coursewareSource.value} · ${coursewareGrade.value}课件`,
        input_text: coursewareInput.value,
        output_data: coursewareResult.value,
        module: 'workbench',
      })
      coursewareSaved.value = true
    } catch (e) {
      console.error('历史记录保存失败', e)
    }
  } catch (e) {
    console.error('课件生成失败', e)
  } finally {
    generating.value = false
  }
}

const writingTheme = ref('学习')
const panelCount = ref(4)
const writingPanels = ref([])
const writingFeedback = ref(null)
const writingSaved = ref(false)

async function generateWritingFrame() {
  generating.value = true
  try {
    const res = await axios.post('/api/workbench/writing/frame', {
      theme: writingTheme.value,
      panel_count: panelCount.value,
    })
    writingPanels.value = res.data.data.panels || []
    writingFeedback.value = null
  } catch (e) {
    console.error('分镜框架生成失败', e)
  } finally {
    generating.value = false
  }
}

async function getWritingFeedback() {
  generating.value = true
  writingSaved.value = false
  try {
    const res = await axios.post('/api/workbench/writing/feedback', {
      panels: writingPanels.value,
    })
    writingFeedback.value = res.data.data

    try {
      await saveHistory({
        title: `写作训练 · ${writingTheme.value}`,
        input_text: JSON.stringify(writingPanels.value),
        output_data: writingFeedback.value,
        module: 'workbench',
      })
      writingSaved.value = true
    } catch (e) {
      console.error('历史记录保存失败', e)
    }
  } catch (e) {
    console.error('写作辅导获取失败', e)
  } finally {
    generating.value = false
  }
}
</script>
