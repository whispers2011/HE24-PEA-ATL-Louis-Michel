const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const ALIAS_PATTERN = /^[A-Za-z0-9_-]{3,32}$/

export function isValidEmail(value: string): boolean {
  return EMAIL_PATTERN.test(value.trim())
}

export function isValidPassword(value: string): boolean {
  return value.length >= 8
}

/** Akzeptiert nur absolute http/https-URLs (analog zum Open-Redirect-Schutz der API). */
export function isValidHttpUrl(value: string): boolean {
  let url: URL
  try {
    url = new URL(value.trim())
  } catch {
    return false
  }
  return url.protocol === 'http:' || url.protocol === 'https:'
}

/** Wunsch-Alias: 3–32 Zeichen aus Buchstaben, Ziffern, "-" und "_". */
export function isValidAlias(value: string): boolean {
  return ALIAS_PATTERN.test(value)
}
