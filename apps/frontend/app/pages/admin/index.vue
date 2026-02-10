<template>
  <div />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'auth',
})

// Redirect to websites page
navigateTo('/admin/websites', { replace: true })
</script>
