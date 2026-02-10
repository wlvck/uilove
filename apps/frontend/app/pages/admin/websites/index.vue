<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-text-primary">Websites</h1>
      <NuxtLink to="/admin/websites/create">
        <UiButton>
          <Icon name="ph:plus" class="h-4 w-4 mr-2" />
          Add Website
        </UiButton>
      </NuxtLink>
    </div>

    <!-- Search -->
    <div class="mb-6">
      <FilterSearchInput
        v-model="search"
        placeholder="Search websites..."
        @submit="loadWebsites"
      />
    </div>

    <!-- Loading -->
    <UiLoadingSpinner v-if="loading" />

    <!-- Table -->
    <div v-else-if="websites.length" class="bg-bg-secondary border border-border rounded-xl overflow-hidden">
      <table class="w-full">
        <thead>
          <tr class="border-b border-border">
            <th class="px-4 py-3 text-left text-xs font-medium text-text-tertiary uppercase tracking-wider">
              Website
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-text-tertiary uppercase tracking-wider">
              Status
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-text-tertiary uppercase tracking-wider">
              Views
            </th>
            <th class="px-4 py-3 text-left text-xs font-medium text-text-tertiary uppercase tracking-wider">
              Created
            </th>
            <th class="px-4 py-3 text-right text-xs font-medium text-text-tertiary uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <tr v-for="website in websites" :key="website.id" class="hover:bg-bg-tertiary/50">
            <td class="px-4 py-3">
              <div class="flex items-center gap-3">
                <div class="h-10 w-16 rounded bg-bg-tertiary overflow-hidden flex-shrink-0">
                  <NuxtImg
                    v-if="website.thumbnail_url"
                    :src="website.thumbnail_url"
                    :alt="website.title"
                    class="h-full w-full object-cover"
                  />
                </div>
                <div class="min-w-0">
                  <p class="text-sm font-medium text-text-primary truncate">{{ website.title }}</p>
                  <p class="text-xs text-text-tertiary truncate">{{ website.slug }}</p>
                </div>
              </div>
            </td>
            <td class="px-4 py-3">
              <UiBadge v-if="website.is_featured" variant="accent" size="sm">Featured</UiBadge>
              <UiBadge v-else size="sm">Normal</UiBadge>
            </td>
            <td class="px-4 py-3 text-sm text-text-secondary">
              {{ website.view_count }}
            </td>
            <td class="px-4 py-3 text-sm text-text-tertiary">
              {{ formatDate(website.created_at) }}
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center justify-end gap-2">
                <NuxtLink :to="`/admin/websites/${website.slug}`">
                  <button class="p-1.5 rounded-lg text-text-tertiary hover:text-text-primary hover:bg-bg-tertiary transition-colors">
                    <Icon name="ph:pencil" class="h-4 w-4" />
                  </button>
                </NuxtLink>
                <button
                  class="p-1.5 rounded-lg text-text-tertiary hover:text-red-400 hover:bg-red-500/10 transition-colors"
                  @click="confirmDelete(website)"
                >
                  <Icon name="ph:trash" class="h-4 w-4" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty state -->
    <div v-else class="text-center py-12">
      <Icon name="ph:globe" class="h-12 w-12 text-text-tertiary mx-auto mb-4" />
      <p class="text-text-secondary">No websites found</p>
    </div>

    <!-- Pagination -->
    <div v-if="meta && meta.pages > 1" class="mt-6">
      <UiPagination
        :current-page="page"
        :total-pages="meta.pages"
        @update:current-page="onPageChange"
      />
    </div>

    <!-- Delete confirmation modal -->
    <UiModal
      :open="deleteModal.open"
      title="Delete Website"
      description="Are you sure you want to delete this website? This action cannot be undone."
      @update:open="deleteModal.open = $event"
    >
      <div class="flex justify-end gap-3 mt-4">
        <UiButton variant="secondary" @click="deleteModal.open = false">
          Cancel
        </UiButton>
        <UiButton variant="primary" class="bg-red-500 hover:bg-red-600" @click="handleDelete">
          Delete
        </UiButton>
      </div>
    </UiModal>
  </div>
</template>

<script setup lang="ts">
import type { Website, PaginationMeta } from '~/types'
import { formatDate } from '~/utils/helpers'

definePageMeta({
  layout: 'admin',
  middleware: 'auth',
})

useSeoMeta({
  title: 'Websites - Admin - UILove',
})

const { authGetPaginated, del } = useAdminApi()

const websites = ref<Website[]>([])
const meta = ref<PaginationMeta | null>(null)
const loading = ref(true)
const search = ref('')
const page = ref(1)

const deleteModal = reactive({
  open: false,
  website: null as Website | null,
})

async function loadWebsites() {
  loading.value = true
  try {
    const response = await authGetPaginated<Website>('/websites', {
      page: page.value,
      size: 20,
      q: search.value || undefined,
    })
    websites.value = response.items
    meta.value = { page: response.page, size: response.size, total: response.total, pages: response.pages }
  } catch (e) {
    console.error('Failed to load websites:', e)
  } finally {
    loading.value = false
  }
}

function onPageChange(newPage: number) {
  page.value = newPage
  loadWebsites()
}

function confirmDelete(website: Website) {
  deleteModal.website = website
  deleteModal.open = true
}

async function handleDelete() {
  if (!deleteModal.website) return

  try {
    await del(`/websites/${deleteModal.website.slug}`)
    deleteModal.open = false
    deleteModal.website = null
    await loadWebsites()
  } catch (e) {
    console.error('Failed to delete website:', e)
  }
}

await loadWebsites()
</script>
