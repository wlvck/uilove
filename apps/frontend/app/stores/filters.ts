import { defineStore } from 'pinia'

export const useFiltersStore = defineStore('filters', () => {
  const searchQuery = ref('')
  const mobileMenuOpen = ref(false)
  const searchOpen = ref(false)

  function toggleMobileMenu() {
    mobileMenuOpen.value = !mobileMenuOpen.value
  }

  function toggleSearch() {
    searchOpen.value = !searchOpen.value
  }

  function closeMobileMenu() {
    mobileMenuOpen.value = false
  }

  function closeSearch() {
    searchOpen.value = false
  }

  return {
    searchQuery,
    mobileMenuOpen,
    searchOpen,
    toggleMobileMenu,
    toggleSearch,
    closeMobileMenu,
    closeSearch,
  }
})
