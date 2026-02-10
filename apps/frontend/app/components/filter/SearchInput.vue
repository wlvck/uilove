<template>
  <div class="relative">
    <Icon
      name="ph:magnifying-glass"
      class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-tertiary"
    />
    <input
      :value="modelValue"
      type="text"
      :placeholder="placeholder"
      class="w-full pl-10 pr-4 py-2.5 rounded-lg bg-bg-tertiary border border-border text-sm text-text-primary placeholder-text-tertiary focus:outline-none focus:border-accent/50 focus:ring-1 focus:ring-accent/50 transition-colors"
      :autofocus="autofocus"
      @input="onInput"
      @keydown.enter="$emit('submit')"
    />
    <button
      v-if="modelValue"
      class="absolute right-3 top-1/2 -translate-y-1/2 text-text-tertiary hover:text-text-secondary transition-colors"
      @click="$emit('update:modelValue', '')"
    >
      <Icon name="ph:x" class="h-4 w-4" />
    </button>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  modelValue: string
  placeholder?: string
  autofocus?: boolean
}>(), {
  placeholder: 'Search websites...',
  autofocus: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  submit: []
}>()

function onInput(e: Event) {
  emit('update:modelValue', (e.target as HTMLInputElement).value)
}
</script>
