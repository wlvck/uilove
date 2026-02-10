<template>
  <footer class="border-t border-border bg-bg-secondary">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
      <div class="flex flex-col md:flex-row items-center justify-between gap-6">
        <!-- Logo -->
        <div class="flex items-center gap-2">
          <div class="h-7 w-7 rounded-lg bg-accent flex items-center justify-center">
            <Icon name="ph:heart-fill" class="h-3.5 w-3.5 text-white" />
          </div>
          <span class="text-sm font-semibold text-text-primary">UILove</span>
        </div>

        <!-- Links -->
        <nav class="flex items-center gap-6">
          <NuxtLink to="/" class="text-sm text-text-tertiary hover:text-text-secondary transition-colors">
            Explore
          </NuxtLink>
          <NuxtLink to="/categories" class="text-sm text-text-tertiary hover:text-text-secondary transition-colors">
            Categories
          </NuxtLink>
        </nav>

        <!-- Copyright -->
        <p class="text-sm text-text-tertiary">
          &copy; {{ new Date().getFullYear() }} UILove
        </p>
      </div>
    </div>
  </footer>
</template>
