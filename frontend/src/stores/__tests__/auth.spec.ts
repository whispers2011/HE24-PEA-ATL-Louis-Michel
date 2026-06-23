import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/api/client', () => ({
  api: {
    login: vi.fn().mockResolvedValue({ access_token: 'tok', token_type: 'bearer' }),
    me: vi.fn().mockResolvedValue({ id: 1, email: 'a@example.com', created_at: '2026-01-01' }),
    register: vi.fn().mockResolvedValue({ id: 1, email: 'a@example.com', created_at: '2026-01-01' }),
  },
  getToken: vi.fn().mockReturnValue(null),
  setToken: vi.fn(),
}))

import { useAuthStore } from '@/stores/auth'

describe('auth store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('is unauthenticated before login', () => {
    expect(useAuthStore().isAuthenticated).toBe(false)
  })

  it('login stores the token and loads the user', async () => {
    const auth = useAuthStore()
    await auth.login('a@example.com', 'secret123')
    expect(auth.isAuthenticated).toBe(true)
    expect(auth.token).toBe('tok')
    expect(auth.user?.email).toBe('a@example.com')
  })

  it('logout clears token and user', async () => {
    const auth = useAuthStore()
    await auth.login('a@example.com', 'secret123')
    auth.logout()
    expect(auth.isAuthenticated).toBe(false)
    expect(auth.user).toBeNull()
  })
})
