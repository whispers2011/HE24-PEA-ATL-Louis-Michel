<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<template>
  <section class="mx-auto mt-16 max-w-md text-center">
    <p class="text-6xl font-bold text-indigo-600">404</p>
    <h1 class="mt-4 text-2xl font-bold text-slate-900">Seite nicht gefunden</h1>
    <p class="mt-2 text-slate-500">Diese Seite gibt es nicht.</p>
    <RouterLink
      :to="auth.isAuthenticated ? '/dashboard' : '/login'"
      class="mt-6 inline-block rounded-lg bg-indigo-600 px-5 py-2.5 font-medium text-white transition hover:bg-indigo-700"
    >
      {{ auth.isAuthenticated ? 'Zum Dashboard' : 'Zur Anmeldung' }}
    </RouterLink>
  </section>
</template>
