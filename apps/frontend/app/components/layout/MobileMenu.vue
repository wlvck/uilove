<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-300"
      leave-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div v-if="filtersStore.mobileMenuOpen" class="fixed inset-0 z-50">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/60" @click="filtersStore.closeMobileMenu()" />

        <!-- Panel -->
        <div class="absolute inset-y-0 right-0 w-72 bg-bg-secondary border-l border-border overflow-y-auto">
          <div class="p-4">
            <!-- Close -->
            <div class="flex items-center justify-between mb-6">
              <span class="text-sm font-semibold text-text-primary">Menu</span>
              <button
                class="p-2 rounded-lg text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
                @click="filtersStore.closeMobileMenu()"
              >
                <Icon name="ph:x" class="h-5 w-5" />
              </button>
            </div>

            <!-- Navigation -->
            <nav class="space-y-1 mb-6">
              <NuxtLink
                to="/"
                class="block px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
                @click="filtersStore.closeMobileMenu()"
              >
                Explore
              </NuxtLink>
              <NuxtLink
                to="/categories"
                class="block px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
                @click="filtersStore.closeMobileMenu()"
              >
                Categories
              </NuxtLink>
            </nav>

            <!-- Categories -->
            <div v-if="categories.length" class="mb-6">
              <h3 class="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-3 px-3">Categories</h3>
              <ul class="space-y-1">
                <li v-for="category in categories" :key="category.slug">
                  <NuxtLink
                    :to="`/categories/${category.slug}`"
                    class="block px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
                    @click="filtersStore.closeMobileMenu()"
                  >
                    {{ category.title }}
                  </NuxtLink>
                </li>
              </ul>
            </div>

            <!-- Styles -->
            <div v-if="styles.length">
              <h3 class="text-xs font-semibold uppercase tracking-wider text-text-tertiary mb-3 px-3">Styles</h3>
              <ul class="space-y-1">
                <li v-for="style in styles" :key="style.slug">
                  <NuxtLink
                    :to="`/styles/${style.slug}`"
                    class="block px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors"
                    @click="filtersStore.closeMobileMenu()"
                  >
                    {{ style.title }}
                  </NuxtLink>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
const filtersStore = useFiltersStore()
const categoriesStore = useCategoriesStore()
const { categories, styles } = storeToRefs(categoriesStore)

onMounted(() => {
  categoriesStore.loadAll()
})
</script>
