<template>
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <NuxtLink to="/" class="text-sm text-text-tertiary hover:text-text-secondary transition-colors mb-2 inline-block">
        &larr; Back
      </NuxtLink>
      <h1 class="text-3xl font-bold text-text-primary">{{ title }}</h1>
    </div>

    <WebsiteGrid
      :websites="websites"
      :loading="loading"
    />

    <UiPagination
      v-if="meta"
      :current-page="page"
      :total-pages="meta.pages"
      @update:current-page="onPageChange"
    />
  </div>
</template>

<script setup lang="ts">
import type { Website, PaginationMeta } from '~/types'

const route = useRoute()
const router = useRouter()
const slug = route.params.slug as string

const { fetchStyleWebsites, fetchStyles } = useCategories()

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
    const [styleData, response] = await Promise.all([
      fetchStyles().then(stls => stls.find(s => s.slug === slug)),
      fetchStyleWebsites(slug, page.value),
    ])
    if (styleData) title.value = styleData.title
    websites.value = response.items
    meta.value = { page: response.page, size: response.size, total: response.total, pages: response.pages }
  } catch (e: any) {
    console.error('Failed to load style:', e)
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
