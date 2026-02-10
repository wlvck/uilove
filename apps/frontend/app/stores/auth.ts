import { defineStore } from 'pinia'
import type { User } from '~/types'

const TOKEN_KEY = 'uilove_admin_token'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  function setToken(newToken: string) {
    token.value = newToken
    if (import.meta.client) {
      localStorage.setItem(TOKEN_KEY, newToken)
    }
  }

  function setUser(newUser: User) {
    user.value = newUser
  }

  function clearAuth() {
    token.value = null
    user.value = null
    error.value = null
    if (import.meta.client) {
      localStorage.removeItem(TOKEN_KEY)
    }
  }

  function initFromStorage() {
    if (import.meta.client) {
      const stored = localStorage.getItem(TOKEN_KEY)
      if (stored) {
        token.value = stored
      }
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    setToken,
    setUser,
    clearAuth,
    initFromStorage,
  }
})
