<template>
  <div>
    <!-- Loading -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <WebsiteWebsiteSkeleton v-for="i in skeletonCount" :key="i" />
    </div>

    <!-- Empty -->
    <div v-else-if="!websites.length" class="text-center py-20">
      <Icon name="ph:magnifying-glass" class="h-12 w-12 text-text-tertiary mx-auto mb-4" />
      <h3 class="text-lg font-medium text-text-secondary mb-2">No websites found</h3>
      <p class="text-sm text-text-tertiary">Try adjusting your filters or search query.</p>
    </div>

    <!-- Grid -->
    <div v-else ref="gridRef" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <WebsiteWebsiteCard
        v-for="website in websites"
        :key="website.id"
        :website="website"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Website } from '~/types'

const props = withDefaults(defineProps<{
  websites: Website[]
  loading?: boolean
  skeletonCount?: number
}>(), {
  loading: false,
  skeletonCount: 8,
})

const gridRef = ref<HTMLElement>()
const { animateGridEntrance } = useAnimations()

watch(() => props.websites, () => {
  nextTick(() => {
    if (gridRef.value && props.websites.length) {
      animateGridEntrance(gridRef.value)
    }
  })
})
</script>
