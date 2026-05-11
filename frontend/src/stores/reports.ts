import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'

interface ReportSummary {
	business_id: number
	business_name: string
	total_sales: number
	total_purchases: number
	total_products: number
	low_stock_count: number
}

interface SalesReport {
	total_sales: number
	count: number
	average_sale: number
}

interface InventoryReport {
	total_products: number
	total_value: number
	low_stock_count: number
	out_of_stock_count: number
}

export const useReportsStore = defineStore('reports', {
	state: () => ({
		summary: [] as ReportSummary[],
		sales: null as SalesReport | null,
		inventory: null as InventoryReport | null,
		loading: false,
		error: null as string | null,
	}),

	actions: {
		async fetchSummary() {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/reports/summary/')
				if (!response.ok) throw new Error('Failed to fetch summary')
				this.summary = await response.json()
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async fetchSales(params: { start_date?: string; end_date?: string } = {}) {
			this.loading = true
			this.error = null
			try {
				const queryParams = new URLSearchParams()
				if (params.start_date) queryParams.set('start_date', params.start_date)
				if (params.end_date) queryParams.set('end_date', params.end_date)

				const queryString = queryParams.toString()
				const url = `/api/reports/sales/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch sales')
				this.sales = await response.json()
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async fetchInventory() {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/reports/inventory/')
				if (!response.ok) throw new Error('Failed to fetch inventory')
				this.inventory = await response.json()
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},
	},
})