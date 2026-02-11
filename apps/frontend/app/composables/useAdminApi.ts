import type { PaginatedResponse } from '~/types'

export function useAdminApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string
  const authStore = useAuthStore()

  function getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    }
    if (authStore.token) {
      headers['Authorization'] = `Bearer ${authStore.token}`
    }
    return headers
  }

  async function authGet<T>(endpoint: string, params?: Record<string, string | number | undefined>): Promise<T> {
    const query: Record<string, string> = {}
    if (params) {
      for (const [key, value] of Object.entries(params)) {
        if (value !== undefined && value !== '') {
          query[key] = String(value)
        }
      }
    }

    return await $fetch<T>(`${baseURL}${endpoint}`, {
      headers: getHeaders(),
      query,
    })
  }

  async function authGetPaginated<T>(endpoint: string, params?: Record<string, string | number | undefined>): Promise<PaginatedResponse<T>> {
    return authGet<PaginatedResponse<T>>(endpoint, params)
  }

  async function post<T>(endpoint: string, data: Record<string, any>): Promise<T> {
    return await $fetch<T>(`${baseURL}${endpoint}`, {
      method: 'POST',
      headers: getHeaders(),
      body: data,
    })
  }

  async function put<T>(endpoint: string, data: Record<string, any>): Promise<T> {
    return await $fetch<T>(`${baseURL}${endpoint}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: data,
    })
  }

  async function del(endpoint: string): Promise<void> {
    await $fetch(`${baseURL}${endpoint}`, {
      method: 'DELETE',
      headers: getHeaders(),
    })
  }

  return { authGet, authGetPaginated, post, put, del, baseURL }
}
