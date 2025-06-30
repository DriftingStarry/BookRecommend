<script setup lang="ts">
// 主应用组件 - 包含导航栏和路由视图
</script>

<template>
  <div id="app">
    <el-container>
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
