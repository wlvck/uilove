<template>
  <button
    :class="[
      'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-accent/50 disabled:opacity-50 disabled:pointer-events-none',
      variants[variant],
      sizes[size],
    ]"
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  variant?: 'primary' | 'secondary' | 'ghost' | 'outline'
  size?: 'sm' | 'md' | 'lg'
}>(), {
  variant: 'primary',
  size: 'md',
})

const variants: Record<string, string> = {
  primary: 'bg-accent hover:bg-accent-hover text-white',
  secondary: 'bg-bg-tertiary hover:bg-bg-card-hover text-text-primary',
  ghost: 'hover:bg-bg-tertiary text-text-secondary hover:text-text-primary',
  outline: 'border border-border hover:border-border-hover text-text-secondary hover:text-text-primary',
}

const sizes: Record<string, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base',
}
</script>
