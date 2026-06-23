import type { Link, Stats, Token, User } from '@/types'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const TOKEN_KEY = 'url-shortener-token'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string | null): void {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token)
  } else {
    localStorage.removeItem(TOKEN_KEY)
  }
}

/** Fehler einer API-Antwort mit zugehörigem HTTP-Status. */
export class ApiError extends Error {
  readonly status: number

  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

let unauthorizedHandler: (() => void) | null = null

/** Registriert eine Reaktion auf abgelaufene/ungültige Sitzungen (401). */
export function setUnauthorizedHandler(handler: () => void): void {
  unauthorizedHandler = handler
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers)
  const token = getToken()
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(`${BASE_URL}${path}`, { ...options, headers })
  if (response.status === 204) {
    return undefined as T
  }

  const data: unknown = await response.json().catch(() => null)
  if (!response.ok) {
    // Abgelaufenes Token bei einem geschützten Aufruf: Sitzung global beenden.
    if (response.status === 401 && token !== null) {
      setToken(null)
      unauthorizedHandler?.()
    }
    const detail =
      (data as { detail?: string } | null)?.detail ?? response.statusText
    throw new ApiError(response.status, detail)
  }
  return data as T
}

function jsonBody(payload: unknown): RequestInit {
  return {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  }
}

export const api = {
  register: (email: string, password: string) =>
    request<User>('/api/auth/register', jsonBody({ email, password })),

  login: (email: string, password: string) =>
    request<Token>('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: email, password }),
    }),

  me: () => request<User>('/api/auth/me'),

  listLinks: () => request<Link[]>('/api/links'),

  createLink: (targetUrl: string, alias?: string) =>
    request<Link>(
      '/api/links',
      jsonBody(alias ? { target_url: targetUrl, alias } : { target_url: targetUrl }),
    ),

  deleteLink: (code: string) =>
    request<void>(`/api/links/${encodeURIComponent(code)}`, { method: 'DELETE' }),

  stats: (code: string) =>
    request<Stats>(`/api/links/${encodeURIComponent(code)}/stats`),
}
