<template>
  <span
    :class="[
      'inline-flex items-center rounded-full font-medium transition-colors',
      variants[variant],
      sizes[size],
    ]"
  >
    <slot />
  </span>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  variant?: 'default' | 'accent' | 'outline'
  size?: 'sm' | 'md'
}>(), {
  variant: 'default',
  size: 'sm',
})

const variants: Record<string, string> = {
  default: 'bg-bg-tertiary text-text-secondary',
  accent: 'bg-accent/10 text-accent-light',
  outline: 'border border-border text-text-secondary',
}

const sizes: Record<string, string> = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-3 py-1 text-sm',
}
</script>
