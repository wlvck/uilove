<template>
  <div v-if="isReady" class="min-h-screen flex bg-bg">
    <AdminSidebar />

    <div class="flex-1 flex flex-col min-w-0">
      <AdminHeader />

      <main class="flex-1 p-6 overflow-auto">
        <slot />
      </main>
    </div>
  </div>
  <div v-else class="min-h-screen flex items-center justify-center bg-bg">
    <UiLoadingSpinner size="lg" />
  </div>
</template>

<script setup lang="ts">
const authStore = useAuthStore()

// Only show content when authenticated (prevents flash)
const isReady = computed(() => authStore.isAuthenticated)
</script>
