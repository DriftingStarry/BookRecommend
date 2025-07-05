<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { useBookStore } from '../stores'
import BookCard from '../components/BookCard.vue'
import { useUserStore } from '../stores'

const userStore = useUserStore()

// 使用图书store
const bookStore = useBookStore()

const randomRecommendedBooks = ref<any[]>([])

function pickRandomBooks() {
  const all = bookStore.homeRecommendedBooks
  if (!all || all.length === 0) {
    randomRecommendedBooks.value = []
    return
  }
  // 随机选取三本
  const shuffled = all.slice().sort(() => Math.random() - 0.5)
  randomRecommendedBooks.value = shuffled.slice(0, 3)
}

// 组件挂载时加载数据
onMounted(async () => {
  try {
    // 只在没有数据时才获取
    if (bookStore.bookList.length === 0) {
      await bookStore.fetchBookList(1, 12, true)
    }
    if (bookStore.homeRecommendedBooks.length === 0) {
      await bookStore.getHomeRecommendations(1, 'user')
    }
    pickRandomBooks()
  } catch (error) {
    console.error('加载数据失败:', error)
  }
})

// 监听推荐书籍变化自动刷新随机三本
watch(() => bookStore.homeRecommendedBooks, pickRandomBooks, { deep: true })

// 加载更多图书
const handleLoadMore = async () => {
  try {
    await bookStore.loadMoreBooks()
    // 加载后自动滚动到底部
    // window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' })
  } catch (error) {
    console.error('加载更多图书失败:', error)
  }
}

// 刷新图书列表
const handleRefresh = async () => {
  try {
    await bookStore.refreshBookList()
  } catch (error) {
    console.error('刷新图书列表失败:', error)
  }
}

// 刷新推荐图书
const handleRefreshRecommendations = async () => {
  try {
    if (userStore.isLoggedIn) {
      await bookStore.getHomeRecommendations(userStore.userId!, 'user')
    } else {
      await bookStore.getHomeRecommendations(Math.floor(Math.random() * 10000), 'book')
    }
    pickRandomBooks()
  } catch (error) {
    console.error('刷新推荐图书失败:', error)
  }
}
</script>

<template>
  <div class="home-view">
    <!-- 错误提示 -->
    <div v-if="bookStore.hasError" class="error-message">
      <el-alert
        :title="bookStore.error"
        type="error"
        show-icon
        closable
        @close="bookStore.clearError"
      />
    </div>

    <!-- 推荐图书部分 -->
    <section class="recommended-section">
      <div class="section-header">
        <h2>推荐图书</h2>
        <p>{{userStore.isLoggedIn ? '今日推荐' : '为您推荐 (登入后获得个性化推荐)'}}</p>
        <div class="section-actions">
          <el-button 
            type="primary" 
            size="small"
            :loading="bookStore.isLoading"
            @click="handleRefreshRecommendations"
          >
            刷新推荐
          </el-button>
        </div>
      </div>

      <!-- 推荐图书加载状态 -->
      <div v-if="bookStore.isLoading && (!bookStore.homeRecommendedBooks || bookStore.homeRecommendedBooks.length === 0)" class="loading-container">
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated />
      </div>

      <!-- 推荐图书网格 -->
      <div v-else-if="randomRecommendedBooks && randomRecommendedBooks.length > 0" class="books-grid recommended-grid">
        <div
          v-for="book in randomRecommendedBooks"
          :key="book.id"
          class="book-item"
        >
          <BookCard :book="book" />
        </div>
      </div>

      <!-- 推荐图书空状态 -->
      <div v-else-if="!bookStore.isLoading" class="empty-state">
        <el-empty description="暂无推荐图书" />
      </div>
    </section>

    <!-- 图书库部分 -->
    <section class="library-section">
      <div class="section-header">
        <h2>图书库</h2>
        <p>探索更多精彩图书</p>
        <div class="section-actions">
          <el-button 
            type="primary" 
            size="small"
            :loading="bookStore.isLoading"
            @click="handleRefresh"
          >
            刷新列表
          </el-button>
        </div>
      </div>

      <!-- 图书库加载状态 -->
      <div v-if="bookStore.isLoading && (!bookStore.bookList || bookStore.bookList.length === 0)" class="loading-container">
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
      <div v-else-if="bookStore.bookList && bookStore.bookList.length > 0" class="books-grid library-grid">
        <div
          v-for="book in bookStore.bookList"
          :key="book.id"
          class="book-item"
        >
          <BookCard :book="book" />
        </div>
      </div>

      <!-- 图书库空状态 -->
      <div v-else-if="!bookStore.isLoading" class="empty-state">
        <el-empty description="暂无图书数据" />
      </div>

      <!-- 加载更多按钮 -->
      <div v-if="bookStore.bookList && bookStore.bookList.length > 0" class="load-more">
        <el-button 
          type="primary" 
          size="large" 
          :loading="bookStore.isLoading"
          :disabled="!bookStore.hasMoreBooks"
          @click="handleLoadMore"
        >
          {{ bookStore.hasMoreBooks ? '加载更多图书' : '已加载全部图书' }}
        </el-button>
      </div>

      <!-- 加载状态指示器 -->
      <div v-if="bookStore.isLoading && bookStore.bookList && bookStore.bookList.length > 0" class="loading-indicator">
        <el-skeleton :rows="1" animated />
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

.error-message {
  margin-bottom: 20px;
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

.empty-state {
  text-align: center;
  margin: 60px 0;
}

.loading-indicator {
  text-align: center;
  margin-top: 20px;
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

  .load-more {
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: center;
  }

  .load-more .el-button {
    width: 100%;
    max-width: 200px;
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