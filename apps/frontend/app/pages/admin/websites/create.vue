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

      <UiFormField label="Categories">
        <UiMultiSelect
          v-model="form.category_ids"
          :options="categories"
          placeholder="Select categories..."
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
import type { WebsiteCreate, Category } from '~/types'

interface WebsiteForm {
  title: string
  slug: string
  description: string
  original_url: string
  thumbnail_url: string
  image_url: string
  is_featured: boolean
  category_ids: number[]
}

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
})

useSeoMeta({
  title: 'Create Website - Admin - UILove',
})

const router = useRouter()
const { post } = useAdminApi()
const { fetchCategories } = useCategories()

const form = reactive<WebsiteForm>({
  title: '',
  slug: '',
  description: '',
  original_url: '',
  thumbnail_url: '',
  image_url: '',
  is_featured: false,
  category_ids: [],
})

const errors = reactive<Record<string, string>>({})
const submitting = ref(false)
const submitError = ref('')

const categories = ref<Category[]>([])

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
      category_ids: form.category_ids,
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
const categoriesData = await fetchCategories()
categories.value = categoriesData
</script>
