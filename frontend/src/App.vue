<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BookCard from './components/BookCard.vue'

interface Book {
  id: number
  title: string
  author: string
  cover?: string
  rating?: number
  year?: number
  genres?: string[]
}

// 模拟图书数据（基于goodbooks-10k数据集的示例）
const books = ref<Book[]>([
  {
    id: 1,
    title: "The Hunger Games",
    author: "Suzanne Collins",
    rating: 4.3,
    year: 2008,
    genres: ["Young Adult", "Dystopian", "Science Fiction"]
  },
  {
    id: 2,
    title: "Harry Potter and the Philosopher's Stone",
    author: "J.K. Rowling",
    rating: 4.4,
    year: 1997,
    genres: ["Fantasy", "Young Adult", "Adventure"]
  },
  {
    id: 3,
    title: "To Kill a Mockingbird",
    author: "Harper Lee",
    rating: 4.2,
    year: 1960,
    genres: ["Classic", "Fiction", "Historical"]
  },
  {
    id: 4,
    title: "Pride and Prejudice",
    author: "Jane Austen",
    rating: 4.1,
    year: 1813,
    genres: ["Classic", "Romance", "Historical"]
  },
  {
    id: 5,
    title: "The Great Gatsby",
    author: "F. Scott Fitzgerald",
    rating: 3.9,
    year: 1925,
    genres: ["Classic", "Fiction", "Historical"]
  },
  {
    id: 6,
    title: "1984",
    author: "George Orwell",
    rating: 4.1,
    year: 1949,
    genres: ["Dystopian", "Science Fiction", "Political"]
  },
  {
    id: 7,
    title: "The Hobbit",
    author: "J.R.R. Tolkien",
    rating: 4.2,
    year: 1937,
    genres: ["Fantasy", "Adventure", "Fiction"]
  },
  {
    id: 8,
    title: "The Catcher in the Rye",
    author: "J.D. Salinger",
    rating: 3.8,
    year: 1951,
    genres: ["Classic", "Fiction", "Coming of Age"]
  },
  {
    id: 9,
    title: "Lord of the Flies",
    author: "William Golding",
    rating: 3.7,
    year: 1954,
    genres: ["Classic", "Fiction", "Allegory"]
  },
  {
    id: 10,
    title: "Animal Farm",
    author: "George Orwell",
    rating: 3.9,
    year: 1945,
    genres: ["Classic", "Political", "Allegory"]
  },
  {
    id: 11,
    title: "The Alchemist",
    author: "Paulo Coelho",
    rating: 3.9,
    year: 1988,
    genres: ["Fiction", "Adventure", "Philosophy"]
  },
  {
    id: 12,
    title: "The Book Thief",
    author: "Markus Zusak",
    rating: 4.3,
    year: 2005,
    genres: ["Historical Fiction", "Young Adult", "War"]
  }
])

const loading = ref(true)

onMounted(() => {
  // 模拟加载延迟
  setTimeout(() => {
    loading.value = false
  }, 1000)
})
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
        <div class="container">
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

.container {
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

  .container {
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
