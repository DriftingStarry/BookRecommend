<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookStore } from '../stores'
import type { Book } from '../models'
import BookCard from '../components/BookCard.vue'
import { ArrowLeft } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const bookStore = useBookStore()

const bookId = ref<number>(Number(route.params.id))
const loading = ref(true)
const error = ref('')

const book = ref<Book | null>(null)
const recommendations = ref<Book[]>([])

const fetchData = async () => {
  loading.value = true
  error.value = ''
  try {
    // 获取书籍详情
    const detail = await bookStore.getBookDetail(bookId.value)
    book.value = detail
    // 获取相关推荐
    recommendations.value = await bookStore.getBookRecommendations(bookId.value, 'book')
  } catch (e) {
    error.value = (e instanceof Error ? e.message : '加载失败')
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
watch(() => route.params.id, (newId) => {
  bookId.value = Number(newId)
  fetchData()
})

const goToGoodreads = () => {
  if (book.value && book.value.goodreadsId) {
    window.open(`https://www.goodreads.com/book/show/${book.value.goodreadsId}`, '_blank')
  }
}

const goBackHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="book-detail-view">
    <el-button class="back-btn" circle size="large" @click="goBackHome">
      <el-icon><ArrowLeft /></el-icon>
    </el-button>
    <el-card v-if="loading" class="loading-card">
      <el-skeleton :rows="6" animated />
    </el-card>
    <el-card v-else-if="error" class="error-card">
      <el-alert :title="error" type="error" show-icon />
    </el-card>
    <el-card v-else-if="book" class="detail-card">
      <div class="detail-header">
        <div class="cover-box">
          <el-image :src="book.cover || '/default-book-cover.svg'" fit="contain" class="cover-img" />
        </div>
        <div class="info-box">
          <h2>{{ book.title }}</h2>
          <p>作者：{{ book.authors }}</p>
          <p v-if="book.year">出版年份：{{ book.year }}</p>
          <p v-if="book.avgRating">评分：{{ book.avgRating }}</p>
          <p v-if="book.tags && book.tags.length">标签：
            <el-tag v-for="tag in book.tags" :key="tag" size="small" style="margin-right:4px">{{ tag }}</el-tag>
          </p>
          <el-button type="primary" @click="goToGoodreads" :disabled="!book.goodreadsId">前往Goodreads</el-button>
        </div>
      </div>
      <div class="recommend-section">
        <h3>相关推荐</h3>
        <div v-if="recommendations && recommendations.length > 0" class="recommend-grid">
          <BookCard v-for="rec in recommendations" :key="rec.id" :book="rec" />
        </div>
        <el-empty v-else description="暂无相关推荐" />
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.book-detail-view {
  max-width: 900px;
  margin: 32px auto;
  padding: 0 12px;
  position: relative;
}
.back-btn {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 10;
  background: #fff;
  box-shadow: 0 2px 8px rgba(64,158,255,0.12);
}
.detail-card {
  padding: 32px 24px;
}
.detail-header {
  display: flex;
  gap: 32px;
  align-items: flex-start;
  margin-bottom: 32px;
}
.cover-box {
  width: 180px;
  min-width: 120px;
  height: 260px;
  background: #f5f7fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.cover-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.info-box {
  flex: 1;
}
.info-box h2 {
  margin: 0 0 12px 0;
  font-size: 26px;
  font-weight: 600;
}
.info-box p {
  margin: 0 0 8px 0;
  color: #606266;
}
.recommend-section {
  margin-top: 32px;
}
.recommend-section h3 {
  font-size: 20px;
  margin-bottom: 16px;
}
.recommend-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}
.loading-card, .error-card {
  margin: 32px auto;
  max-width: 500px;
}
</style> 