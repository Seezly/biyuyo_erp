import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'

interface GlobalStats {
  totalBusinesses: number
  totalUsers: number
  totalSales: number
  activeSubscriptions: number
}

interface SalesData {
  total_sales: number
  count: number
  average_sale: number
}

interface InventoryData {
  total_products: number
  total_value: number
  low_stock_count: number
}

export const useReportsStore = defineStore('reports', {
  state: () => ({
    loading: false,
    error: null as string | null,
    stats: null as GlobalStats | null,
    sales: null as SalesData | null,
    inventory: null as InventoryData | null,
  }),

  actions: {
    async fetchGlobalStats() {
      this.loading = true
      this.error = null
      try {
        const response = await apiFetch('/api/reports/global_stats/')
        if (!response.ok) throw new Error('Failed to fetch global stats')
        const data = await response.json()
        this.stats = data
        return data
      } catch (e: any) {
        this.error = e.message
        return null
      } finally {
        this.loading = false
      }
    },

    async fetchSales() {
      this.loading = true
      this.error = null
      try {
        const response = await apiFetch('/api/reports/sales/')
        if (!response.ok) throw new Error('Failed to fetch sales report')
        const data = await response.json()
        this.sales = data
        return data
      } catch (e: any) {
        this.error = e.message
        return null
      } finally {
        this.loading = false
      }
    },

    async fetchInventory() {
      this.loading = true
      this.error = null
      try {
        const response = await apiFetch('/api/reports/inventory/')
        if (!response.ok) throw new Error('Failed to fetch inventory report')
        const data = await response.json()
        this.inventory = data
        return data
      } catch (e: any) {
        this.error = e.message
        return null
      } finally {
        this.loading = false
      }
    },
  },
})