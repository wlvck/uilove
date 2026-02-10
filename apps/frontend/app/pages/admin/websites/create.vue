<template>
  <div>
    <!-- Header -->
    <div class="flex items-center gap-4 mb-6">
      <button
        class="p-2 rounded-lg text-text-tertiary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
        @click="router.back()"
      >
        <Icon name="ph:arrow-left" class="h-5 w-5" />
      </button>
      <h1 class="text-2xl font-bold text-text-primary">Create Website</h1>
    </div>

    <!-- Form -->
    <form class="max-w-2xl space-y-6" @submit.prevent="handleSubmit">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <UiFormField label="Title" :error="errors.title" required>
          <UiInput
            v-model="form.title"
            placeholder="Website title"
            :error="!!errors.title"
            @input="generateSlug"
          />
        </UiFormField>

        <UiFormField label="Slug" :error="errors.slug" required hint="URL-friendly identifier">
          <UiInput
            v-model="form.slug"
            placeholder="website-slug"
            :error="!!errors.slug"
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

      <UiFormField label="Featured">
        <div class="flex items-center gap-3">
          <UiSwitch v-model="form.is_featured" />
          <span class="text-sm text-text-secondary">Show in featured section</span>
        </div>
      </UiFormField>

      <div v-if="submitError" class="p-3 rounded-lg bg-red-500/10 border border-red-500/20">
        <p class="text-sm text-red-400">{{ submitError }}</p>
      </div>

      <div class="flex gap-3 pt-4">
        <UiButton type="submit" :disabled="submitting">
          {{ submitting ? 'Creating...' : 'Create Website' }}
        </UiButton>
        <UiButton variant="secondary" type="button" @click="router.back()">
          Cancel
        </UiButton>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import type { WebsiteCreate, Category, Style, Collection, Platform } from '~/types'

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
})

useSeoMeta({
  title: 'Create Website - Admin - UILove',
})

const router = useRouter()
const { post } = useAdminApi()
const { fetchCategories, fetchStyles, fetchCollections, fetchPlatforms } = useCategories()

const form = reactive<WebsiteCreate>({
  title: '',
  slug: '',
  description: '',
  original_url: '',
  thumbnail_url: '',
  image_url: '',
  is_featured: false,
  platform_id: undefined,
  category_ids: [],
  style_ids: [],
  collection_ids: [],
})

const errors = reactive<Record<string, string>>({})
const submitting = ref(false)
const submitError = ref('')

const categories = ref<Category[]>([])
const styles = ref<Style[]>([])
const collections = ref<Collection[]>([])
const platforms = ref<Platform[]>([])

function generateSlug() {
  if (!form.slug || form.slug === slugify(form.title.slice(0, -1))) {
    form.slug = slugify(form.title)
  }
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

function validate(): boolean {
  errors.title = ''
  errors.slug = ''

  if (!form.title.trim()) {
    errors.title = 'Title is required'
  }
  if (!form.slug.trim()) {
    errors.slug = 'Slug is required'
  } else if (!/^[a-z0-9-]+$/.test(form.slug)) {
    errors.slug = 'Slug can only contain lowercase letters, numbers, and hyphens'
  }

  return !errors.title && !errors.slug
}

async function handleSubmit() {
  submitError.value = ''

  if (!validate()) return

  submitting.value = true
  try {
    const data: WebsiteCreate = {
      title: form.title,
      slug: form.slug,
      description: form.description || null,
      original_url: form.original_url || null,
      thumbnail_url: form.thumbnail_url || null,
      image_url: form.image_url || null,
      is_featured: form.is_featured,
      platform_id: form.platform_id || null,
      category_ids: form.category_ids,
      style_ids: form.style_ids,
      collection_ids: form.collection_ids,
    }

    await post('/websites', data)
    router.push('/admin/websites')
  } catch (e: any) {
    submitError.value = e?.data?.detail || e?.message || 'Failed to create website'
  } finally {
    submitting.value = false
  }
}

// Load taxonomy data
const [categoriesData, stylesData, collectionsData, platformsData] = await Promise.all([
  fetchCategories(),
  fetchStyles(),
  fetchCollections(),
  fetchPlatforms(),
])

categories.value = categoriesData
styles.value = stylesData
collections.value = collectionsData
platforms.value = platformsData
</script>
