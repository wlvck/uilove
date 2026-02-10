<template>
  <header class="sticky top-0 z-50 border-b border-border bg-bg/80 backdrop-blur-xl">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center gap-2">
          <div class="h-8 w-8 rounded-lg bg-accent flex items-center justify-center">
            <Icon name="ph:heart-fill" class="h-4 w-4 text-white" />
          </div>
          <span class="text-lg font-semibold text-text-primary">UILove</span>
        </NuxtLink>

        <!-- Desktop Nav -->
        <nav class="hidden md:flex items-center gap-6">
          <NuxtLink
            to="/"
            class="text-sm text-text-secondary hover:text-text-primary transition-colors"
            active-class="text-text-primary"
          >
            Explore
          </NuxtLink>
          <NuxtLink
            to="/categories"
            class="text-sm text-text-secondary hover:text-text-primary transition-colors"
            active-class="text-text-primary"
          >
            Categories
          </NuxtLink>
        </nav>

        <!-- Actions -->
        <div class="flex items-center gap-2">
          <!-- Search Toggle -->
          <button
            class="p-2 rounded-lg text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
            @click="filtersStore.toggleSearch()"
          >
            <Icon name="ph:magnifying-glass" class="h-5 w-5" />
          </button>

          <!-- Mobile Menu Toggle -->
          <button
            class="p-2 rounded-lg text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors md:hidden"
            @click="filtersStore.toggleMobileMenu()"
          >
            <Icon name="ph:list" class="h-5 w-5" />
          </button>
        </div>
      </div>

      <!-- Search Bar (Expandable) -->
      <Transition
        enter-active-class="transition-all duration-300 ease-out"
        leave-active-class="transition-all duration-200 ease-in"
        enter-from-class="opacity-0 -translate-y-2 max-h-0"
        enter-to-class="opacity-100 translate-y-0 max-h-16"
        leave-from-class="opacity-100 translate-y-0 max-h-16"
        leave-to-class="opacity-0 -translate-y-2 max-h-0"
      >
        <div v-if="filtersStore.searchOpen" class="pb-4 overflow-hidden">
          <FilterSearchInput
            :model-value="searchQuery"
            autofocus
            @update:model-value="onSearch"
            @submit="onSearchSubmit"
          />
        </div>
      </Transition>
    </div>
  </header>
</template>

<script setup lang="ts">
const filtersStore = useFiltersStore()
const router = useRouter()
const searchQuery = ref('')

function onSearch(value: string) {
  searchQuery.value = value
}

function onSearchSubmit() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value.trim() } })
    filtersStore.closeSearch()
    searchQuery.value = ''
  }
}
</script>
