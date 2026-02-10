<template>
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-3xl font-bold text-text-primary mb-8">Categories</h1>

    <UiLoadingSpinner v-if="!categoriesStore.loaded" size="lg" />

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <NuxtLink
        v-for="category in categoriesStore.categories"
        :key="category.slug"
        :to="`/categories/${category.slug}`"
        class="group p-6 rounded-xl bg-bg-card border border-border hover:border-border-hover transition-all"
      >
        <div class="flex items-center gap-3 mb-3">
          <div class="h-10 w-10 rounded-lg bg-accent/10 flex items-center justify-center">
            <Icon :name="category.icon || 'ph:folder'" class="h-5 w-5 text-accent-light" />
          </div>
          <h2 class="text-base font-semibold text-text-primary group-hover:text-accent-light transition-colors">
            {{ category.title }}
          </h2>
        </div>
        <p v-if="category.description" class="text-sm text-text-secondary line-clamp-2 mb-3">
          {{ category.description }}
        </p>
        <span class="text-xs text-text-tertiary">
          {{ category.website_count }} {{ category.website_count === 1 ? 'website' : 'websites' }}
        </span>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
const categoriesStore = useCategoriesStore()

useSeoMeta({
  title: 'Categories - UILove',
})

categoriesStore.loadAll()
</script>
