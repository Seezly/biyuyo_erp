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
	}),

	actions: {
		async fetchSuppliers() {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/suppliers/')
				if (!response.ok) throw new Error('Failed to fetch suppliers')
				this.suppliers = await response.json()
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

		async fetchPurchases() {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/purchases/')
				if (!response.ok) throw new Error('Failed to fetch purchases')
				this.purchases = await response.json()
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