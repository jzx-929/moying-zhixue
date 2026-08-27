<template>
  <div class="max-w-4xl mx-auto py-8">
    <!-- Hero -->
    <div class="text-center mb-12">
      <div class="w-20 h-20 bg-gradient-to-br from-accent to-shu text-white rounded-2xl flex items-center justify-center font-heading text-3xl mx-auto mb-4 shadow-lg">
        墨影
      </div>
      <h1 class="font-heading text-4xl font-bold text-ink tracking-widest mb-3">墨影智学</h1>
      <p class="text-ink-light text-lg mb-2">文本 · 漫画 · 动画 跨媒介教学智能体</p>
      <p class="text-ink-muted text-sm">赛题编号 XH-202620 · 发榜单位：科大讯飞股份有限公司</p>
    </div>

    <!-- 项目简介 -->
    <section class="mb-10">
      <h2 class="font-heading text-2xl text-ink mb-4 border-b-2 border-accent pb-2">项目简介</h2>
      <div class="space-y-4 text-ink-light leading-relaxed">
        <p>
          墨影智学面向人文通识一流学科建设，基于星火大模型研发学科垂类教学智能体，
          深度融合国学典籍文本与蔡志忠水墨漫画视觉范式，
          致力于让沉睡在典籍中的国学智慧以水墨动画的形式重新苏醒。
        </p>
        <p>
          系统构建文本、漫画、动画三态双向转化技术链路，全面覆盖课程教学与科研全流程。
          核心工作流为：<strong class="text-ink">古文 → 分镜文案 → 线稿漫画 → 连续水墨动画</strong>。
        </p>
      </div>
    </section>

    <!-- 三大核心理念 -->
    <section class="mb-10">
      <h2 class="font-heading text-2xl text-ink mb-4 border-b-2 border-accent pb-2">核心理念</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="card p-6 text-center">
          <div class="text-3xl mb-3">📜</div>
          <h3 class="font-heading text-lg text-ink mb-2">古文入画</h3>
          <p class="text-sm text-ink-light">将古文原文转化为水墨画面，用视觉语言诠释经典文本</p>
        </div>
        <div class="card p-6 text-center">
          <div class="text-3xl mb-3">🖌</div>
          <h3 class="font-heading text-lg text-ink mb-2">以画承文</h3>
          <p class="text-sm text-ink-light">以画面承载文化传播，让经典以新的形态触达当代受众</p>
        </div>
        <div class="card p-6 text-center">
          <div class="text-3xl mb-3">🔬</div>
          <h3 class="font-heading text-lg text-ink mb-2">以画研文</h3>
          <p class="text-sm text-ink-light">视觉数据反哺研究，用量化分析挖掘文本与画面的深层关联</p>
        </div>
      </div>
    </section>

    <!-- 技术架构 -->
    <section class="mb-10">
      <h2 class="font-heading text-2xl text-ink mb-4 border-b-2 border-accent pb-2">技术架构</h2>
      <div class="space-y-3">
        <div v-for="layer in techLayers" :key="layer.name" class="card p-4">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center text-2xl flex-shrink-0"
              :class="layer.bgClass">
              {{ layer.icon }}
            </div>
            <div class="flex-1">
              <div class="flex items-center gap-3">
                <h3 class="font-heading text-base text-ink">{{ layer.name }}</h3>
                <span class="text-xs text-ink-muted">{{ layer.tech }}</span>
              </div>
              <p class="text-sm text-ink-light mt-1">{{ layer.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 四大功能板块 -->
    <section class="mb-10">
      <h2 class="font-heading text-2xl text-ink mb-4 border-b-2 border-accent pb-2">四大功能板块</h2>
      <div class="space-y-3">
        <div v-for="(m, i) in modules" :key="m.title" class="card p-4 flex items-start gap-4">
          <span class="text-accent font-heading text-lg flex-shrink-0">{{ String(i+1).padStart(2, '0') }}</span>
          <div class="flex-1">
            <div class="flex items-center gap-2">
              <span class="text-xl">{{ m.icon }}</span>
              <h3 class="font-heading text-base text-ink">{{ m.title }}</h3>
            </div>
            <p class="text-sm text-ink-light mt-1">{{ m.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 双 Agent 架构 -->
    <section class="mb-10">
      <h2 class="font-heading text-2xl text-ink mb-4 border-b-2 border-accent pb-2">双 Agent 架构</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="card p-6 border-t-4 border-t-accent">
          <div class="text-2xl mb-2">📝</div>
          <h3 class="font-heading text-lg text-ink mb-2">墨影文改 Agent</h3>
          <p class="text-sm text-ink-light mb-3">古文解析 → 白话翻译 → 剧本拆分 → 3-5格分镜文案</p>
          <div class="text-xs text-ink-muted">
            <div>挂载知识库：国学文本库（1729条）</div>
            <div>输出格式：JSON（source + translation + storyboard）</div>
          </div>
        </div>
        <div class="card p-6 border-t-4 border-t-olive">
          <div class="text-2xl mb-2">🖌</div>
          <h3 class="font-heading text-lg text-ink mb-2">墨影画风 Agent</h3>
          <p class="text-sm text-ink-light mb-3">分镜文案 → 蔡志忠风格水墨构图方案</p>
          <div class="text-xs text-ink-muted">
            <div>范式五原则：线条≤5、留白≥40%、纯水墨、无五官、空灵</div>
            <div>输出格式：JSON（composition + ink_density + whitespace）</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 项目路线图 -->
    <section class="mb-10">
      <h2 class="font-heading text-2xl text-ink mb-4 border-b-2 border-accent pb-2">项目路线图</h2>
      <div class="space-y-3">
        <div v-for="phase in roadmap" :key="phase.phase" class="card p-4">
          <div class="flex items-center gap-3 mb-2">
            <span
              class="px-3 py-1 rounded-full text-xs font-heading"
              :class="phase.status === 'done' ? 'bg-olive/20 text-olive' : phase.status === 'doing' ? 'bg-accent/20 text-accent' : 'bg-gold/10 text-gold'"
            >
              {{ phase.status === 'done' ? '✓ 已完成' : phase.status === 'doing' ? '进行中' : '待启动' }}
            </span>
            <h3 class="font-heading text-base text-ink">{{ phase.phase }}</h3>
          </div>
          <p class="text-sm text-ink-light">{{ phase.desc }}</p>
        </div>
      </div>
    </section>

    <!-- 团队信息 -->
    <section class="mb-10">
      <h2 class="font-heading text-2xl text-ink mb-4 border-b-2 border-accent pb-2">团队信息</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="card p-6">
          <h3 class="font-heading text-base text-ink mb-3">团队规模</h3>
          <div class="space-y-2 text-sm text-ink-light">
            <div class="flex justify-between">
              <span>总人数</span>
              <span class="text-ink">10 人</span>
            </div>
            <div class="flex justify-between">
              <span>新成员</span>
              <span class="text-ink">3 人</span>
            </div>
          </div>
        </div>
        <div class="card p-6">
          <h3 class="font-heading text-base text-ink mb-3">分工架构</h3>
          <div class="space-y-2 text-sm text-ink-light">
            <div class="flex justify-between">
              <span>项目管理</span>
              <span class="text-ink">1 人</span>
            </div>
            <div class="flex justify-between">
              <span>AI 模型组</span>
              <span class="text-ink">2 人</span>
            </div>
            <div class="flex justify-between">
              <span>后端开发</span>
              <span class="text-ink">2 人</span>
            </div>
            <div class="flex justify-between">
              <span>前端开发</span>
              <span class="text-ink">2 人</span>
            </div>
            <div class="flex justify-between">
              <span>内容数据组</span>
              <span class="text-ink">3 人</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <div class="text-center text-ink-muted text-sm border-t border-border pt-6">
      <p>墨影智学 · 2026 学科垂类大模型与创新应用开发赛</p>
      <p class="mt-1">基于讯飞星火大模型平台开发 · 赛题编号 XH-202620</p>
    </div>
  </div>
</template>

<script setup>
const techLayers = [
  { name: '前端层', icon: '🖥', tech: 'Vue 3 + Vite + Tailwind CSS', desc: '水墨国风设计系统，响应式布局，组件化开发', bgClass: 'bg-accent/10' },
  { name: '后端层', icon: '⚡', tech: 'FastAPI + Uvicorn', desc: '异步 API 框架，自动文档生成，中间件支持', bgClass: 'bg-olive/10' },
  { name: 'AI 模型层', icon: '🤖', tech: '讯飞星火 + 双 Agent + LoRA', desc: '文改 Agent + 画风 Agent，工作流流水线固化', bgClass: 'bg-gold/10' },
  { name: '知识库层', icon: '📦', tech: 'ChromaDB + 双 RAG', desc: '文本向量库（1729条）+ 视觉图库（500+），bge-small-zh-v1.5 嵌入', bgClass: 'bg-shu/10' },
  { name: '存储层', icon: '💾', tech: 'SQLite + 文件系统', desc: 'ChromaDB 持久化存储，图片素材管理', bgClass: 'bg-accent/10' },
]

const modules = [
  { icon: '🎨', title: '墨漫工坊', desc: '国学典籍水墨动画核心赛道，古文↔蔡志忠漫画动画双向通道' },
  { icon: '📚', title: '教学工作台', desc: '助教课件一键生成、助学漫画式写作训练' },
  { icon: '🎬', title: '文影创作坊', desc: '白话小说影视改编，小说→剧本→多风格短片+配音' },
  { icon: '🔬', title: '数字人文实验室', desc: '图像叙事量化研究、数据可视化分析、双RAG数据集' },
]

const roadmap = [
  { phase: 'Phase 1：MVP 核心链路', status: 'done', desc: '后端脚手架 + RAG 检索 + 前端工坊页面 + 双 Agent Mock + 前后端联调验证通过' },
  { phase: 'Phase 2：四大板块全页面', status: 'done', desc: '教学工作台 + 文影创作坊 + 数字人文实验室 + 首页视觉增强 + 后端 API 全量接口' },
  { phase: 'Phase 3：真实 Agent 接入', status: 'doing', desc: '星火 API 配置 → 真实 Agent 调用 → 端到端联调 → 性能优化' },
  { phase: 'Phase 4：提交材料准备', status: 'todo', desc: '演示视频录制、技术文档整理、源码打包、最终验收' },
]
</script>
