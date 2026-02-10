<template>
  <SwitchRoot
    :checked="modelValue"
    :disabled="disabled"
    class="w-10 h-6 rounded-full relative transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
    :class="modelValue ? 'bg-accent' : 'bg-bg-tertiary border border-border'"
    @update:checked="$emit('update:modelValue', $event)"
  >
    <SwitchThumb
      class="block w-5 h-5 bg-white rounded-full shadow transition-transform"
      :class="modelValue ? 'translate-x-[18px]' : 'translate-x-0.5'"
    />
  </SwitchRoot>
</template>

<script setup lang="ts">
import { SwitchRoot, SwitchThumb } from 'radix-vue'

withDefaults(defineProps<{
  modelValue: boolean
  disabled?: boolean
}>(), {
  disabled: false,
})

defineEmits<{
  'update:modelValue': [value: boolean]
}>()
</script>
