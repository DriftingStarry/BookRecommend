<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores'
import { useBookStore } from '../stores'

const userStore = useUserStore()
const bookStore = useBookStore()
const router = useRouter()
const userId = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  const idNum = Number(userId.value)
  const result = await userStore.login(idNum)
  loading.value = false
  if (result) {
    await bookStore.getFavorBooks(userStore.userId!)
    router.back()
  } else {
    error.value = userStore.error || '登录失败，请输入有效ID'
  }
}

const handleBackHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="login-view">
    <el-card class="login-card">
      <h2>用户登录</h2>
      <el-form @submit.prevent="handleLogin">
        <el-form-item label="用户ID">
          <el-input v-model="userId" placeholder="请输入用户ID" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" style="width:100%">登录</el-button>
        </el-form-item>
        <el-form-item v-if="error">
          <el-alert :title="error" type="error" show-icon />
        </el-form-item>
      </el-form>
      <div class="back-home">
        <el-button type="info" link @click="handleBackHome" style="width:100%">返回主页</el-button>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.login-view {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
}
.login-card {
  width: 350px;
  padding: 32px 24px 24px 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  border-radius: 8px;
  background: #fff;
}
h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #303133;
}
.back-home {
  text-align: center;
  margin-top: 12px;
}
</style> 