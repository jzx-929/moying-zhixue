<template>
  <div class="text-center py-8">
    <div class="inline-block mb-6">
      <div class="w-20 h-20 bg-shu text-white rounded-lg flex items-center justify-center font-heading text-3xl mx-auto">墨影</div>
    </div>
    <h1 class="font-heading text-5xl font-bold text-ink tracking-widest mb-3">墨影智学</h1>
    <p class="text-xl text-ink-light mb-2">文本-漫画-动画跨媒介教学智能体</p>
    <p class="text-ink-muted max-w-2xl mx-auto leading-relaxed">
      古文入画，以画承文，以画研文。基于星火大模型研发学科垂类教学智能体，
      将蔡志忠国学漫画范式固化为 AI 视觉生成约束。
    </p>

    <div class="flex justify-center gap-4 mt-8">
      <router-link to="/workshop" class="btn-primary">进入墨漫工坊</router-link>
      <router-link to="/about" class="btn-ghost">了解项目</router-link>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 max-w-5xl mx-auto mt-16">
      <div v-for="panel in panels" :key="panel.num" class="card p-6 text-left">
        <div class="text-2xl font-heading text-accent mb-2">{{ panel.num }}</div>
        <h3 class="font-heading text-lg text-ink mb-2">{{ panel.title }}</h3>
        <p class="text-sm text-ink-light leading-relaxed">{{ panel.desc }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const panels = [
  { num: '01', title: '文影创作坊', desc: '白话小说影视改编赛道，文本到剧本到影视的完整创作流。' },
  { num: '02', title: '墨漫工坊（核心）', desc: '国学典籍水墨动画赛道，古文到分镜到水墨动画的核心管线。' },
  { num: '03', title: '教学工作台', desc: '助教课件一键生成、助学漫画式写作训练，服务教学场景。' },
  { num: '04', title: '数字人文实验室', desc: '图像叙事量化研究、数据可视化分析，服务科研场景。' },
]
</script>
