import { defineStore } from 'pinia'
import type { Website, PaginationMeta, Filters } from '~/types'

export const useWebsitesStore = defineStore('websites', () => {
  const websites = ref<Website[]>([])
  const currentWebsite = ref<Website | null>(null)
  const featured = ref<Website[]>([])
  const meta = ref<PaginationMeta | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const { fetchWebsites, fetchWebsite, fetchFeatured } = useWebsites()

  async function loadWebsites(filters: Filters = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await fetchWebsites(filters)
      websites.value = response.data
      meta.value = response.meta
    } catch (e: any) {
      error.value = e?.message || 'Failed to load websites'
    } finally {
      loading.value = false
    }
  }

  async function loadWebsite(slug: string) {
    loading.value = true
    error.value = null
    try {
      currentWebsite.value = await fetchWebsite(slug)
    } catch (e: any) {
      error.value = e?.message || 'Failed to load website'
    } finally {
      loading.value = false
    }
  }

  async function loadFeatured() {
    try {
      featured.value = await fetchFeatured()
    } catch (e: any) {
      console.error('Failed to load featured websites:', e)
    }
  }

  return {
    websites,
    currentWebsite,
    featured,
    meta,
    loading,
    error,
    loadWebsites,
    loadWebsite,
    loadFeatured,
  }
})
