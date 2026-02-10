<template>
  <div class="min-h-screen flex flex-col bg-bg">
    <LayoutHeader />
    <LayoutMobileMenu />

    <main class="flex-1">
      <slot />
    </main>

    <LayoutFooter />
  </div>
</template>
