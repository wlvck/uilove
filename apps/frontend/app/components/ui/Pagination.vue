<template>
  <nav v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-8">
    <button
      :disabled="currentPage <= 1"
      class="px-3 py-2 rounded-lg text-sm font-medium text-text-secondary hover:text-text-primary hover:bg-bg-tertiary disabled:opacity-40 disabled:pointer-events-none transition-colors"
      @click="$emit('update:currentPage', currentPage - 1)"
    >
      <Icon name="ph:caret-left-bold" class="w-4 h-4" />
    </button>

    <template v-for="page in visiblePages" :key="page">
      <span v-if="page === '...'" class="px-2 text-text-tertiary">...</span>
      <button
        v-else
        :class="[
          'px-3 py-2 rounded-lg text-sm font-medium transition-colors',
          page === currentPage
            ? 'bg-accent text-white'
            : 'text-text-secondary hover:text-text-primary hover:bg-bg-tertiary',
        ]"
        @click="$emit('update:currentPage', page as number)"
      >
        {{ page }}
      </button>
    </template>

    <button
      :disabled="currentPage >= totalPages"
      class="px-3 py-2 rounded-lg text-sm font-medium text-text-secondary hover:text-text-primary hover:bg-bg-tertiary disabled:opacity-40 disabled:pointer-events-none transition-colors"
      @click="$emit('update:currentPage', currentPage + 1)"
    >
      <Icon name="ph:caret-right-bold" class="w-4 h-4" />
    </button>
  </nav>
</template>

<script setup lang="ts">
const props = defineProps<{
  currentPage: number
  totalPages: number
}>()

defineEmits<{
  'update:currentPage': [page: number]
}>()

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  const total = props.totalPages
  const current = props.currentPage

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
    return pages
  }

  pages.push(1)

  if (current > 3) pages.push('...')

  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)

  for (let i = start; i <= end; i++) pages.push(i)

  if (current < total - 2) pages.push('...')

  pages.push(total)

  return pages
})
</script>
