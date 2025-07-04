import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/home',
      name: 'home-alias',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/book/:id',
      name: 'book-detail',
      component: () => import('../views/BookDetailView.vue')
    },
    {
      path: '/favor',
      name: 'favor',
      component: () => import('../views/FavorView.vue')
    }
  ]
})

export default router
