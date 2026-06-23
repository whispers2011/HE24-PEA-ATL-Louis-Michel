import { createRouter, createWebHistory } from 'vue-router'

import { getToken } from '@/api/client'
import DashboardView from '@/views/DashboardView.vue'
import LoginView from '@/views/LoginView.vue'
import StatsView from '@/views/StatsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/login', name: 'login', component: LoginView },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/links/:code/stats',
      name: 'stats',
      component: StatsView,
      props: true,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to) => {
  const authenticated = getToken() !== null
  if (to.meta.requiresAuth && !authenticated) {
    return { name: 'login' }
  }
  if (to.name === 'login' && authenticated) {
    return { name: 'dashboard' }
  }
})

export default router
