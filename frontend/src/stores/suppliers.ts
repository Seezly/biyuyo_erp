import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'

interface Supplier {
	id: number
	name: string
	business: number
	rif: string
	email: string
	address: string
	phone: string
	is_active: boolean
	created_at: string
	updated_at: string
}

interface SupplierForm {
	name: string
	rif: string
	email: string
	address: string
	phone: string
}

interface Purchase {
	id: number
	business: number
	supplier: number
	status: string
	total: number
	created_at: string
	updated_at: string
	items?: PurchaseItem[]
}

interface PurchaseItem {
	id: number
	purchase: number
	product: number
	quantity: number
	cost_price: number
	total_price: number
}

interface PurchaseForm {
	supplier: number
	total: number
	items: { product: number; quantity: number; cost_price: number }[]
}

export const useSuppliersStore = defineStore('suppliers', {
	state: () => ({
		suppliers: [] as Supplier[],
		purchases: [] as Purchase[],
		currentPurchase: null as Purchase | null,
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
		async fetchSuppliers(params: {
			search?: string
			ordering?: string
			page?: string
		} = {}) {
			this.loading = true
			this.error = null
			try {
				const queryParams = new URLSearchParams()
				if (params.search) queryParams.set('search', params.search)
				if (params.ordering) queryParams.set('ordering', params.ordering)
				if (params.page) queryParams.set('page', params.page)

				const queryString = queryParams.toString()
				const url = `/api/suppliers/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch suppliers')
				const data = await response.json()
				this.suppliers = data.results || data
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

		async fetchSupplier(id: number) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/suppliers/${id}/`)
				if (!response.ok) throw new Error('Failed to fetch supplier')
				return await response.json()
			} catch (e: any) {
				this.error = e.message
				return null
			} finally {
				this.loading = false
			}
		},

		async createSupplier(data: SupplierForm) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/suppliers/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) {
					const errorData = await response.json()
					throw new Error(JSON.stringify(errorData))
				}
				const supplier = await response.json()
				this.suppliers.unshift(supplier)
				return supplier
			} catch (e: any) {
				this.error = e.message
				return null
			} finally {
				this.loading = false
			}
		},

		async updateSupplier(id: number, data: Partial<SupplierForm>) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/suppliers/${id}/`, {
					method: 'PATCH',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to update supplier')
				const updated = await response.json()
				const index = this.suppliers.findIndex(s => s.id === id)
				if (index !== -1) this.suppliers[index] = updated
				return updated
			} catch (e: any) {
				this.error = e.message
				return null
			} finally {
				this.loading = false
			}
		},

		async deleteSupplier(id: number) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/suppliers/${id}/`, {
					method: 'DELETE',
				})
				if (!response.ok) throw new Error('Failed to delete supplier')
				this.suppliers = this.suppliers.filter(s => s.id !== id)
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async fetchPurchases(params: {
			search?: string
			status?: string
			ordering?: string
			page?: string
		} = {}) {
			this.loading = true
			this.error = null
			try {
				const queryParams = new URLSearchParams()
				if (params.search) queryParams.set('search', params.search)
				if (params.status) queryParams.set('status', params.status)
				if (params.ordering) queryParams.set('ordering', params.ordering)
				if (params.page) queryParams.set('page', params.page)

				const queryString = queryParams.toString()
				const url = `/api/purchases/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch purchases')
				const data = await response.json()
				this.purchases = data.results || data
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async fetchPurchase(id: number) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/purchases/${id}/`)
				if (!response.ok) throw new Error('Failed to fetch purchase')
				this.currentPurchase = await response.json()
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async createPurchase(data: PurchaseForm) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/purchases/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to create purchase')
				const purchase = await response.json()
				this.purchases.unshift(purchase)
				return purchase
			} catch (e: any) {
				this.error = e.message
				return null
			} finally {
				this.loading = false
			}
		},

		clearCurrentPurchase() {
			this.currentPurchase = null
		},
	},

	getters: {
		activeSuppliers: (state) => state.suppliers.filter(s => s.is_active),
		supplierById: (state) => (id: number) => state.suppliers.find(s => s.id === id),
	},
})