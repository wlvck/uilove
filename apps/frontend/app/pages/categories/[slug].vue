<template>
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <NuxtLink to="/categories" class="text-sm text-text-tertiary hover:text-text-secondary transition-colors mb-2 inline-block">
        &larr; All Categories
      </NuxtLink>
      <h1 class="text-3xl font-bold text-text-primary">{{ title }}</h1>
      <p v-if="description" class="mt-2 text-text-secondary">{{ description }}</p>
    </div>

    <!-- Grid -->
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

const { fetchCategoryWebsites, fetchCategories } = useCategories()

const websites = ref<Website[]>([])
const meta = ref<PaginationMeta | null>(null)
const loading = ref(true)
const title = ref(slug)
const description = ref<string | null>(null)
const page = ref(Number(route.query.page) || 1)

useSeoMeta({
  title: () => `${title.value} - UILove`,
})

async function loadData() {
  loading.value = true
  try {
    const [categoryData, response] = await Promise.all([
      fetchCategories().then(cats => cats.find(c => c.slug === slug)),
      fetchCategoryWebsites(slug, page.value),
    ])
    if (categoryData) {
      title.value = categoryData.title
      description.value = categoryData.description
    }
    websites.value = response.items
    meta.value = { page: response.page, size: response.size, total: response.total, pages: response.pages }
  } catch (e: any) {
    console.error('Failed to load category:', e)
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
