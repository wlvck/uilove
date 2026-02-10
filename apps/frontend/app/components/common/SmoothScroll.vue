<template>
  <div>
    <slot />
  </div>
</template>

<script setup lang="ts">
const { init, destroy } = useSmoothScroll()

onMounted(() => {
  init()
})

onBeforeUnmount(() => {
  destroy()
})
</script>
