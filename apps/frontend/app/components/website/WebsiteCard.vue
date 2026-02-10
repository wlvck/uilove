<template>
  <NuxtLink
    :to="`/websites/${website.slug}`"
    class="website-card group block rounded-xl overflow-hidden bg-bg-card border border-border hover:border-border-hover transition-all duration-300"
    @mouseenter="onHover"
    @mouseleave="onLeave"
  >
    <!-- Thumbnail -->
    <div class="relative aspect-[16/10] overflow-hidden bg-bg-tertiary">
      <NuxtImg
        v-if="website.thumbnail_url"
        :src="website.thumbnail_url"
        :alt="website.title"
        class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
        loading="lazy"
        placeholder
      />
      <div v-else class="h-full w-full flex items-center justify-center">
        <Icon name="ph:image" class="h-12 w-12 text-text-tertiary" />
      </div>

      <!-- Featured badge -->
      <div v-if="website.is_featured" class="absolute top-3 left-3">
        <UiBadge variant="accent" size="sm">
          <Icon name="ph:star-fill" class="h-3 w-3 mr-1" />
          Featured
        </UiBadge>
      </div>
    </div>

    <!-- Info -->
    <div class="p-4">
      <h3 class="text-sm font-medium text-text-primary group-hover:text-accent-light transition-colors truncate">
        {{ website.title }}
      </h3>

      <div class="mt-2 flex items-center gap-2 flex-wrap">
        <UiBadge v-for="cat in website.categories.slice(0, 2)" :key="cat.slug" size="sm">
          {{ cat.title }}
        </UiBadge>
      </div>

      <div class="mt-3 flex items-center justify-between text-xs text-text-tertiary">
        <span class="flex items-center gap-1">
          <Icon name="ph:eye" class="h-3.5 w-3.5" />
          {{ formatNumber(website.view_count) }}
        </span>
        <span>{{ formatDate(website.created_at) }}</span>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
import type { Website } from '~/types'
import { formatNumber, formatDate } from '~/utils/helpers'

defineProps<{
  website: Website
}>()

const { animateCardHover, animateCardLeave } = useAnimations()

function onHover(e: MouseEvent) {
  animateCardHover(e.currentTarget as HTMLElement)
}

function onLeave(e: MouseEvent) {
  animateCardLeave(e.currentTarget as HTMLElement)
}
</script>
