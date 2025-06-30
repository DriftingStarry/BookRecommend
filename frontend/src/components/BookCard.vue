<script setup lang="ts">
import type { Book } from '../models'

interface Props {
  book: Book
}

defineProps<Props>()
</script>

<template>
  <el-card class="book-card" shadow="hover">
    <div class="book-cover">
      <el-image
        :src="book.cover || '/default-book-cover.svg'"
        fit="contain"
        class="cover-image"
        :alt="book.title"
      >
        <template #error>
          <div class="cover-placeholder">
            <el-icon :size="40" color="#909399">
              <Document />
            </el-icon>
          </div>
        </template>
      </el-image>
    </div>
    
    <div class="book-info">
      <h3 class="book-title" :title="book.title">{{ book.title }}</h3>
      <p class="book-author" :title="book.authors">{{ book.authors }}</p>
      
      <div class="book-meta">
        <div v-if="book.avgRating" class="rating">
          <el-rate
            v-model="book.avgRating"
            disabled
            show-score
            text-color="#ff9900"
            score-template="{value}"
            :max="5"
          />
        </div>
        
        <div v-if="book.year" class="year">
          <el-icon><Calendar /></el-icon>
          <span>{{ book.year }}</span>
        </div>
      </div>
      
      <div v-if="book.tags && book.tags.length > 0" class="tags">
        <el-tag
          v-for="genre in book.tags.slice(0, 3)"
          :key="genre"
          size="small"
          type="info"
          class="genre-tag"
        >
          {{ genre }}
        </el-tag>
      </div>
    </div>
  </el-card>
</template>

<style scoped>
.book-card {
  width: 100%;
  height: 100%;
  transition: all 0.3s ease;
  cursor: pointer;
}

.book-card:hover {
  transform: translateY(-4px);
}

.book-cover {
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 12px;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  color: #909399;
}

.book-info {
  padding: 0 4px;
}

.book-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.book-author {
  font-size: 14px;
  color: #606266;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.book-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.rating {
  flex: 1;
}

.year {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.genre-tag {
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .book-cover {
    height: 160px;
  }
  
  .book-title {
    font-size: 14px;
  }
  
  .book-author {
    font-size: 12px;
  }
  
  .book-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style> 