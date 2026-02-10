<template>
  <div class="flex items-center gap-2 flex-wrap">
    <button
      :class="[
        'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
        !selected
          ? 'bg-accent text-white'
          : 'bg-bg-tertiary text-text-secondary hover:text-text-primary',
      ]"
      @click="$emit('update:selected', undefined)"
    >
      All
    </button>
    <button
      v-for="category in categories"
      :key="category.slug"
      :class="[
        'px-3 py-1.5 rounded-full text-sm font-medium transition-colors',
        selected === category.slug
          ? 'bg-accent text-white'
          : 'bg-bg-tertiary text-text-secondary hover:text-text-primary',
      ]"
      @click="$emit('update:selected', category.slug)"
    >
      {{ category.title }}
    </button>
  </div>
</template>

<script setup lang="ts">
import type { Category } from '~/types'

defineProps<{
  categories: Category[]
  selected?: string
}>()

defineEmits<{
  'update:selected': [value: string | undefined]
}>()
</script>
