export interface User {
  id: number
  email: string
  created_at: string
}

export interface Link {
  code: string
  target_url: string
  short_url: string
  created_at: string
}

export interface Stats {
  code: string
  total: number
  per_day: Record<string, number>
}

export interface Token {
  access_token: string
  token_type: string
}
