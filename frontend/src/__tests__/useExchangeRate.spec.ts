import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('@/utils/helpers', () => ({
  apiFetch: vi.fn(),
}))

import { apiFetch } from '@/utils/helpers'
import { useExchangeRate } from '@/composables/useExchangeRate'

describe('useExchangeRate', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('returns default rate of 500 before fetch', () => {
    const { exchangeRate } = useExchangeRate()
    expect(exchangeRate.value).toBe(500)
  })

  it('fetches exchange rate from API', async () => {
    const mockResponse = {
      ok: true,
      json: async () => ({ rate: 36.5, source: 'BCV', currency: 'USD' }),
    }
    vi.mocked(apiFetch).mockResolvedValue(mockResponse as Response)

    const { exchangeRate, exchangeSource, refetch } = useExchangeRate()
    await refetch()

    expect(exchangeRate.value).toBe(36.5)
    expect(exchangeSource.value).toBe('BCV')
  })

  it('falls back to 500 on API error', async () => {
    vi.mocked(apiFetch).mockRejectedValue(new Error('Network error'))

    const { exchangeRate, refetch } = useExchangeRate()
    await refetch()

    expect(exchangeRate.value).toBe(500)
  })

  it('falls back to 500 when response not ok', async () => {
    const mockResponse = { ok: false, status: 500 }
    vi.mocked(apiFetch).mockResolvedValue(mockResponse as Response)

    const { exchangeRate, refetch } = useExchangeRate()
    await refetch()

    expect(exchangeRate.value).toBe(500)
  })
})
