import type { User, Token, LoginRequest } from '~/types'

export function useAuth() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string
  const authStore = useAuthStore()

  async function login(email: string, password: string): Promise<void> {
    authStore.loading = true
    authStore.error = null

    try {
      const data: LoginRequest = { email, password }
      const response = await $fetch<Token>(`${baseURL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: data,
      })

      authStore.setToken(response.access_token)
      await fetchUser()
    } catch (e: any) {
      authStore.error = e?.data?.detail || e?.message || 'Login failed'
      throw e
    } finally {
      authStore.loading = false
    }
  }

  async function fetchUser(): Promise<User | null> {
    if (!authStore.token) return null

    try {
      const user = await $fetch<User>(`${baseURL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
        },
      })
      authStore.setUser(user)
      return user
    } catch (e) {
      authStore.clearAuth()
      return null
    }
  }

  function logout() {
    authStore.clearAuth()
    navigateTo('/admin/login')
  }

  async function initAuth(): Promise<boolean> {
    authStore.initFromStorage()
    if (authStore.token) {
      const user = await fetchUser()
      return !!user
    }
    return false
  }

  return {
    login,
    logout,
    fetchUser,
    initAuth,
  }
}
