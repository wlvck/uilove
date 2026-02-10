<template>
  <header class="h-16 bg-bg-secondary border-b border-border flex items-center justify-between px-6">
    <!-- Breadcrumb -->
    <div class="flex items-center gap-2 text-sm">
      <span class="text-text-tertiary">Admin</span>
      <Icon name="ph:caret-right" class="h-4 w-4 text-text-tertiary" />
      <span class="text-text-primary capitalize">{{ currentSection }}</span>
    </div>

    <!-- User -->
    <div class="flex items-center gap-4">
      <span v-if="authStore.user" class="text-sm text-text-secondary">
        {{ authStore.user.email }}
      </span>
      <button
        class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
        @click="handleLogout"
      >
        <Icon name="ph:sign-out" class="h-4 w-4" />
        Logout
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
const route = useRoute()
const authStore = useAuthStore()
const { logout } = useAuth()

const currentSection = computed(() => {
  const path = route.path.replace('/admin/', '').split('/')[0]
  return path || 'dashboard'
})

function handleLogout() {
  logout()
}
</script>
