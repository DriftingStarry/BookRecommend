<script setup lang="ts">
// 主应用组件 - 包含导航栏和路由视图
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from './stores'
import { Top } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const handleLogin = () => {
  router.push('/login')
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const isLoggedIn = computed(() => userStore.isLoggedIn)
const userId = computed(() => userStore.userId)
const isLoginPage = computed(() => route.path === '/login')

// 回到顶部按钮逻辑
const showBackTop = ref(false)
const handleScroll = () => {
  showBackTop.value = window.scrollY > 300
}
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div id="app">
    <el-container style="min-height: 100vh;">
      <!-- 头部 -->
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo">
            <el-icon :size="32" color="#409EFF">
              <Reading />
            </el-icon>
            <h1>图书推荐系统</h1>
          </div>
          <div class="search-box">
            <el-input
              placeholder="搜索图书..."
              prefix-icon="Search"
              clearable
              class="search-input"
            />
          </div>
          <div class="user-actions">
            <template v-if="!isLoggedIn && !isLoginPage">
              <el-button type="primary" @click="handleLogin">登录</el-button>
            </template>
            <template v-else-if="isLoggedIn">
              <span class="welcome">欢迎 {{ userId }}</span>
              <el-button type="info" @click="handleLogout">登出</el-button>
            </template>
          </div>
        </div>
      </el-header>

      <!-- 主要内容 -->
      <el-main class="app-main">
        <router-view />
      </el-main>

      <!-- 底部 -->
      <el-footer class="app-footer">
        <p>&copy; 2024 图书推荐系统 - 基于 goodbooks-10k 数据集</p>
      </el-footer>
    </el-container>

    <!-- 回到顶部按钮 -->
    <transition name="fade">
      <el-button
        v-if="showBackTop"
        class="back-top-btn"
        circle
        type="primary"
        @click="scrollToTop"
        size="large"
      >
        <el-icon><Top /></el-icon>
      </el-button>
    </transition>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.app-header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
  height: auto;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.search-box {
  flex: 1;
  max-width: 400px;
}

.search-input {
  width: 100%;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.welcome {
  color: #409EFF;
  font-size: 15px;
  margin-right: 8px;
}

.app-main {
  padding: 0;
  background-color: #f5f7fa;
}

.app-footer {
  background-color: #fff;
  border-top: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
}

.app-footer p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.back-top-btn {
  position: fixed;
  right: 32px;
  bottom: 48px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(64,158,255,0.15);
  transition: opacity 0.3s;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    padding: 12px 16px;
  }

  .logo h1 {
    font-size: 20px;
  }

  .search-box {
    max-width: 100%;
  }
}
</style>
