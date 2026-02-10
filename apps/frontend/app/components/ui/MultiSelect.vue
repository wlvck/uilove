<template>
  <div class="relative">
    <!-- Selected items display -->
    <div
      class="min-h-[42px] w-full px-3 py-2 rounded-lg bg-bg-tertiary border text-sm cursor-pointer transition-colors"
      :class="error ? 'border-red-500' : 'border-border focus-within:border-accent/50 focus-within:ring-1 focus-within:ring-accent/50'"
      @click="isOpen = !isOpen"
    >
      <div v-if="selectedOptions.length" class="flex flex-wrap gap-1">
        <span
          v-for="option in selectedOptions"
          :key="getOptionValue(option)"
          class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-accent/10 text-accent-light text-xs"
        >
          {{ getOptionLabel(option) }}
          <button
            type="button"
            class="hover:text-accent"
            @click.stop="removeOption(option)"
          >
            <Icon name="ph:x" class="h-3 w-3" />
          </button>
        </span>
      </div>
      <span v-else class="text-text-tertiary">{{ placeholder }}</span>
    </div>

    <!-- Dropdown -->
    <Transition
      enter-active-class="transition duration-100 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-75 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        class="absolute z-50 mt-1 w-full bg-bg-secondary border border-border rounded-lg shadow-xl overflow-hidden"
      >
        <div class="max-h-60 overflow-auto p-1">
          <button
            v-for="option in options"
            :key="getOptionValue(option)"
            type="button"
            class="w-full flex items-center justify-between px-3 py-2 text-sm rounded-md text-left transition-colors"
            :class="isSelected(option)
              ? 'bg-accent/10 text-accent-light'
              : 'text-text-secondary hover:text-text-primary hover:bg-bg-tertiary'"
            @click="toggleOption(option)"
          >
            {{ getOptionLabel(option) }}
            <Icon v-if="isSelected(option)" name="ph:check" class="h-4 w-4" />
          </button>
        </div>
      </div>
    </Transition>

    <!-- Backdrop -->
    <div
      v-if="isOpen"
      class="fixed inset-0 z-40"
      @click="isOpen = false"
    />
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(defineProps<{
  modelValue: number[]
  options: Array<Record<string, any>>
  labelKey?: string
  valueKey?: string
  placeholder?: string
  error?: boolean
}>(), {
  labelKey: 'title',
  valueKey: 'id',
  placeholder: 'Select...',
  error: false,
})

const emit = defineEmits<{
  'update:modelValue': [value: number[]]
}>()

const isOpen = ref(false)

const selectedOptions = computed(() => {
  return props.options.filter(opt => props.modelValue.includes(opt[props.valueKey]))
})

function getOptionLabel(option: Record<string, any>): string {
  return String(option[props.labelKey])
}

function getOptionValue(option: Record<string, any>): number {
  return option[props.valueKey]
}

function isSelected(option: Record<string, any>): boolean {
  return props.modelValue.includes(getOptionValue(option))
}

function toggleOption(option: Record<string, any>) {
  const value = getOptionValue(option)
  if (isSelected(option)) {
    emit('update:modelValue', props.modelValue.filter(v => v !== value))
  } else {
    emit('update:modelValue', [...props.modelValue, value])
  }
}

function removeOption(option: Record<string, any>) {
  const value = getOptionValue(option)
  emit('update:modelValue', props.modelValue.filter(v => v !== value))
}
</script>
