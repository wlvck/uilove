<template>
  <div v-if="filters.length" class="flex items-center gap-2 flex-wrap">
    <span class="text-xs text-text-tertiary">Active filters:</span>
    <button
      v-for="filter in filters"
      :key="filter.key"
      class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-accent/10 text-accent-light text-xs font-medium hover:bg-accent/20 transition-colors"
      @click="$emit('remove', filter.key)"
    >
      <span class="capitalize">{{ filter.key }}:</span> {{ filter.value }}
      <Icon name="ph:x" class="h-3 w-3" />
    </button>
    <button
      class="text-xs text-text-tertiary hover:text-text-secondary transition-colors"
      @click="$emit('clear')"
    >
      Clear all
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  filters: { key: string; value: string }[]
}>()

defineEmits<{
  remove: [key: string]
  clear: []
}>()
</script>
