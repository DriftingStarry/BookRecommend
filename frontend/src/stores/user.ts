import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
    const userId = ref<number>(-1)
    const isLogin = ref<boolean>(false)

    function login(id:number) {
        userId.value = id
        isLogin.value = true
    }

    function logout() {
        userId.value = -1
        isLogin.value = false
    }

    return {
        userId,
        isLogin,
        login,
        logout,
    }
})