<template>
  <div class="max-w-3xl mx-auto py-8">
    <h1 class="font-heading text-3xl font-bold text-ink mb-6">关于墨影智学</h1>

    <div class="space-y-4 text-ink-light leading-relaxed">
      <p>
        墨影智学面向人文通识一流学科建设，基于星火大模型研发学科垂类教学智能体，
        深度融合国学典籍文本与蔡志忠水墨漫画视觉范式，
        致力于让沉睡在典籍中的国学智慧以水墨动画的形式重新苏醒。
      </p>
      <p>
        系统构建文本、漫画、动画三态双向转化技术链路，全面覆盖课程教学与科研全流程。
        核心工作流为：古文 → 分镜文案 → 线稿漫画 → 连续水墨动画。
      </p>
      <p>
        赛题编号 XH-202620，发榜单位科大讯飞股份有限公司。
        基于讯飞星火学科大模型平台开发。
      </p>
    </div>

    <div class="mt-8 grid grid-cols-2 gap-4">
      <div class="card p-4">
        <h3 class="font-heading text-base text-ink mb-2">技术栈</h3>
        <ul class="text-sm text-ink-light space-y-1">
          <li>前端：Vue 3 + Tailwind CSS</li>
          <li>后端：FastAPI + ChromaDB</li>
          <li>AI：讯飞星火 + 双 Agent + LoRA</li>
          <li>知识库：双 RAG（文本 + 视觉）</li>
        </ul>
      </div>
      <div class="card p-4">
        <h3 class="font-heading text-base text-ink mb-2">核心理念</h3>
        <ul class="text-sm text-ink-light space-y-1">
          <li>古文入画 — 古文转化为水墨画面</li>
          <li>以画承文 — 画面承载传播文化</li>
          <li>以画研文 — 视觉数据反哺研究</li>
        </ul>
      </div>
    </div>
  </div>
</template>
