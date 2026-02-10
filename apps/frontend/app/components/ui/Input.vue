<template>
  <input
    :type="type"
    :value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    class="w-full px-3 py-2 rounded-lg bg-bg-tertiary border text-sm text-text-primary placeholder-text-tertiary focus:outline-none focus:ring-1 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
    :class="error ? 'border-red-500 focus:border-red-500 focus:ring-red-500/50' : 'border-border focus:border-accent/50 focus:ring-accent/50'"
    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
  />
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  modelValue: string
  type?: 'text' | 'email' | 'password' | 'url' | 'number'
  placeholder?: string
  disabled?: boolean
  error?: boolean
}>(), {
  type: 'text',
  placeholder: '',
  disabled: false,
  error: false,
})

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>
