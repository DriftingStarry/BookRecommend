<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Book } from '../models'
import BookCard from '../components/BookCard.vue'

const books = ref<Book[]>([{
  id: 1,
  title: "The Hunger Games",
  authors: "Suzanne Collins",
  cover: "https://images.gr-assets.com/books/1447303603m/2767052.jpg",
  avgRating: 4.3,
  year: 2008,
  tags: ["Young Adult", "Dystopian", "Science Fiction"],
}])

const loading = ref(true)

onMounted(() => {
  // 模拟加载延迟
  setTimeout(() => {
    loading.value = false
  }, 1000)
})
</script>

<template>
  <div class="home-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>推荐图书</h2>
      <p>基于goodbooks-10k数据集的精选图书推荐</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="3" animated />
      <el-skeleton :rows="3" animated />
      <el-skeleton :rows="3" animated />
    </div>

    <!-- 图书网格 -->
    <div v-else class="books-grid">
      <div
        v-for="book in books"
        :key="book.id"
        class="book-item"
      >
        <BookCard :book="book" />
      </div>
    </div>

    <!-- 加载更多按钮 -->
    <div class="load-more">
      <el-button type="primary" size="large" :loading="loading">
        加载更多图书
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h2 {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.page-header p {
  font-size: 16px;
  color: #606266;
  margin: 0;
}

.loading-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.book-item {
  height: 400px;
}

.load-more {
  text-align: center;
  margin-top: 40px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-view {
    padding: 16px;
  }

  .page-header h2 {
    font-size: 24px;
  }

  .page-header p {
    font-size: 14px;
  }

  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }

  .book-item {
    height: 360px;
  }
}

@media (max-width: 480px) {
  .books-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .book-item {
    height: 340px;
  }
}
</style> 