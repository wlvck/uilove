<template>
  <div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-8">
    <!-- Back button -->
    <button
      class="mb-6 inline-flex items-center gap-1.5 text-sm text-text-secondary hover:text-text-primary transition-colors"
      @click="router.back()"
    >
      <Icon name="ph:arrow-left" class="h-4 w-4" />
      Back
    </button>

    <!-- Loading Skeleton -->
    <template v-if="pending">
      <div class="animate-pulse">
        <!-- Image skeleton -->
        <div class="aspect-video bg-bg-tertiary rounded-xl mb-6" />
        <!-- Title skeleton -->
        <div class="h-8 bg-bg-tertiary rounded w-2/3 mb-4" />
        <!-- Description skeleton -->
        <div class="space-y-2 mb-6">
          <div class="h-4 bg-bg-tertiary rounded w-full" />
          <div class="h-4 bg-bg-tertiary rounded w-5/6" />
          <div class="h-4 bg-bg-tertiary rounded w-4/6" />
        </div>
        <!-- Tags skeleton -->
        <div class="flex gap-2">
          <div class="h-6 bg-bg-tertiary rounded-full w-20" />
          <div class="h-6 bg-bg-tertiary rounded-full w-24" />
          <div class="h-6 bg-bg-tertiary rounded-full w-16" />
        </div>
      </div>
    </template>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-20">
      <Icon name="ph:warning" class="h-12 w-12 text-text-tertiary mx-auto mb-4" />
      <h2 class="text-lg font-medium text-text-secondary mb-2">Website not found</h2>
      <p class="text-sm text-text-tertiary mb-6">{{ error.message }}</p>
      <NuxtLink to="/">
        <UiButton>Go home</UiButton>
      </NuxtLink>
    </div>

    <!-- Detail -->
    <template v-else-if="website">
      <WebsiteDetail :website="website" />

      <!-- Related -->
      <section v-if="related.length" class="mt-16">
        <h2 class="text-lg font-semibold text-text-primary mb-6">Related Websites</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <WebsiteCard
            v-for="site in related"
            :key="site.id"
            :website="site"
          />
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import type { Website } from '~/types'

const route = useRoute()
const router = useRouter()
const slug = route.params.slug as string

const { fetchWebsite, fetchWebsites } = useWebsites()

const { data: website, pending, error } = await useLazyAsyncData(
  `website-${slug}`,
  () => fetchWebsite(slug)
)

const related = ref<Website[]>([])

useSeoMeta({
  title: () => website.value ? `${website.value.title} - UILove` : 'UILove',
})

// Fetch related websites when main data loads
watch(website, async (data) => {
  const firstCategory = data?.categories?.[0]
  if (firstCategory) {
    const res = await fetchWebsites({ category: firstCategory.slug })
    related.value = res.items.filter(w => w.slug !== slug).slice(0, 3)
  }
}, { immediate: true })
</script>
