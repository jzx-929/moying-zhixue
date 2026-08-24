import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: '首页 · 墨影智学' },
  },
  {
    path: '/workshop',
    name: 'Workshop',
    component: () => import('../views/Workshop.vue'),
    meta: { title: '墨漫工坊 · 墨影智学' },
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue'),
    meta: { title: '关于 · 墨影智学' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.afterEach((to) => {
  document.title = to.meta.title || '墨影智学'
})

export default router
