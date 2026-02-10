<template>
  <div class="min-h-screen flex items-center justify-center bg-bg px-4">
    <div class="w-full max-w-sm">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="flex items-center justify-center gap-2 mb-2">
          <Icon name="ph:sparkle-fill" class="h-8 w-8 text-accent" />
          <span class="text-2xl font-bold text-text-primary">UILove</span>
        </div>
        <p class="text-sm text-text-secondary">Admin Panel</p>
      </div>

      <!-- Form -->
      <form class="space-y-4" @submit.prevent="handleSubmit">
        <UiFormField label="Email" :error="errors.email">
          <UiInput
            v-model="form.email"
            type="email"
            placeholder="admin@uilove.co"
            :error="!!errors.email"
          />
        </UiFormField>

        <UiFormField label="Password" :error="errors.password">
          <UiInput
            v-model="form.password"
            type="password"
            placeholder="Enter password"
            :error="!!errors.password"
          />
        </UiFormField>

        <div v-if="authStore.error" class="p-3 rounded-lg bg-red-500/10 border border-red-500/20">
          <p class="text-sm text-red-400">{{ authStore.error }}</p>
        </div>

        <UiButton type="submit" class="w-full" :disabled="authStore.loading">
          {{ authStore.loading ? 'Signing in...' : 'Sign in' }}
        </UiButton>
      </form>

      <!-- Back link -->
      <div class="mt-6 text-center">
        <NuxtLink to="/" class="text-sm text-text-tertiary hover:text-text-secondary transition-colors">
          &larr; Back to site
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false,
  middleware: 'auth',
})

useSeoMeta({
  title: 'Admin Login - UILove',
})

const router = useRouter()
const authStore = useAuthStore()
const { login } = useAuth()

const form = reactive({
  email: '',
  password: '',
})

const errors = reactive<Record<string, string>>({})

async function handleSubmit() {
  errors.email = ''
  errors.password = ''

  if (!form.email) {
    errors.email = 'Email is required'
    return
  }
  if (!form.password) {
    errors.password = 'Password is required'
    return
  }

  try {
    await login(form.email, form.password)
    router.push('/admin/websites')
  } catch {
    // Error is handled in authStore
  }
}
</script>
