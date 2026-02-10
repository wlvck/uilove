<template>
  <DialogRoot :open="open" @update:open="$emit('update:open', $event)">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50" />
      <DialogContent
        class="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md bg-bg-secondary border border-border rounded-xl p-6 shadow-xl"
      >
        <DialogTitle class="text-lg font-semibold text-text-primary">
          {{ title }}
        </DialogTitle>
        <DialogDescription v-if="description" class="mt-2 text-sm text-text-secondary">
          {{ description }}
        </DialogDescription>

        <div class="mt-4">
          <slot />
        </div>

        <DialogClose
          class="absolute top-4 right-4 p-1 rounded-lg text-text-tertiary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
        >
          <Icon name="ph:x" class="w-5 h-5" />
        </DialogClose>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<script setup lang="ts">
import {
  DialogRoot,
  DialogPortal,
  DialogOverlay,
  DialogContent,
  DialogTitle,
  DialogDescription,
  DialogClose,
} from 'radix-vue'

defineProps<{
  open: boolean
  title: string
  description?: string
}>()

defineEmits<{
  'update:open': [value: boolean]
}>()
</script>
