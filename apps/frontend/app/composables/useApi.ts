import type { PaginatedResponse } from '~/types'

export function useApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string

  async function get<T>(endpoint: string, params?: Record<string, string | number | undefined>): Promise<T> {
    const query: Record<string, string> = {}
    if (params) {
      for (const [key, value] of Object.entries(params)) {
        if (value !== undefined && value !== '') {
          query[key] = String(value)
        }
      }
    }

    return await $fetch<T>(`${baseURL}${endpoint}`, { query })
  }

  async function getPaginated<T>(endpoint: string, params?: Record<string, string | number | undefined>): Promise<PaginatedResponse<T>> {
    return get<PaginatedResponse<T>>(endpoint, params)
  }

  return { get, getPaginated, baseURL }
}
