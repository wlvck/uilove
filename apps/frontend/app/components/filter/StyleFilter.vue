<template>
  <div class="flex items-center gap-2 flex-wrap">
    <button
      v-for="style in styles"
      :key="style.slug"
      :class="[
        'px-3 py-1.5 rounded-full text-sm font-medium border transition-colors',
        selected === style.slug
          ? 'border-accent text-accent-light bg-accent/10'
          : 'border-border text-text-secondary hover:text-text-primary hover:border-border-hover',
      ]"
      @click="$emit('update:selected', selected === style.slug ? undefined : style.slug)"
    >
      {{ style.title }}
    </button>
  </div>
</template>

<script setup lang="ts">
import type { Style } from '~/types'

defineProps<{
  styles: Style[]
  selected?: string
}>()

defineEmits<{
  'update:selected': [value: string | undefined]
}>()
</script>
