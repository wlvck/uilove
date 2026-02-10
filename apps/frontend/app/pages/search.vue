<template>
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
    <!-- Search Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-text-primary mb-4">Search</h1>
      <div class="max-w-xl">
        <FilterSearchInput
          v-model="query"
          placeholder="Search for websites..."
          autofocus
          @submit="doSearch"
        />
      </div>
    </div>

    <!-- Results info -->
    <p v-if="searched && !loading" class="text-sm text-text-secondary mb-6">
      <template v-if="websites.length">
        Found {{ meta?.total || websites.length }} result{{ (meta?.total || websites.length) === 1 ? '' : 's' }} for "{{ searchedQuery }}"
      </template>
      <template v-else>
        No results found for "{{ searchedQuery }}"
      </template>
    </p>

    <!-- Grid -->
    <WebsiteWebsiteGrid
      :websites="websites"
      :loading="loading"
    />

    <UiPagination
      v-if="meta && meta.total_pages > 1"
      :current-page="page"
      :total-pages="meta.total_pages"
      @update:current-page="onPageChange"
    />
  </div>
</template>

<script setup lang="ts">
import type { Website, PaginationMeta } from '~/types'

const route = useRoute()
const router = useRouter()
const { fetchWebsites } = useWebsites()

const query = ref((route.query.q as string) || '')
const searchedQuery = ref('')
const websites = ref<Website[]>([])
const meta = ref<PaginationMeta | null>(null)
const loading = ref(false)
const searched = ref(false)
const page = ref(Number(route.query.page) || 1)

useSeoMeta({
  title: () => query.value ? `Search: ${query.value} - UILove` : 'Search - UILove',
})

async function doSearch() {
  if (!query.value.trim()) return
  loading.value = true
  searched.value = true
  searchedQuery.value = query.value.trim()

  router.push({ query: { q: query.value.trim(), page: page.value > 1 ? String(page.value) : undefined } })

  try {
    const response = await fetchWebsites({ q: query.value.trim(), page: page.value })
    websites.value = response.data
    meta.value = response.meta
  } catch (e: any) {
    console.error('Search failed:', e)
  } finally {
    loading.value = false
  }
}

function onPageChange(p: number) {
  page.value = p
  doSearch()
}

if (query.value) {
  await doSearch()
}
</script>
