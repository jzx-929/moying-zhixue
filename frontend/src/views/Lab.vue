<template>
  <div>
    <div class="text-center mb-8">
      <h1 class="font-heading text-4xl font-bold text-ink tracking-widest mb-2">数字人文实验室</h1>
      <p class="text-ink-muted">图像叙事量化研究 · 数据可视化分析</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
      <div v-for="stat in stats" :key="stat.label" class="card p-6">
        <div class="text-3xl font-heading text-accent mb-1">{{ stat.value }}</div>
        <div class="text-sm text-ink-light">{{ stat.label }}</div>
      </div>
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

    <!-- 构图分析 -->
    <div v-if="activeTab === 'composition'" class="space-y-6">
      <div class="card p-6">
        <h2 class="font-heading text-xl text-ink mb-4">画面构图量化分析</h2>
        <p class="text-sm text-ink-light mb-6">批量导入蔡志忠漫画，AI 识别画面元素，统计构图规律</p>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h3 class="font-heading text-base text-ink mb-3">主体位置分布</h3>
            <div class="bg-paper2 border border-border rounded-lg p-4">
              <div class="relative w-full aspect-square max-w-xs mx-auto">
                <div class="absolute inset-0 border-2 border-border rounded-lg">
                  <div class="absolute inset-0 grid grid-cols-3 grid-rows-3">
                    <div v-for="(cell, i) in gridCells" :key="i"
                      class="border border-border/50 flex items-center justify-center text-xs"
                      :style="{ backgroundColor: `rgba(139, 69, 19, ${cell.count / 50})` }">
                      <span :class="cell.count > 25 ? 'text-white' : 'text-ink-muted'">{{ cell.count }}%</span>
                    </div>
                  </div>
                </div>
              </div>
              <p class="text-xs text-ink-muted text-center mt-3">九宫格主体位置热力图（n=200 幅）</p>
            </div>
          </div>

          <div>
            <h3 class="font-heading text-base text-ink mb-3">留白比例分布</h3>
            <div class="bg-paper2 border border-border rounded-lg p-4">
              <div class="space-y-3">
                <div v-for="(range, i) in whitespaceRanges" :key="i">
                  <div class="flex justify-between text-xs mb-1">
                    <span class="text-ink">{{ range.label }}</span>
                    <span class="text-ink-muted">{{ range.count }} 幅</span>
                  </div>
                  <div class="h-3 bg-border rounded-full overflow-hidden">
                    <div
                      class="h-full bg-accent rounded-full transition-all"
                      :style="{ width: `${range.percent}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h3 class="font-heading text-base text-ink mb-3">线条数量统计</h3>
            <div class="bg-paper2 border border-border rounded-lg p-4">
              <div class="flex items-end justify-around h-48 gap-2">
                <div v-for="bar in lineCountBars" :key="bar.label" class="flex flex-col items-center flex-1">
                  <div
                    class="w-full bg-olive rounded-t transition-all"
                    :style="{ height: `${bar.height}%` }"
                  ></div>
                  <span class="text-xs text-ink-muted mt-2">{{ bar.label }}</span>
                </div>
              </div>
              <p class="text-xs text-ink-muted text-center mt-3">平均线条数：4.2 条 / 幅</p>
            </div>
          </div>

          <div>
            <h3 class="font-heading text-base text-ink mb-3">墨色浓淡分布</h3>
            <div class="bg-paper2 border border-border rounded-lg p-4">
              <div class="space-y-4">
                <div v-for="ink in inkDensity" :key="ink.label">
                  <div class="flex justify-between text-sm mb-1">
                    <span class="text-ink">{{ ink.label }}</span>
                    <span class="text-ink-muted">{{ ink.percent }}%</span>
                  </div>
                  <div class="h-4 bg-border rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full"
                      :class="ink.label === '浓墨' ? 'bg-ink' : ink.label === '中墨' ? 'bg-ink-light' : 'bg-ink-muted'"
                      :style="{ width: `${ink.percent}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card p-6">
        <h3 class="font-heading text-lg text-ink mb-4">📊 研究发现摘要</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 bg-paper2 border border-border rounded-lg">
            <div class="text-accent font-heading text-lg mb-1">构图规律</div>
            <p class="text-sm text-ink-light">蔡志忠漫画主体多位于右下或居中，左上大面积留白，形成"虚-实"对比，符合中国传统绘画"计白当黑"的美学原则。</p>
          </div>
          <div class="p-4 bg-paper2 border border-border rounded-lg">
            <div class="text-olive font-heading text-lg mb-1">极简特征</div>
            <p class="text-sm text-ink-light">单幅平均仅4.2条主线，最少仅2条，最高不超过8条。以最简练的线条传递最丰富的意蕴，是"以简驭繁"的典范。</p>
          </div>
          <div class="p-4 bg-paper2 border border-border rounded-lg">
            <div class="text-gold font-heading text-lg mb-1">墨色层次</div>
            <p class="text-sm text-ink-light">淡墨占比约50%，中墨35%，浓墨15%。整体色调淡雅，关键处用浓墨点睛，层次分明，节奏感强。</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 文本分析 -->
    <div v-if="activeTab === 'text'" class="space-y-6">
      <div class="card p-6">
        <h2 class="font-heading text-xl text-ink mb-4">文本题材分析</h2>
        <p class="text-sm text-ink-light mb-6">基于文本库对国学典籍进行主题分类与词频分析</p>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h3 class="font-heading text-base text-ink mb-3">学派分布</h3>
            <div class="bg-paper2 border border-border rounded-lg p-4">
              <div class="flex items-center justify-center gap-8">
                <div class="relative w-40 h-40">
                  <svg viewBox="0 0 100 100" class="w-full h-full -rotate-90">
                    <circle cx="50" cy="50" r="40" fill="none" stroke="#e8e0d2" stroke-width="12" />
                    <circle cx="50" cy="50" r="40" fill="none" stroke="#8b4513" stroke-width="12"
                      stroke-dasharray="251.2" stroke-dashoffset="100.5" stroke-linecap="round" />
                    <circle cx="50" cy="50" r="40" fill="none" stroke="#556b2f" stroke-width="12"
                      stroke-dasharray="251.2" stroke-dashoffset="25.1" stroke-linecap="round" />
                    <circle cx="50" cy="50" r="40" fill="none" stroke="#b8860b" stroke-width="12"
                      stroke-dasharray="251.2" stroke-dashoffset="251.2" stroke-linecap="round" />
                  </svg>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <span class="font-heading text-2xl text-ink">1729</span>
                  </div>
                </div>
                <div class="space-y-2">
                  <div class="flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full bg-accent"></span>
                    <span class="text-sm text-ink">儒家 60%</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full bg-olive"></span>
                    <span class="text-sm text-ink">道家 30%</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full bg-gold"></span>
                    <span class="text-sm text-ink">史家 10%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h3 class="font-heading text-base text-ink mb-3">高频词汇 TOP 10</h3>
            <div class="bg-paper2 border border-border rounded-lg p-4">
              <div class="space-y-2">
                <div v-for="(word, i) in topWords" :key="i" class="flex items-center gap-3">
                  <span class="w-6 text-center text-xs font-bold" :class="i < 3 ? 'text-accent' : 'text-ink-muted'">{{ i + 1 }}</span>
                  <span class="font-heading text-ink w-12">{{ word.word }}</span>
                  <div class="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all"
                      :class="i < 3 ? 'bg-accent' : 'bg-olive'"
                      :style="{ width: `${word.percent}%` }"
                    ></div>
                  </div>
                  <span class="text-xs text-ink-muted w-12 text-right">{{ word.count }} 次</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card p-6">
        <h3 class="font-heading text-lg text-ink mb-4">情感倾向分析</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 bg-paper2 border border-border rounded-lg text-center">
            <div class="text-4xl mb-2">😊</div>
            <div class="font-heading text-2xl text-olive">45%</div>
            <div class="text-sm text-ink-light">积极正面</div>
            <p class="text-xs text-ink-muted mt-2">劝学、乐道、仁爱等</p>
          </div>
          <div class="p-4 bg-paper2 border border-border rounded-lg text-center">
            <div class="text-4xl mb-2">😐</div>
            <div class="font-heading text-2xl text-ink-light">40%</div>
            <div class="text-sm text-ink-light">中性叙述</div>
            <p class="text-xs text-ink-muted mt-2">记事、论述、说明等</p>
          </div>
          <div class="p-4 bg-paper2 border border-border rounded-lg text-center">
            <div class="text-4xl mb-2">😔</div>
            <div class="font-heading text-2xl text-shu">15%</div>
            <div class="text-sm text-ink-light">消极警示</div>
            <p class="text-xs text-ink-muted mt-2">劝诫、批评、忧患等</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 数据集 -->
    <div v-if="activeTab === 'dataset'" class="space-y-6">
      <div class="card p-6">
        <h2 class="font-heading text-xl text-ink mb-4">数据集概览</h2>
        <p class="text-sm text-ink-light mb-6">墨影智学自建双 RAG 知识库</p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-paper2 border border-border rounded-lg p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center text-2xl">📚</div>
              <div>
                <h3 class="font-heading text-lg text-ink">国学文本库</h3>
                <p class="text-xs text-ink-muted">ChromaDB · 向量检索</p>
              </div>
            </div>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-ink-light">典籍数量</span>
                <span class="text-ink">5 部</span>
              </div>
              <div class="flex justify-between">
                <span class="text-ink-light">文本段落</span>
                <span class="text-ink">1,729 条</span>
              </div>
              <div class="flex justify-between">
                <span class="text-ink-light">总字数</span>
                <span class="text-ink">约 12 万字</span>
              </div>
              <div class="flex justify-between">
                <span class="text-ink-light">嵌入模型</span>
                <span class="text-ink">bge-small-zh-v1.5</span>
              </div>
              <div class="flex justify-between">
                <span class="text-ink-light">向量维度</span>
                <span class="text-ink">512 维</span>
              </div>
            </div>
            <div class="mt-4 pt-4 border-t border-border">
              <div class="text-xs text-ink-muted mb-2">涵盖典籍</div>
              <div class="flex flex-wrap gap-2">
                <span class="px-2 py-1 bg-accent/10 text-accent rounded text-xs">论语</span>
                <span class="px-2 py-1 bg-accent/10 text-accent rounded text-xs">孟子</span>
                <span class="px-2 py-1 bg-olive/10 text-olive rounded text-xs">道德经</span>
                <span class="px-2 py-1 bg-olive/10 text-olive rounded text-xs">庄子</span>
                <span class="px-2 py-1 bg-gold/10 text-gold rounded text-xs">史记</span>
              </div>
            </div>
          </div>

          <div class="bg-paper2 border border-border rounded-lg p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-12 h-12 bg-olive/10 rounded-lg flex items-center justify-center text-2xl">🖼</div>
              <div>
                <h3 class="font-heading text-lg text-ink">国风漫画图库</h3>
                <p class="text-xs text-ink-muted">ChromaDB · 多模态对齐</p>
              </div>
            </div>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-ink-light">漫画图片</span>
                <span class="text-ink">500+ 幅</span>
              </div>
              <div class="flex justify-between">
                <span class="text-ink-light">分镜标注</span>
                <span class="text-ink">300+ 组</span>
              </div>
              <div class="flex justify-between">
                <span class="text-ink-light">图文对</span>
                <span class="text-ink">500+ 对</span>
              </div>
              <div class="flex justify-between">
                <span class="text-ink-light">风格标签</span>
                <span class="text-ink">8 类</span>
              </div>
              <div class="flex justify-between">
                <span class="text-ink-light">构图标注</span>
                <span class="text-ink">九宫格位置</span>
              </div>
            </div>
            <div class="mt-4 pt-4 border-t border-border">
              <div class="text-xs text-ink-muted mb-2">数据状态</div>
              <span class="px-2 py-1 bg-gold/10 text-gold rounded text-xs">⏳ 收集中（Phase 2）</span>
            </div>
          </div>
        </div>
      </div>

      <div class="card p-6">
        <h3 class="font-heading text-lg text-ink mb-4">研究工具链</h3>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="p-4 bg-paper2 border border-border rounded-lg text-center">
            <div class="text-3xl mb-2">🔍</div>
            <div class="font-heading text-sm text-ink mb-1">图像识别</div>
            <p class="text-xs text-ink-light">AI 自动识别画面元素与构图</p>
          </div>
          <div class="p-4 bg-paper2 border border-border rounded-lg text-center">
            <div class="text-3xl mb-2">📊</div>
            <div class="font-heading text-sm text-ink mb-1">统计分析</div>
            <p class="text-xs text-ink-light">多维度量化指标与分布统计</p>
          </div>
          <div class="p-4 bg-paper2 border border-border rounded-lg text-center">
            <div class="text-3xl mb-2">📈</div>
            <div class="font-heading text-sm text-ink mb-1">可视化</div>
            <p class="text-xs text-ink-light">图表直观呈现研究发现</p>
          </div>
          <div class="p-4 bg-paper2 border border-border rounded-lg text-center">
            <div class="text-3xl mb-2">📥</div>
            <div class="font-heading text-sm text-ink mb-1">数据导出</div>
            <p class="text-xs text-ink-light">支持 CSV/JSON 格式导出</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const activeTab = ref('composition')

