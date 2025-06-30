import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useBookStore } from './book'

export const useUserStore = defineStore('user', () => {
    const userId = ref<number | null>(null)
    const isLoggedIn = ref(false)
    const error = ref<string | null>(null)

    // 简单登录方法
    const login = async (id: number) => {
        if (!id || isNaN(id)) {
            error.value = '请输入有效的用户ID'
            isLoggedIn.value = false
            userId.value = null
            return false
        }
        userId.value = id
        isLoggedIn.value = true
        error.value = null
        return true
    }

    // 登出
    const logout = () => {
        userId.value = null
        isLoggedIn.value = false
        error.value = null
        // 登出时重置图书store
        const bookStore = useBookStore()
        bookStore.resetStore()
    }

    return {
        userId,
        isLoggedIn,
        error,
        login,
        logout
    }
})