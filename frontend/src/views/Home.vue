<template>
  <div class="py-8">
    <!-- Hero Section -->
    <section class="text-center py-12 relative overflow-hidden">
      <div class="absolute inset-0 opacity-5 pointer-events-none">
        <div class="absolute top-10 left-10 text-9xl font-heading text-accent">墨</div>
        <div class="absolute bottom-10 right-10 text-9xl font-heading text-olive">影</div>
      </div>

      <div class="relative z-10">
        <div class="inline-block mb-6">
          <div class="w-24 h-24 bg-gradient-to-br from-accent to-shu text-white rounded-2xl flex items-center justify-center font-heading text-4xl mx-auto shadow-lg">
            墨影
          </div>
        </div>
        <h1 class="font-heading text-5xl md:text-6xl font-bold text-ink tracking-widest mb-4">墨影智学</h1>
        <p class="text-xl text-ink-light mb-3">文本 · 漫画 · 动画 跨媒介教学智能体</p>
        <p class="text-ink-muted max-w-2xl mx-auto leading-relaxed mb-8">
          古文入画，以画承文，以画研文。基于星火大模型研发学科垂类教学智能体，
          将蔡志忠国学漫画范式固化为 AI 视觉生成约束，打通教学—创作—科研闭环。
        </p>

        <div class="flex flex-wrap justify-center gap-4">
          <router-link to="/workshop" class="btn-primary px-8 py-3">
            立即体验
          </router-link>
          <router-link to="/about" class="btn-ghost px-8 py-3">
            了解更多
          </router-link>
        </div>
      </div>
    </section>

    <!-- Four Modules -->
    <section class="py-12">
      <div class="text-center mb-10">
        <h2 class="font-heading text-3xl font-bold text-ink tracking-wider mb-3">四大功能板块</h2>
        <p class="text-ink-light">覆盖创作、教学、科研全场景</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
        <router-link
          v-for="panel in panels"
          :key="panel.path"
          :to="panel.path"
          class="card p-8 text-left transition-all hover:shadow-lg hover:-translate-y-1 group"
        >
          <div class="flex items-start gap-4">
            <div class="w-14 h-14 rounded-xl flex items-center justify-center text-2xl flex-shrink-0"
              :class="panel.bgClass">
              {{ panel.icon }}
            </div>
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <span class="text-accent font-heading text-sm">{{ panel.num }}</span>
                <h3 class="font-heading text-xl text-ink">{{ panel.title }}</h3>
              </div>
              <p class="text-sm text-ink-light leading-relaxed mb-3">{{ panel.desc }}</p>
              <span class="text-sm text-accent inline-flex items-center gap-1 group-hover:gap-2 transition-all">
                进入体验 →
              </span>
            </div>
          </div>
        </router-link>
      </div>
    </section>

    <!-- Features -->
    <section class="py-12 bg-paper2/50 -mx-4 px-4">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-10">
          <h2 class="font-heading text-3xl font-bold text-ink tracking-wider mb-3">三大核心创新</h2>
          <p class="text-ink-light">独家技术壁垒与创新亮点</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="card p-6">
            <div class="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center text-2xl mb-4">🎭</div>
            <h3 class="font-heading text-lg text-ink mb-2">独家双叙事赛道</h3>
            <p class="text-sm text-ink-light leading-relaxed">
              赛道A白话小说影视改编、赛道B国学典籍水墨动画，文漫互转双向闭环。
            </p>
          </div>
          <div class="card p-6">
            <div class="w-12 h-12 bg-olive/10 rounded-lg flex items-center justify-center text-2xl mb-4">📚</div>
            <h3 class="font-heading text-lg text-ink mb-2">教学场景专属模式</h3>
            <p class="text-sm text-ink-light leading-relaxed">
              助教课件一键生成、助学漫画式写作训练、助研图像叙事量化研究工具。
            </p>
          </div>
          <div class="card p-6">
            <div class="w-12 h-12 bg-gold/10 rounded-lg flex items-center justify-center text-2xl mb-4">🧠</div>
            <h3 class="font-heading text-lg text-ink mb-2">垂类模型技术壁垒</h3>
            <p class="text-sm text-ink-light leading-relaxed">
              自建双数据集、双智能体分工协作、工作流流水线固化，形成独家技术优势。
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Tech Stack -->
    <section class="py-12">
      <div class="max-w-5xl mx-auto text-center">
        <h2 class="font-heading text-3xl font-bold text-ink tracking-wider mb-3">技术架构</h2>
        <p class="text-ink-light mb-10">五层架构，全栈自研</p>

        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div v-for="layer in techLayers" :key="layer.name" class="card p-4">
            <div class="text-2xl mb-2">{{ layer.icon }}</div>
            <div class="font-heading text-sm text-ink mb-1">{{ layer.name }}</div>
            <div class="text-xs text-ink-muted">{{ layer.tech }}</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const panels = [
  {
    num: '01',
    title: '墨漫工坊',
    icon: '🎨',
    bgClass: 'bg-accent/10',
    desc: '国学典籍水墨动画核心赛道，古文↔蔡志忠漫画动画双向通道，完整创作流水线。',
    path: '/workshop',
  },
  {
    num: '02',
    title: '教学工作台',
    icon: '📚',
    bgClass: 'bg-olive/10',
    desc: '助教课件一键生成、助学漫画式写作训练，全面服务教学场景，提升教学效率。',
    path: '/workbench',
  },
  {
    num: '03',
    title: '文影创作坊',
    icon: '🎬',
    bgClass: 'bg-gold/10',
    desc: '白话小说影视改编赛道，小说→剧本→多风格短片，支持跨版本对照与配音。',
    path: '/studio',
  },
  {
    num: '04',
    title: '数字人文实验室',
    icon: '🔬',
    bgClass: 'bg-shu/10',
    desc: '图像叙事量化研究、数据可视化分析、双RAG数据集，服务科研场景。',
    path: '/lab',
  },
]

const techLayers = [
  { icon: '🖥', name: '前端层', tech: 'Vue 3 + Tailwind' },
  { icon: '⚡', name: '后端层', tech: 'FastAPI + Celery' },
  { icon: '🤖', name: 'AI模型层', tech: '星火 + LoRA + Agent' },
  { icon: '📦', name: '知识库层', tech: 'Chroma + 双RAG' },
  { icon: '💾', name: '存储层', tech: 'MinIO + PostgreSQL' },
]
</script>
