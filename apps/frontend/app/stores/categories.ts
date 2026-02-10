import { defineStore } from 'pinia'
import type { Category, Style, Collection, Platform } from '~/types'

export const useCategoriesStore = defineStore('categories', () => {
  const categories = ref<Category[]>([])
  const styles = ref<Style[]>([])
  const collections = ref<Collection[]>([])
  const platforms = ref<Platform[]>([])
  const loaded = ref(false)

  const { fetchCategories, fetchStyles, fetchCollections, fetchPlatforms } = useCategories()

  async function loadAll() {
    if (loaded.value) return
    try {
      const [cats, stls, cols, plts] = await Promise.all([
        fetchCategories(),
        fetchStyles(),
        fetchCollections(),
        fetchPlatforms(),
      ])
      categories.value = cats
      styles.value = stls
      collections.value = cols
      platforms.value = plts
      loaded.value = true
    } catch (e: any) {
      console.error('Failed to load filter data:', e)
    }
  }

  function getCategoryBySlug(slug: string) {
    return categories.value.find(c => c.slug === slug)
  }

  function getStyleBySlug(slug: string) {
    return styles.value.find(s => s.slug === slug)
  }

  return {
    categories,
    styles,
    collections,
    platforms,
    loaded,
    loadAll,
    getCategoryBySlug,
    getStyleBySlug,
  }
})
