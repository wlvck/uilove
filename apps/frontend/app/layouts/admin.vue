<template>
  <div class="min-h-screen flex bg-bg">
    <AdminSidebar />

    <div class="flex-1 flex flex-col min-w-0">
      <AdminHeader />

      <main class="flex-1 p-6 overflow-auto">
        <slot />
      </main>
    </div>
  </div>
</template>
