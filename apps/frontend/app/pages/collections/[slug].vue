<template>
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <NuxtLink to="/" class="text-sm text-text-tertiary hover:text-text-secondary transition-colors mb-2 inline-block">
        &larr; Back
      </NuxtLink>
      <h1 class="text-3xl font-bold text-text-primary">{{ title }}</h1>
    </div>

    <WebsiteWebsiteGrid
      :websites="websites"
      :loading="loading"
    />

    <UiPagination
      v-if="meta"
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
const slug = route.params.slug as string

const { fetchCollectionWebsites, fetchCollections } = useCategories()

const websites = ref<Website[]>([])
const meta = ref<PaginationMeta | null>(null)
const loading = ref(true)
const title = ref(slug)
const page = ref(Number(route.query.page) || 1)

useSeoMeta({
  title: () => `${title.value} - UILove`,
})

async function loadData() {
  loading.value = true
  try {
    const [collectionData, response] = await Promise.all([
      fetchCollections().then(cols => cols.find(c => c.slug === slug)),
      fetchCollectionWebsites(slug, page.value),
    ])
    if (collectionData) title.value = collectionData.title
    websites.value = response.data
    meta.value = response.meta
  } catch (e: any) {
    console.error('Failed to load collection:', e)
  } finally {
    loading.value = false
  }
}

function onPageChange(p: number) {
  page.value = p
  router.push({ query: { ...route.query, page: p > 1 ? String(p) : undefined } })
  loadData()
}

await loadData()
</script>
