import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/sounds',
      name: 'sounds',
      component: () => import('@/views/SoundsView.vue'),
    },
    {
      path: '/plans',
      name: 'plans',
      component: () => import('@/views/PlansView.vue'),
    },
    {
      path: '/analyze',
      name: 'analyze',
      component: () => import('@/views/AnalyzeView.vue'),
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
