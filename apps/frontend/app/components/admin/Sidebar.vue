<template>
  <aside class="w-64 bg-bg-secondary border-r border-border flex flex-col">
    <!-- Logo -->
    <div class="h-16 flex items-center px-6 border-b border-border">
      <NuxtLink to="/admin" class="flex items-center gap-2">
        <Icon name="ph:sparkle-fill" class="h-6 w-6 text-accent" />
        <span class="text-lg font-semibold text-text-primary">UILove</span>
        <UiBadge variant="accent" size="sm">Admin</UiBadge>
      </NuxtLink>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 p-4 space-y-1">
      <NuxtLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors"
        :class="isActive(item.to)
          ? 'bg-accent/10 text-accent-light'
          : 'text-text-secondary hover:text-text-primary hover:bg-bg-tertiary'"
      >
        <Icon :name="item.icon" class="h-5 w-5" />
        {{ item.label }}
      </NuxtLink>
    </nav>

    <!-- Back to site -->
    <div class="p-4 border-t border-border">
      <NuxtLink
        to="/"
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-text-tertiary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
      >
        <Icon name="ph:arrow-left" class="h-5 w-5" />
        Back to site
      </NuxtLink>
    </div>
  </aside>
</template>

<script setup lang="ts">
const route = useRoute()

const navItems = [
  { to: '/admin/websites', label: 'Websites', icon: 'ph:globe' },
  { to: '/admin/categories', label: 'Categories', icon: 'ph:folders' },
  { to: '/admin/styles', label: 'Styles', icon: 'ph:palette' },
  { to: '/admin/collections', label: 'Collections', icon: 'ph:stack' },
  { to: '/admin/platforms', label: 'Platforms', icon: 'ph:app-window' },
]

function isActive(path: string): boolean {
  return route.path.startsWith(path)
}
</script>
