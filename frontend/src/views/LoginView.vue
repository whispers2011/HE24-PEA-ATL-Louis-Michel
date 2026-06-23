<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { ApiError } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { isValidEmail, isValidPassword } from '@/utils/validation'

const auth = useAuthStore()
const router = useRouter()

const mode = ref<'login' | 'register'>('login')
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

function switchMode(next: 'login' | 'register') {
  mode.value = next
  error.value = ''
}

function validate(): boolean {
  if (!isValidEmail(email.value)) {
    error.value = 'Bitte eine gültige E-Mail-Adresse eingeben.'
    return false
  }
  if (!isValidPassword(password.value)) {
    error.value = 'Das Passwort muss mindestens 8 Zeichen lang sein.'
    return false
  }
  return true
}

async function submit() {
  error.value = ''
  if (!validate()) {
    return
  }
  loading.value = true
  try {
    if (mode.value === 'login') {
      await auth.login(email.value.trim(), password.value)
    } else {
      await auth.register(email.value.trim(), password.value)
    }
    router.push({ name: 'dashboard' })
  } catch (e) {
    error.value = e instanceof ApiError ? e.message : 'Unerwarteter Fehler.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="mx-auto mt-10 max-w-md">
    <div class="mb-8 text-center">
      <div
        class="mx-auto mb-4 grid h-14 w-14 place-items-center rounded-2xl bg-indigo-600 text-2xl text-white shadow-lg shadow-indigo-200"
      >
        ↗
      </div>
      <h1 class="text-2xl font-bold text-slate-900">URL-Shortener</h1>
      <p class="mt-1 text-sm text-slate-500">Kurzlinks verwalten und Klicks auswerten.</p>
    </div>

    <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div class="mb-6 grid grid-cols-2 rounded-lg bg-slate-100 p-1 text-sm font-medium">
        <button
          type="button"
          class="rounded-md py-2 transition"
          :class="mode === 'login' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500'"
          @click="switchMode('login')"
        >
          Anmelden
        </button>
        <button
          type="button"
          class="rounded-md py-2 transition"
          :class="mode === 'register' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500'"
          @click="switchMode('register')"
        >
          Registrieren
        </button>
      </div>

      <form class="space-y-4" novalidate @submit.prevent="submit">
        <div>
          <label class="mb-1 block text-sm font-medium text-slate-700" for="email">E-Mail</label>
          <input
            id="email"
            v-model="email"
            type="email"
            autocomplete="email"
            class="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"
          />
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-slate-700" for="password">
            Passwort
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            autocomplete="current-password"
            class="w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200"
          />
        </div>

        <p v-if="error" class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
          {{ error }}
        </p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full rounded-lg bg-indigo-600 py-2.5 font-medium text-white transition hover:bg-indigo-700 disabled:opacity-60"
        >
          {{ loading ? 'Bitte warten …' : mode === 'login' ? 'Anmelden' : 'Konto erstellen' }}
        </button>
      </form>
    </div>
  </div>
</template>
