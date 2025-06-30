import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Book, Response } from '../models'
import { getBookInfo, getBookList, getBookRecommend } from '../api'

export const useBookStore = defineStore('book', () => {
  // 状态定义
  const bookDetail = ref<Book | null>(null)
  const bookList = ref<Book[]>([])
  const totalBooks = ref(0)
  const recommendedBooks = ref<Book[]>([])
  
  // 加载状态
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  // 分页信息
  const currentPage = ref(1)
  const pageSize = ref(12)
  
  // 计算属性
  const hasMoreBooks = computed(() => {
    return bookList.value.length < totalBooks.value
  })
  
  const isLoading = computed(() => loading.value)
  
  const hasError = computed(() => error.value !== null)
  
  // 获取图书详情
  const getBookDetail = async (id: number) => {
    try {
      loading.value = true
      error.value = null
      
      const response: Response<Book> = await getBookInfo(id)
      
      // 检查响应状态码
      if (response.code === 200) {
        bookDetail.value = response.data
        return response.data
      } else {
        error.value = response.message || '获取图书详情失败'
        throw new Error(response.message || '获取图书详情失败')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取图书详情失败'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  // 获取图书列表
  const fetchBookList = async (page: number = 1, size: number = 12, reset: boolean = false) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await getBookList(page, size)
      
      // 检查响应状态码
      if (response.code === 200) {
        if (reset || page === 1) {
          // 重置列表
          bookList.value = response.data.books
          currentPage.value = 1
        } else {
          // 追加到列表
          bookList.value.push(...response.data.books)
        }
        
        totalBooks.value = response.data.total
        currentPage.value = page
        pageSize.value = size
        
        return response.data
      } else {
        error.value = response.message || '获取图书列表失败'
        throw new Error(response.message || '获取图书列表失败')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取图书列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  // 获取推荐图书
  const getBookRecommendations = async (id: number, by: 'user'|'book') => {
    try {
      loading.value = true
      error.value = null
      
      const response: Response<Book[]> = await getBookRecommend(id, by)
      
      // 检查响应状态码
      if (response.code === 200) {
        recommendedBooks.value = response.data
        return response.data
      } else {
        error.value = response.message || '获取推荐图书失败'
        throw new Error(response.message || '获取推荐图书失败')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取推荐图书失败'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  // 加载更多图书
  const loadMoreBooks = async () => {
    if (hasMoreBooks.value && !loading.value) {
      const nextPage = currentPage.value + 1
      await fetchBookList(nextPage, pageSize.value, false)
    }
  }
  
  // 刷新图书列表
  const refreshBookList = async () => {
    await fetchBookList(1, pageSize.value, true)
  }
  
  // 清除错误
  const clearError = () => {
    error.value = null
  }
  
  // 清除图书详情
  const clearBookDetail = () => {
    bookDetail.value = null
  }
  
  // 清除推荐图书
  const clearRecommendations = () => {
    recommendedBooks.value = []
  }
  
  // 重置store状态
  const resetStore = () => {
    bookDetail.value = null
    bookList.value = []
    totalBooks.value = 0
    recommendedBooks.value = []
    currentPage.value = 1
    pageSize.value = 12
    loading.value = false
    error.value = null
  }
  
  return {
    // 状态
    bookDetail,
    bookList,
    totalBooks,
    recommendedBooks,
    loading,
    error,
    currentPage,
    pageSize,
    
    // 计算属性
    hasMoreBooks,
    isLoading,
    hasError,
    
    // 方法
    getBookDetail,
    fetchBookList,
    getBookRecommendations,
    loadMoreBooks,
    refreshBookList,
    clearError,
    clearBookDetail,
    clearRecommendations,
    resetStore
  }
}) 