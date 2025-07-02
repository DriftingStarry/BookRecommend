<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useBookStore } from '../stores'
import { useUserStore } from '../stores/user'
import BookCard from '../components/BookCard.vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const bookStore = useBookStore()
const userStore = useUserStore()
const router = useRouter()

const favorBooks = ref<any[]>([])
const loading = ref(false)

const fetchFavorBooks = async () => {
  if (!userStore.userId) return
  loading.value = true
  try {
    // 获取喜爱书籍 id 列表
    const ids = await bookStore.getFavorBooks(userStore.userId)
    // 批量获取详情
    favorBooks.value = []
    for (const id of ids) {
      try {
        const detail = await bookStore.getBookDetail(id)
        favorBooks.value.push(detail)
      } catch {}
    }
  } finally {
    loading.value = false
  }
}

const handleDelete = async (bookId: number) => {
  if (!userStore.userId) return
  loading.value = true
  try {
    await bookStore.delFavorBook(userStore.userId, bookId)
    favorBooks.value = favorBooks.value.filter(b => b.id !== bookId)
    // 同步 store
    const idx = bookStore.favorBooks.indexOf(bookId)
    if (idx !== -1) bookStore.favorBooks.splice(idx, 1)
    ElMessage.success('已取消喜爱')
  } catch (e) {
    ElMessage.error(e instanceof Error ? e.message : '操作失败')
  } finally {
    loading.value = false
  }
}

onMounted(fetchFavorBooks)
</script>

<template>
  <div class="favor-view">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
      <el-button type="primary" @click="() => router.push('/')">返回主页</el-button>
      <h2 style="margin:0;">我的喜爱书籍</h2>
    </div>
    <el-empty v-if="!loading && favorBooks.length === 0" description="暂无喜爱书籍" />
    <div v-else class="favor-grid">
      <el-skeleton v-if="loading" :rows="4" animated />
      <BookCard
        v-for="book in favorBooks"
        :key="book.id"
        :book="book"
      >
        <template #footer>
          <el-button type="danger" size="small" @click.stop="handleDelete(book.id)">取消喜爱</el-button>    
        </template>
      </BookCard>
    </div>
  </div>
</template>

<style scoped>
.favor-view {
  max-width: 1000px;
  margin: 32px auto;
  padding: 0 12px;
}
.favor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
</style>
