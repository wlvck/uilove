<template>
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
    <!-- Hero -->
    <section class="text-center py-12 sm:py-16">
      <h1 class="text-4xl sm:text-5xl font-bold text-text-primary tracking-tight">
        Discover Beautiful
        <span class="text-accent">Landing Pages</span>
      </h1>
      <p class="mt-4 text-lg text-text-secondary max-w-2xl mx-auto">
        A curated gallery of the best designed landing pages for your inspiration.
      </p>
    </section>

    <!-- Filters -->
    <section class="space-y-4 mb-8">
      <FilterCategoryFilter
        v-if="categoriesStore.categories.length"
        :categories="categoriesStore.categories"
        :selected="filters.category"
        @update:selected="(v) => setFilter('category', v)"
      />

      <FilterStyleFilter
        v-if="categoriesStore.styles.length"
        :styles="categoriesStore.styles"
        :selected="filters.style"
        @update:selected="(v) => setFilter('style', v)"
      />

      <FilterActiveFilters
        :filters="activeFilterEntries"
        @remove="(key) => removeFilter(key as any)"
        @clear="clearFilters"
      />
    </section>

    <!-- Grid with Sidebar -->
    <div class="flex gap-8">
      <LayoutSidebar />

      <div class="flex-1 min-w-0">
        <WebsiteGrid
          :websites="websitesStore.websites"
          :loading="websitesStore.loading"
        />

        <UiPagination
          v-if="websitesStore.meta"
          :current-page="filters.page || 1"
          :total-pages="websitesStore.meta.pages"
          @update:current-page="(p) => setFilter('page', p)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const websitesStore = useWebsitesStore()
const categoriesStore = useCategoriesStore()
const { filters, setFilter, removeFilter, clearFilters, activeFilterEntries } = useFilters()

useSeoMeta({
  title: 'UILove - Curated Landing Page Gallery',
  description: 'Discover beautifully designed landing pages for your inspiration.',
})

categoriesStore.loadAll()

watch(
  filters,
  (newFilters) => {
    websitesStore.loadWebsites(newFilters)
  },
  { immediate: true },
)
</script>
