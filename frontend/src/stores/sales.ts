import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'
import { useToastStore } from '@/stores/toast'
import type { Sale, SaleItem, Payment } from '@/types/sale'

interface SaleForm {
	customer_id?: number
	subtotal: number
	discount: number
	tax: number
	total: number
	status: string
	items: { product_id: number; quantity: number; unit_price: number; total_price: number }[]
}

export const useSalesStore = defineStore('sales', {
	state: () => ({
		sales: [] as Sale[],
		currentSale: null as Sale | null,
		payments: [] as Payment[],
		loading: false,
		error: null as string | null,
		// Pagination state
		pagination: {
			count: 0,
			next: null as string | null,
			previous: null as string | null,
		},
	}),

	actions: {
		async fetchSales(params: {
			search?: string
			status?: string
			ordering?: string
			page?: string
			business_id?: number | null
		} = {}) {
			this.loading = true
			this.error = null
			try {
				const queryParams = new URLSearchParams()
				if (params.search) queryParams.set('search', params.search)
				if (params.status) queryParams.set('status', params.status)
				if (params.ordering) queryParams.set('ordering', params.ordering)
				if (params.page) queryParams.set('page', params.page)
				if (params.business_id) queryParams.set('business_id', params.business_id.toString())

				const queryString = queryParams.toString()
				const url = `/api/sales/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch sales')
				const data = await response.json()
				this.sales = data.results || data
				this.pagination = {
					count: data.count || data.length,
					next: data.next,
					previous: data.previous,
				}
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
		const toastStore = useToastStore()
		try {
			const response = await apiFetch('/api/sales/', {
				method: 'POST',
				body: JSON.stringify(data),
			})
			if (!response.ok) throw new Error('Failed to create sale')
			const sale = await response.json()
			this.sales.unshift(sale)
			toastStore.success('Venta procesada correctamente')
			return sale
		} catch (e: any) {
			this.error = e.message
			toastStore.error(e.message || 'Error al procesar la venta')
			return null
		} finally {
			this.loading = false
		}
	},

  async updateSale(id: number, data: Partial<SaleForm>): Promise<boolean> {
    this.loading = true
    this.error = null
    const toastStore = useToastStore()
    try {
      const response = await apiFetch(`/api/sales/${id}/`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to update sale')
      const updated = await response.json()
      const index = this.sales.findIndex(s => s.id === id)
      if (index !== -1) this.sales[index] = updated
      toastStore.success('Venta actualizada correctamente')
      return true
    } catch (e: any) {
      this.error = e.message
      toastStore.error(e.message || 'Error al actualizar la venta')
      return false
    } finally {
      this.loading = false
    }
  },

	async deleteSale(id: number) {
		this.loading = true
		this.error = null
		const toastStore = useToastStore()
		try {
			const response = await apiFetch(`/api/sales/${id}/`, {
				method: 'DELETE',
			})
			if (!response.ok) throw new Error('Failed to delete sale')
			this.sales = this.sales.filter(s => s.id !== id)
			toastStore.success('Venta eliminada correctamente')
		} catch (e: any) {
			this.error = e.message
			toastStore.error(e.message || 'Error al eliminar la venta')
		} finally {
			this.loading = false
		}
	},

		async fetchPayments(params: {
			sale?: string
			method?: string
			status?: string
			search?: string
			ordering?: string
			page?: string
			business_id?: number | null
		} = {}) {
			this.loading = true
			this.error = null
			try {
				const queryParams = new URLSearchParams()
				if (params.sale) queryParams.set('sale', params.sale)
				if (params.method) queryParams.set('method', params.method)
				if (params.status) queryParams.set('status', params.status)
				if (params.search) queryParams.set('search', params.search)
				if (params.ordering) queryParams.set('ordering', params.ordering)
				if (params.page) queryParams.set('page', params.page)
				if (params.business_id) queryParams.set('business_id', params.business_id.toString())

				const queryString = queryParams.toString()
				const url = `/api/payments/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch payments')
				const data = await response.json()
				this.payments = data.results || data
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async createPayment(data: { sale: number; method: string; amount: number; reference: string; status: string }) {
			this.loading = true
			this.error = null
			const toastStore = useToastStore()
			try {
				const response = await apiFetch('/api/payments/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to create payment')
				const payment = await response.json()
				this.payments.push(payment)
				toastStore.success('Pago registrado correctamente')
				return payment
			} catch (e: any) {
				this.error = e.message
				toastStore.error(e.message || 'Error al registrar pago')
				return null
			} finally {
				this.loading = false
			}
		},

		async fetchPaymentById(id: number) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/payments/${id}/`)
				if (!response.ok) throw new Error('Failed to fetch payment')
				return await response.json()
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
			const today = new Date().toISOString().split('T')[0] as string
			return state.sales.filter(s => {
				const createdAt = s.created_at as string | undefined
				return createdAt ? createdAt.startsWith(today) : false
			})
		},
		todayTotal: (state) => {
			const today = new Date().toISOString().split('T')[0] as string
			return state.sales
				.filter(s => {
					const createdAt = s.created_at as string | undefined
					return createdAt ? createdAt.startsWith(today) : false
				})
				.reduce((sum, s) => sum + Number(s.total), 0)
		},
	},
})