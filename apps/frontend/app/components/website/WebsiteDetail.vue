<template>
  <div>
    <!-- Image -->
    <div class="relative rounded-xl overflow-hidden bg-bg-card border border-border">
      <NuxtImg
        v-if="website.image_url || website.thumbnail_url"
        :src="(website.image_url || website.thumbnail_url)!"
        :alt="website.title"
        class="w-full"
        placeholder
      />
      <div v-else class="aspect-video flex items-center justify-center bg-bg-tertiary">
        <Icon name="ph:image" class="h-16 w-16 text-text-tertiary" />
      </div>
    </div>

    <!-- Info -->
    <div class="mt-8 space-y-6">
      <div>
        <div class="flex items-start justify-between gap-4 flex-wrap">
          <h1 class="text-2xl font-bold text-text-primary">{{ website.title }}</h1>
          <div class="flex items-center gap-2 text-sm text-text-tertiary">
            <Icon name="ph:eye" class="h-4 w-4" />
            {{ formatNumber(website.view_count) }} views
          </div>
        </div>

        <p v-if="website.description" class="mt-3 text-text-secondary leading-relaxed">
          {{ website.description }}
        </p>
      </div>

      <!-- Visit Button -->
      <div v-if="website.original_url">
        <a
          :href="website.original_url"
          target="_blank"
          rel="noopener noreferrer"
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-accent hover:bg-accent-hover text-white text-sm font-medium transition-colors"
        >
          <Icon name="ph:arrow-square-out" class="h-4 w-4" />
          Visit Website
        </a>
      </div>

      <!-- Tags -->
      <div class="flex flex-wrap gap-2">
        <NuxtLink
          v-for="cat in website.categories"
          :key="cat.slug"
          :to="`/categories/${cat.slug}`"
        >
          <UiBadge variant="accent" size="md">{{ cat.title }}</UiBadge>
        </NuxtLink>
        <NuxtLink
          v-for="style in website.styles"
          :key="style.slug"
          :to="`/styles/${style.slug}`"
        >
          <UiBadge variant="outline" size="md">{{ style.title }}</UiBadge>
        </NuxtLink>
        <UiBadge v-if="website.platform" size="md">
          {{ website.platform.title }}
        </UiBadge>
      </div>

      <!-- Meta -->
      <div class="text-sm text-text-tertiary">
        Added {{ formatDate(website.created_at) }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Website } from '~/types'
import { formatNumber, formatDate } from '~/utils/helpers'

defineProps<{
  website: Website
}>()
</script>
