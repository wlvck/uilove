import type { Filters } from '~/types'

export function useFilters() {
  const route = useRoute()
  const router = useRouter()

  const filters = computed<Filters>(() => ({
    category: route.query.category as string | undefined,
    style: route.query.style as string | undefined,
    collection: route.query.collection as string | undefined,
    platform: route.query.platform as string | undefined,
    q: route.query.q as string | undefined,
    page: route.query.page ? Number(route.query.page) : 1,
  }))

  function setFilter(key: keyof Filters, value: string | number | undefined) {
    const query = { ...route.query }
    if (value === undefined || value === '') {
      delete query[key]
    } else {
      query[key] = String(value)
    }
    if (key !== 'page') {
      delete query.page
    }
    router.push({ query })
  }

  function clearFilters() {
    router.push({ query: {} })
  }

  function removeFilter(key: keyof Filters) {
    setFilter(key, undefined)
  }

  const hasActiveFilters = computed(() => {
    const { page, ...rest } = filters.value
    return Object.values(rest).some(v => v !== undefined && v !== '')
  })

  const activeFilterEntries = computed(() => {
    const entries: { key: keyof Filters; value: string }[] = []
    const { page, ...rest } = filters.value
    for (const [key, value] of Object.entries(rest)) {
      if (value !== undefined && value !== '') {
        entries.push({ key: key as keyof Filters, value: String(value) })
      }
    }
    return entries
  })

  return {
    filters,
    setFilter,
    clearFilters,
    removeFilter,
    hasActiveFilters,
    activeFilterEntries,
  }
}
