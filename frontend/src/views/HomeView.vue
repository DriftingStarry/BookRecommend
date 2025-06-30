<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Book } from '../models'
import BookCard from '../components/BookCard.vue'

// 推荐图书数据
const recommendedBooks = ref<Book[]>([
  {
    id: 1,
    title: "The Hunger Games",
    authors: "Suzanne Collins",
    cover: "https://images.gr-assets.com/books/1447303603m/2767052.jpg",
    avgRating: 4.3,
    year: 2008,
    tags: ["Young Adult", "Dystopian", "Science Fiction"],
  },
  {
    id: 2,
    title: "Harry Potter and the Philosopher's Stone",
    authors: "J.K. Rowling",
    cover: "https://images.gr-assets.com/books/1474154022m/3.jpg",
    avgRating: 4.4,
    year: 1997,
    tags: ["Fantasy", "Young Adult", "Adventure"],
  },
  {
    id: 3,
    title: "To Kill a Mockingbird",
    authors: "Harper Lee",
    cover: "https://images.gr-assets.com/books/1553383690m/2657.jpg",
    avgRating: 4.2,
    year: 1960,
    tags: ["Classic", "Fiction", "Historical"],
  },
  {
    id: 4,
    title: "The Great Gatsby",
    authors: "F. Scott Fitzgerald",
    cover: "https://images.gr-assets.com/books/1490528560m/4671.jpg",
    avgRating: 3.9,
    year: 1925,
    tags: ["Classic", "Fiction", "Historical"],
  }
])

// 图书库数据
const libraryBooks = ref<Book[]>([
  {
    id: 5,
    title: "1984",
    authors: "George Orwell",
    cover: "https://images.gr-assets.com/books/1532714506m/40961427.jpg",
    avgRating: 4.1,
    year: 1949,
    tags: ["Dystopian", "Science Fiction", "Political"],
  },
  {
    id: 6,
    title: "The Hobbit",
    authors: "J.R.R. Tolkien",
    cover: "https://images.gr-assets.com/books/1372847500m/5907.jpg",
    avgRating: 4.2,
    year: 1937,
    tags: ["Fantasy", "Adventure", "Fiction"],
  },
  {
    id: 7,
    title: "Pride and Prejudice",
    authors: "Jane Austen",
    cover: "https://images.gr-assets.com/books/1320399351m/1885.jpg",
    avgRating: 4.1,
    year: 1813,
    tags: ["Classic", "Romance", "Historical"],
  },
  {
    id: 8,
    title: "The Catcher in the Rye",
    authors: "J.D. Salinger",
    cover: "https://images.gr-assets.com/books/1398034300m/5107.jpg",
    avgRating: 3.8,
    year: 1951,
    tags: ["Classic", "Fiction", "Coming of Age"],
  },
  {
    id: 9,
    title: "Lord of the Flies",
    authors: "William Golding",
    cover: "https://images.gr-assets.com/books/1327949360m/7624.jpg",
    avgRating: 3.7,
    year: 1954,
    tags: ["Classic", "Fiction", "Allegory"],
  },
  {
    id: 10,
    title: "Animal Farm",
    authors: "George Orwell",
    cover: "https://images.gr-assets.com/books/1424037542m/7613.jpg",
    avgRating: 3.9,
    year: 1945,
    tags: ["Classic", "Political", "Allegory"],
  },
  {
    id: 11,
    title: "The Alchemist",
    authors: "Paulo Coelho",
    cover: "https://images.gr-assets.com/books/1483412266m/865.jpg",
    avgRating: 3.9,
    year: 1988,
    tags: ["Fiction", "Adventure", "Philosophy"],
  },
  {
    id: 12,
    title: "The Book Thief",
    authors: "Markus Zusak",
    cover: "https://images.gr-assets.com/books/1327942880m/19063.jpg",
    avgRating: 4.3,
    year: 2005,
    tags: ["Historical Fiction", "Young Adult", "War"],
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
  <div class="home-view">
    <!-- 推荐图书部分 -->
    <section class="recommended-section">
      <div class="section-header">
        <h2>推荐图书</h2>
        <p>为您精心挑选的优质图书</p>
      </div>

      <!-- 推荐图书加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
      </div>

      <!-- 推荐图书网格 -->
      <div v-else class="books-grid recommended-grid">
        <div
          v-for="book in recommendedBooks"
          :key="book.id"
          class="book-item"
        >
          <BookCard :book="book" />
        </div>
      </div>
    </section>

    <!-- 图书库部分 -->
    <section class="library-section">
      <div class="section-header">
        <h2>图书库</h2>
        <p>探索更多精彩图书</p>
        <div class="section-actions">
          <el-button type="primary" size="small">
            <el-icon><Search /></el-icon>
            搜索图书
          </el-button>
          <el-button size="small">
            <el-icon><Filter /></el-icon>
            筛选
          </el-button>
        </div>
      </div>

      <!-- 图书库加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
      </div>

      <!-- 图书库网格 -->
      <div v-else class="books-grid library-grid">
        <div
          v-for="book in libraryBooks"
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
    </section>
  </div>
</template>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 通用部分样式 */
.section-header {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.section-header h2 {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.section-header p {
  font-size: 16px;
  color: #606266;
  margin: 0;
  flex: 1;
}

.section-actions {
  display: flex;
  gap: 12px;
}

.loading-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.books-grid {
  display: grid;
  gap: 20px;
  margin-bottom: 40px;
}

.recommended-grid {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

.library-grid {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

.book-item {
  height: 400px;
}

.load-more {
  text-align: center;
  margin-top: 40px;
}

/* 推荐图书部分 */
.recommended-section {
  margin-bottom: 60px;
  padding-bottom: 40px;
  border-bottom: 1px solid #e4e7ed;
}

.recommended-section .section-header {
  text-align: center;
  flex-direction: column;
}

.recommended-section .section-header h2 {
  font-size: 32px;
  margin-bottom: 8px;
}

/* 图书库部分 */
.library-section {
  margin-bottom: 40px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-view {
    padding: 16px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .section-header h2 {
    font-size: 24px;
  }

  .section-header p {
    font-size: 14px;
  }

  .section-actions {
    width: 100%;
    justify-content: center;
  }

  .recommended-section .section-header h2 {
    font-size: 28px;
  }

  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }

  .book-item {
    height: 360px;
  }

  .recommended-section {
    margin-bottom: 40px;
    padding-bottom: 30px;
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

  .section-actions {
    flex-direction: column;
    width: 100%;
  }

  .section-actions .el-button {
    width: 100%;
  }
}
</style> 