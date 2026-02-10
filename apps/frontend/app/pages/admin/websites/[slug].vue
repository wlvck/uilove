<template>
  <div>
    <!-- Loading -->
    <UiLoadingSpinner v-if="loading" />

    <!-- Error -->
    <div v-else-if="loadError" class="text-center py-12">
      <Icon name="ph:warning" class="h-12 w-12 text-text-tertiary mx-auto mb-4" />
      <p class="text-text-secondary mb-4">{{ loadError }}</p>
      <UiButton variant="secondary" @click="router.back()">
        Go back
      </UiButton>
    </div>

    <!-- Form -->
    <template v-else>
      <!-- Header -->
      <div class="flex items-center gap-4 mb-6">
        <button
          class="p-2 rounded-lg text-text-tertiary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
          @click="router.back()"
        >
          <Icon name="ph:arrow-left" class="h-5 w-5" />
        </button>
        <h1 class="text-2xl font-bold text-text-primary">Edit Website</h1>
      </div>

      <form class="max-w-2xl space-y-6" @submit.prevent="handleSubmit">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <UiFormField label="Title" :error="errors.title" required>
            <UiInput
              v-model="form.title"
              placeholder="Website title"
              :error="!!errors.title"
            />
          </UiFormField>

          <UiFormField label="Slug" hint="Cannot be changed">
            <UiInput
              :model-value="slug"
              disabled
            />
          </UiFormField>
        </div>

        <UiFormField label="Description">
          <UiTextarea
            v-model="form.description"
            placeholder="Brief description of the website..."
            :rows="3"
          />
        </UiFormField>

        <UiFormField label="Original URL" hint="Link to the live website">
          <UiInput
            v-model="form.original_url"
            type="url"
            placeholder="https://example.com"
          />
        </UiFormField>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <UiFormField label="Thumbnail URL">
            <UiInput
              v-model="form.thumbnail_url"
              type="url"
              placeholder="https://..."
            />
          </UiFormField>

          <UiFormField label="Full Image URL">
            <UiInput
              v-model="form.image_url"
              type="url"
              placeholder="https://..."
            />
          </UiFormField>
        </div>

        <UiFormField label="Platform">
          <UiSelect
            v-model="form.platform_id"
            :options="platforms"
            placeholder="Select platform..."
          />
        </UiFormField>

        <UiFormField label="Categories">
          <UiMultiSelect
            v-model="form.category_ids"
            :options="categories"
            placeholder="Select categories..."
          />
        </UiFormField>

        <UiFormField label="Styles">
          <UiMultiSelect
            v-model="form.style_ids"
            :options="styles"
            placeholder="Select styles..."
          />
        </UiFormField>

        <UiFormField label="Collections">
          <UiMultiSelect
            v-model="form.collection_ids"
            :options="collections"
            placeholder="Select collections..."
          />
        </UiFormField>

        <div class="flex gap-6">
          <UiFormField label="Featured">
            <div class="flex items-center gap-3">
              <UiSwitch v-model="form.is_featured" />
              <span class="text-sm text-text-secondary">Show in featured section</span>
            </div>
          </UiFormField>

          <UiFormField label="Active">
            <div class="flex items-center gap-3">
              <UiSwitch v-model="form.is_active" />
              <span class="text-sm text-text-secondary">Website is visible</span>
            </div>
          </UiFormField>
        </div>

        <div v-if="submitError" class="p-3 rounded-lg bg-red-500/10 border border-red-500/20">
          <p class="text-sm text-red-400">{{ submitError }}</p>
        </div>

        <div class="flex gap-3 pt-4">
          <UiButton type="submit" :disabled="submitting">
            {{ submitting ? 'Saving...' : 'Save Changes' }}
          </UiButton>
          <UiButton variant="secondary" type="button" @click="router.back()">
            Cancel
          </UiButton>
        </div>
      </form>
    </template>
  </div>
</template>

<script setup lang="ts">
import type { Website, WebsiteUpdate, Category, Style, Collection, Platform } from '~/types'

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
})

const route = useRoute()
const router = useRouter()
const slug = route.params.slug as string
const { authGet, put } = useAdminApi()
const { fetchCategories, fetchStyles, fetchCollections, fetchPlatforms } = useCategories()

useSeoMeta({
  title: 'Edit Website - Admin - UILove',
})

const loading = ref(true)
const loadError = ref('')

const form = reactive({
  title: '',
  description: '',
  original_url: '',
  thumbnail_url: '',
  image_url: '',
  is_featured: false,
  is_active: true,
  platform_id: undefined as number | undefined,
  category_ids: [] as number[],
  style_ids: [] as number[],
  collection_ids: [] as number[],
})

const errors = reactive<Record<string, string>>({})
const submitting = ref(false)
const submitError = ref('')

const categories = ref<Category[]>([])
const styles = ref<Style[]>([])
const collections = ref<Collection[]>([])
const platforms = ref<Platform[]>([])

function validate(): boolean {
  errors.title = ''

  if (!form.title.trim()) {
    errors.title = 'Title is required'
  }

  return !errors.title
}

async function handleSubmit() {
  submitError.value = ''

  if (!validate()) return

  submitting.value = true
  try {
    const data: WebsiteUpdate = {
      title: form.title,
      description: form.description || null,
      original_url: form.original_url || null,
      thumbnail_url: form.thumbnail_url || null,
      image_url: form.image_url || null,
      is_featured: form.is_featured,
      is_active: form.is_active,
      platform_id: form.platform_id || null,
      category_ids: form.category_ids,
      style_ids: form.style_ids,
      collection_ids: form.collection_ids,
    }

    await put(`/websites/${slug}`, data)
    router.push('/admin/websites')
  } catch (e: any) {
    submitError.value = e?.data?.detail || e?.message || 'Failed to update website'
  } finally {
    submitting.value = false
  }
}

// Load data
try {
  const [website, categoriesData, stylesData, collectionsData, platformsData] = await Promise.all([
    authGet<Website>(`/websites/${slug}`),
    fetchCategories(),
    fetchStyles(),
    fetchCollections(),
    fetchPlatforms(),
  ])

  // Populate form
  form.title = website.title
  form.description = website.description || ''
  form.original_url = website.original_url || ''
  form.thumbnail_url = website.thumbnail_url || ''
  form.image_url = website.image_url || ''
  form.is_featured = website.is_featured
  form.is_active = true // Default, might need to fetch from API if available
  form.platform_id = website.platform?.id
  form.category_ids = website.categories?.map(c => c.id) || []
  form.style_ids = website.styles?.map(s => s.id) || []
  form.collection_ids = website.collections?.map(c => c.id) || []

  categories.value = categoriesData
  styles.value = stylesData
  collections.value = collectionsData
  platforms.value = platformsData
} catch (e: any) {
  loadError.value = e?.data?.detail || e?.message || 'Failed to load website'
} finally {
  loading.value = false
}
</script>
