<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { ApiError } from '@/api/client'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

onMounted(async () => {
  if (auth.isAuthenticated && !auth.user) {
    try {
      await auth.fetchMe()
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        auth.logout()
        router.push({ name: 'login' })
      }
    }
  }
})

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="min-h-full bg-slate-50 text-slate-800">
    <header v-if="auth.isAuthenticated" class="border-b border-slate-200 bg-white">
      <div class="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
        <RouterLink
          to="/dashboard"
          class="flex items-center gap-2 text-lg font-semibold text-indigo-600"
        >
          <span class="grid h-8 w-8 place-items-center rounded-lg bg-indigo-600 text-white">
            ↗
          </span>
          URL-Shortener
        </RouterLink>
        <div class="flex items-center gap-3 text-sm">
          <span class="hidden text-slate-500 sm:inline">{{ auth.user?.email }}</span>
          <button
            type="button"
            class="rounded-md border border-slate-200 px-3 py-1.5 font-medium text-slate-600 transition hover:bg-slate-100"
            @click="logout"
          >
            Abmelden
          </button>
        </div>
      </div>
    </header>

    <main class="mx-auto max-w-4xl px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>
