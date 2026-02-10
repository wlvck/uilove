<template>
  <div class="space-y-1.5">
    <label v-if="label" class="block text-sm font-medium text-text-primary">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <slot />
    <p v-if="hint && !error" class="text-xs text-text-tertiary">{{ hint }}</p>
    <p v-if="error" class="text-xs text-red-500">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label?: string
  error?: string
  hint?: string
  required?: boolean
}>()
</script>
