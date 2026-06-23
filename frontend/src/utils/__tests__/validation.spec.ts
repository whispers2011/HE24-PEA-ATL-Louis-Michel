import { describe, expect, it } from 'vitest'

import { isValidAlias, isValidEmail, isValidHttpUrl, isValidPassword } from '@/utils/validation'

describe('validation', () => {
  it('accepts valid e-mail addresses and rejects malformed ones', () => {
    expect(isValidEmail('a@example.com')).toBe(true)
    expect(isValidEmail('no-at-sign')).toBe(false)
    expect(isValidEmail('a@b')).toBe(false)
  })

  it('requires passwords of at least eight characters', () => {
    expect(isValidPassword('secret123')).toBe(true)
    expect(isValidPassword('short')).toBe(false)
  })

  it('accepts only http and https URLs', () => {
    expect(isValidHttpUrl('https://example.com')).toBe(true)
    expect(isValidHttpUrl('http://example.com/path')).toBe(true)
    expect(isValidHttpUrl('ftp://example.com')).toBe(false)
    expect(isValidHttpUrl('javascript:alert(1)')).toBe(false)
    expect(isValidHttpUrl('not-a-url')).toBe(false)
  })

  it('validates the optional alias pattern', () => {
    expect(isValidAlias('my-link_1')).toBe(true)
    expect(isValidAlias('ab')).toBe(false)
    expect(isValidAlias('with space')).toBe(false)
    expect(isValidAlias('a'.repeat(33))).toBe(false)
  })
})
