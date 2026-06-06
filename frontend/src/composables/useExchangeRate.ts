import { ref, onMounted } from 'vue'
import { apiFetch } from '@/utils/helpers'

const exchangeRate = ref(500)
const exchangeSource = ref('fallback')

export function useExchangeRate() {
  const fetchRate = async () => {
    try {
      const response = await apiFetch('/api/exchange-rate/')
      if (response.ok) {
        const data = await response.json()
        exchangeRate.value = data.rate || 500
        exchangeSource.value = data.source || 'fallback'
      }
    } catch {
      exchangeRate.value = 500
      exchangeSource.value = 'fallback'
    }
  }

  onMounted(fetchRate)

  return { exchangeRate, exchangeSource, refetch: fetchRate }
}
