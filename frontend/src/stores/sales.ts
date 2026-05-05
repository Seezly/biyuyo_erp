import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'

interface SaleItem {
	id: number
	sale: number
	product: number
	quantity: number
	unit_price: number
	total_price: number
}

interface Sale {
	id: number
	business: number
	customer: number
	user: number
	subtotal: number
	discount: number
	tax: number
	total: number
	status: string
	created_at: string
	items?: SaleItem[]
}

interface Payment {
	id: number
	sale: number
	method: string
	amount: number
	reference: string
	status: string
	created_at: string
}

interface SaleForm {
	customer: number
	subtotal: number
	discount: number
	tax: number
	total: number
	items: { product: number; quantity: number; unit_price: number; total_price: number }[]
	payments: { method: string; amount: number; reference: string }[]
}

export const useSalesStore = defineStore('sales', {
	state: () => ({
		sales: [] as Sale[],
		currentSale: null as Sale | null,
		payments: [] as Payment[],
		loading: false,
		error: null as string | null,
	}),

	actions: {
		async fetchSales() {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/sales/')
				if (!response.ok) throw new Error('Failed to fetch sales')
				this.sales = await response.json()
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async fetchSale(id: number) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/sales/${id}/`)
				if (!response.ok) throw new Error('Failed to fetch sale')
				this.currentSale = await response.json()
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async createSale(data: SaleForm) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/sales/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to create sale')
				const sale = await response.json()
				this.sales.unshift(sale)
				return sale
			} catch (e: any) {
				this.error = e.message
				return null
			} finally {
				this.loading = false
			}
		},

		async updateSale(id: number, data: Partial<SaleForm>) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/sales/${id}/`, {
					method: 'PATCH',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to update sale')
				const updated = await response.json()
				const index = this.sales.findIndex(s => s.id === id)
				if (index !== -1) this.sales[index] = updated
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async deleteSale(id: number) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/sales/${id}/`, {
					method: 'DELETE',
				})
				if (!response.ok) throw new Error('Failed to delete sale')
				this.sales = this.sales.filter(s => s.id !== id)
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async fetchPayments(saleId?: number) {
			this.loading = true
			this.error = null
			try {
				const url = saleId 
					? `/api/payments/?sale=${saleId}`
					: '/api/payments/'
				const response = await apiFetch(url)
				if (!response.ok) throw new Error('Failed to fetch payments')
				this.payments = await response.json()
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async createPayment(data: { sale: number; method: string; amount: number; reference: string }) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/payments/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to create payment')
				const payment = await response.json()
				this.payments.push(payment)
				return payment
			} catch (e: any) {
				this.error = e.message
				return null
			} finally {
				this.loading = false
			}
		},

		clearCurrentSale() {
			this.currentSale = null
		},
	},

	getters: {
		todaySales: (state) => {
			const today = new Date().toISOString().split('T')[0]
			return state.sales.filter(s => s.created_at.startsWith(today))
		},
		todayTotal: (state) => {
			const today = new Date().toISOString().split('T')[0]
			return state.sales
				.filter(s => s.created_at.startsWith(today))
				.reduce((sum, s) => sum + Number(s.total), 0)
		},
	},
})