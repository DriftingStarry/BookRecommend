<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBookStore } from '../stores'
import { useUserStore } from '../stores/user'
import type { Book } from '../models'
import BookCard from '../components/BookCard.vue'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const bookStore = useBookStore()
const userStore = useUserStore()

const bookId = ref<number>(Number(route.params.id))
const loading = ref(true)
const error = ref('')

const book = ref<Book | null>(null)

const isFavored = computed(() => {
  return bookStore.favorBooks.includes(bookId.value)
})

const favorLoading = ref(false)

const handleFavor = async () => {
  if (favorLoading.value) return
  if (!userStore.userId) {
    ElMessage.warning('请先登录')
    return
  }
  favorLoading.value = true
  try {
    if (isFavored.value) {
      await bookStore.delFavorBook(userStore.userId, bookId.value)
      // 本地移除
      const idx = bookStore.favorBooks.indexOf(bookId.value)
      if (idx !== -1) bookStore.favorBooks.splice(idx, 1)
      ElMessage.success('已取消喜爱')
    } else {
      await bookStore.addFavorBook(userStore.userId, bookId.value)
      bookStore.favorBooks.push(bookId.value)
      ElMessage.success('已添加到喜爱')
    }
  } catch (e) {
    ElMessage.error(e instanceof Error ? e.message : '操作失败')
  } finally {
    favorLoading.value = false
  }
}

const fetchData = async () => {
  loading.value = true
  error.value = ''
  try {
    // 获取书籍详情
    const detail = await bookStore.getBookDetail(bookId.value)
    book.value = detail
    // 获取相关推荐
    await bookStore.getDetailRecommendations(bookId.value, 'book')
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

const formatCount = (count: number | string | undefined) => {
  if (!count || isNaN(Number(count))) return ''
  const n = Number(count)
  if (n >= 10000) return (n / 10000).toFixed(1).replace(/\.0$/, '') + '万'
  if (n >= 1000) return (n / 1000).toFixed(1).replace(/\.0$/, '') + '千'
  return n.toLocaleString()
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
          <h2>
            {{ book.title }}
            <el-button
              circle
              :type="isFavored ? 'danger' : 'info'"
              size="small"
              style="margin-left:8px;vertical-align:middle"
              @click="handleFavor"
              :icon="isFavored ? 'el-icon-star-on' : 'el-icon-star-off'"
              :loading="favorLoading"
              :disabled="favorLoading"
            >
              <el-icon v-if="isFavored"><svg viewBox="0 0 24 24" width="1em" height="1em"><path fill="currentColor" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41 0.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"></path></svg></el-icon>
              <el-icon v-else><svg viewBox="0 0 24 24" width="1em" height="1em"><path fill="currentColor" d="M16.5 3c-1.74 0-3.41 0.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04 1 3.57 2.36h1.87C13.46 6 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z"></path></svg></el-icon>
            </el-button>
          </h2>
          <p>作者：{{ book.authors }}</p>
          <p v-if="book.year">出版年份：{{ book.year }}</p>
          <p v-if="book.avgRating">评分：{{ book.avgRating }}</p>
          <p v-if="book.ratingsCount" class="ratings-count">
            {{ formatCount(book.ratingsCount) }}<span v-if="formatCount(book.ratingsCount)">人评分</span>
          </p>
          <p v-if="book.tags && book.tags.length">标签：
            <el-tag v-for="tag in book.tags" :key="tag" size="small" style="margin-right:4px">{{ tag }}</el-tag>
          </p>
          <el-button type="primary" @click="goToGoodreads" :disabled="!book.goodreadsId">前往Goodreads</el-button>
        </div>
      </div>
      <div class="recommend-section">
        <h3>相关推荐</h3>
        <div v-if="bookStore.detailRecommendedBooks && bookStore.detailRecommendedBooks.length > 0" class="recommend-grid">
          <BookCard v-for="rec in bookStore.detailRecommendedBooks" :key="rec.id" :book="rec" />
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
.ratings-count {
  font-size: 13px;
  color: #909399;
  margin: 0 0 8px 0;
  line-height: 1.2;
}

@media (max-width: 768px) {
  .detail-card {
    padding: 16px 4px;
  }
  .detail-header {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
  .cover-box {
    width: 140px;
    height: 200px;
    min-width: 0;
    margin: 0 auto;
  }
  .info-box {
    width: 100%;
    text-align: center;
  }
  .info-box h2 {
    font-size: 22px;
  }
}
</style> 