<template>
  <SelectRoot :model-value="modelValue != null ? String(modelValue) : undefined" @update:model-value="$emit('update:modelValue', $event)">
    <SelectTrigger
      class="w-full flex items-center justify-between px-3 py-2 rounded-lg bg-bg-tertiary border text-sm transition-colors"
      :class="error ? 'border-red-500' : 'border-border focus:border-accent/50 focus:ring-1 focus:ring-accent/50'"
      :disabled="disabled"
    >
      <SelectValue :placeholder="placeholder" />
      <SelectIcon>
        <Icon name="ph:caret-down" class="h-4 w-4 text-text-tertiary" />
      </SelectIcon>
    </SelectTrigger>

    <SelectPortal>
      <SelectContent
        class="bg-bg-secondary border border-border rounded-lg shadow-xl overflow-hidden z-50"
        position="popper"
        :side-offset="4"
      >
        <SelectViewport class="p-1">
          <SelectItem
            v-for="option in options"
            :key="getOptionValue(option)"
            :value="getOptionValue(option)"
            class="flex items-center px-3 py-2 text-sm rounded-md cursor-pointer outline-none text-text-secondary hover:text-text-primary hover:bg-bg-tertiary data-[highlighted]:bg-bg-tertiary data-[highlighted]:text-text-primary"
          >
            <SelectItemText>{{ getOptionLabel(option) }}</SelectItemText>
            <SelectItemIndicator class="ml-auto">
              <Icon name="ph:check" class="h-4 w-4 text-accent" />
            </SelectItemIndicator>
          </SelectItem>
        </SelectViewport>
      </SelectContent>
    </SelectPortal>
  </SelectRoot>
</template>

<script setup lang="ts">
import {
  SelectRoot,
  SelectTrigger,
  SelectValue,
  SelectIcon,
  SelectPortal,
  SelectContent,
  SelectViewport,
  SelectItem,
  SelectItemText,
  SelectItemIndicator,
} from 'radix-vue'

const props = withDefaults(defineProps<{
  modelValue: string | number | undefined
  options: Array<Record<string, any>>
  labelKey?: string
  valueKey?: string
  placeholder?: string
  disabled?: boolean
  error?: boolean
}>(), {
  labelKey: 'title',
  valueKey: 'id',
  placeholder: 'Select...',
  disabled: false,
  error: false,
})

defineEmits<{
  'update:modelValue': [value: string | number]
}>()

function getOptionLabel(option: Record<string, any>): string {
  return String(option[props.labelKey])
}

function getOptionValue(option: Record<string, any>): string {
  return String(option[props.valueKey])
}
</script>
