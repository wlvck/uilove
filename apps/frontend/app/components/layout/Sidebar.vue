<template>
  <aside class="hidden lg:block w-56 shrink-0">
    <div class="sticky top-20 space-y-6">
      <!-- Categories -->
      <div>
        <h3 class="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-3">Categories</h3>
        <ul class="space-y-1">
          <li v-for="category in categories" :key="category.slug">
            <NuxtLink
              :to="`/categories/${category.slug}`"
              class="flex items-center justify-between px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
              active-class="bg-bg-tertiary text-text-primary"
            >
              <span>{{ category.title }}</span>
              <span class="text-xs text-text-tertiary">{{ category.website_count }}</span>
            </NuxtLink>
          </li>
        </ul>
      </div>

      <!-- Styles -->
      <div v-if="styles.length">
        <h3 class="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-3">Styles</h3>
        <ul class="space-y-1">
          <li v-for="style in styles" :key="style.slug">
            <NuxtLink
              :to="`/styles/${style.slug}`"
              class="flex items-center justify-between px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
              active-class="bg-bg-tertiary text-text-primary"
            >
              <span>{{ style.title }}</span>
              <span class="text-xs text-text-tertiary">{{ style.website_count }}</span>
            </NuxtLink>
          </li>
        </ul>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
const categoriesStore = useCategoriesStore()
const { categories, styles } = storeToRefs(categoriesStore)

onMounted(() => {
  categoriesStore.loadAll()
})
</script>
