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

    <!-- Loading -->
    <UiLoadingSpinner v-if="loading" size="lg" />

    <!-- Error -->
    <div v-else-if="error" class="text-center py-20">
      <Icon name="ph:warning" class="h-12 w-12 text-text-tertiary mx-auto mb-4" />
      <h2 class="text-lg font-medium text-text-secondary mb-2">Website not found</h2>
      <p class="text-sm text-text-tertiary mb-6">{{ error }}</p>
      <NuxtLink to="/">
        <UiButton>Go home</UiButton>
      </NuxtLink>
    </div>

    <!-- Detail -->
    <template v-else-if="website">
      <WebsiteWebsiteDetail :website="website" />

      <!-- Related -->
      <section v-if="related.length" class="mt-16">
        <h2 class="text-lg font-semibold text-text-primary mb-6">Related Websites</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <WebsiteWebsiteCard
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

const website = ref<Website | null>(null)
const related = ref<Website[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

useSeoMeta({
  title: () => website.value ? `${website.value.title} - UILove` : 'UILove',
})

try {
  const data = await fetchWebsite(slug)
  website.value = data

  if (data.categories.length) {
    const res = await fetchWebsites({ category: data.categories[0].slug })
    related.value = res.data.filter(w => w.slug !== slug).slice(0, 3)
  }
} catch (e: any) {
  error.value = e?.message || 'Failed to load website'
} finally {
  loading.value = false
}
</script>
