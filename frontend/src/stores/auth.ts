import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { api, getToken, setToken } from '@/api/client'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(getToken())
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => token.value !== null)

  async function login(email: string, password: string): Promise<void> {
    const result = await api.login(email, password)
    token.value = result.access_token
    setToken(result.access_token)
    await fetchMe()
  }

  async function register(email: string, password: string): Promise<void> {
    await api.register(email, password)
    await login(email, password)
  }

  async function fetchMe(): Promise<void> {
    user.value = await api.me()
  }

  function logout(): void {
    token.value = null
    user.value = null
    setToken(null)
  }

  return { token, user, isAuthenticated, login, register, fetchMe, logout }
})
