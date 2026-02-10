export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore()
  const { initAuth } = useAuth()

  // Skip middleware on server-side
  if (import.meta.server) return

  // Initialize auth from storage if not already done
  if (!authStore.token) {
    await initAuth()
  }

  // Protect admin routes (except login)
  if (to.path.startsWith('/admin') && to.path !== '/admin/login') {
    if (!authStore.isAuthenticated) {
      return navigateTo('/admin/login')
    }
  }

  // Redirect authenticated users away from login
  if (to.path === '/admin/login' && authStore.isAuthenticated) {
    return navigateTo('/admin/websites')
  }
})
