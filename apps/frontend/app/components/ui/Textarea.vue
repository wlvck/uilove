<template>
  <textarea
    :value="modelValue"
    :placeholder="placeholder"
    :rows="rows"
    :disabled="disabled"
    class="w-full px-3 py-2 rounded-lg bg-bg-tertiary border text-sm text-text-primary placeholder-text-tertiary focus:outline-none focus:ring-1 transition-colors disabled:opacity-50 disabled:cursor-not-allowed resize-none"
    :class="error ? 'border-red-500 focus:border-red-500 focus:ring-red-500/50' : 'border-border focus:border-accent/50 focus:ring-accent/50'"
    @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
  />
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  modelValue: string
  placeholder?: string
  rows?: number
  disabled?: boolean
  error?: boolean
}>(), {
  placeholder: '',
  rows: 4,
  disabled: false,
  error: false,
})

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>
