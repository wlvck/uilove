<template>
  <div class="flex items-center justify-center" :class="containerClass">
    <div
      :class="[
        'animate-spin rounded-full border-2 border-border border-t-accent',
        sizes[size],
      ]"
    />
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  size?: 'sm' | 'md' | 'lg'
  containerClass?: string
}>(), {
  size: 'md',
  containerClass: 'py-12',
})

const sizes: Record<string, string> = {
  sm: 'h-5 w-5',
  md: 'h-8 w-8',
  lg: 'h-12 w-12',
}
</script>