const tabs = [
  { key: 'composition', icon: '🖼', label: '构图分析', desc: '画面构图、留白、线条、墨色的量化研究' },
  { key: 'text', icon: '📝', label: '文本分析', desc: '国学典籍主题分类、词频、情感倾向分析' },
  { key: 'dataset', icon: '📦', label: '数据集', desc: '双RAG知识库概览与研究工具链' },
]

const stats = ref([
  { value: '...', label: '文本段落' },
  { value: '...', label: '漫画图像' },
  { value: '...', label: '涵盖典籍' },
  { value: '...', label: '分析维度' },
])

const gridCells = ref([])
const whitespaceRanges = ref([])
const lineCountBars = ref([])
const inkDensity = ref([
  { label: '浓墨', percent: 15 },
  { label: '中墨', percent: 35 },
  { label: '淡墨', percent: 50 },
])
const topWords = ref([])
const datasets = ref(null)

onMounted(async () => {
  try {
    const [statsRes, compRes, textRes, dsRes] = await Promise.all([
      axios.get('/api/lab/stats'),
      axios.get('/api/lab/composition'),
      axios.get('/api/lab/text-analysis'),
      axios.get('/api/lab/datasets'),
    ])
    const s = statsRes.data.data
    stats.value = [
      { value: s.text_chunks.toLocaleString(), label: '文本段落' },
      { value: s.images, label: '漫画图像' },
      { value: String(s.classics), label: '涵盖典籍' },
      { value: String(s.dimensions), label: '分析维度' },
    ]
    const c = compRes.data.data
    gridCells.value = c.grid_cells.map(v => ({ count: v }))
    whitespaceRanges.value = c.whitespace_ranges
    lineCountBars.value = c.line_count_bars
    inkDensity.value = c.ink_density
    topWords.value = textRes.data.data.top_words
    datasets.value = dsRes.data.data
  } catch (e) {
    console.error('Lab 数据加载失败', e)
  }
})
</script>
