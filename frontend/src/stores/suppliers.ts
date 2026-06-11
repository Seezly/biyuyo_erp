import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'
import { useToastStore } from '@/stores/toast'
import type { Supplier, Purchase, PurchaseItem } from '@/types/supplier'

interface SupplierForm {
  name: string
  rif: string
  email: string
  address?: string
  phone?: string
}

interface PurchaseForm {
	supplier_id: number
	total: number
	items: { product_id: number; quantity: number; cost_price: number }[]
}

export const useSuppliersStore = defineStore('suppliers', {
	state: () => ({
		suppliers: [] as Supplier[],
		purchases: [] as Purchase[],
		loading: false,
		error: null as string | null,
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
			business_id?: number | null
		} = {}) {
			this.loading = true
			this.error = null
			try {
				const queryParams = new URLSearchParams()
				if (params.search) queryParams.set('search', params.search)
				if (params.ordering) queryParams.set('ordering', params.ordering)
				if (params.page) queryParams.set('page', params.page)
				if (params.business_id) queryParams.set('business_id', params.business_id.toString())

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
		const toastStore = useToastStore()
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
			toastStore.success('Proveedor creado correctamente')
			return supplier
		} catch (e: any) {
			this.error = e.message
			toastStore.error(e.message || 'Error al crear proveedor')
			return null
		} finally {
			this.loading = false
		}
	},

	async updateSupplier(id: number, data: Partial<SupplierForm>) {
		this.loading = true
		this.error = null
		const toastStore = useToastStore()
		try {
			const response = await apiFetch(`/api/suppliers/${id}/`, {
				method: 'PATCH',
				body: JSON.stringify(data),
			})
			if (!response.ok) throw new Error('Failed to update supplier')
			const updated = await response.json()
			const index = this.suppliers.findIndex(s => s.id === id)
			if (index !== -1) this.suppliers[index] = updated
			toastStore.success('Proveedor actualizado correctamente')
			return updated
		} catch (e: any) {
			this.error = e.message
			toastStore.error(e.message || 'Error al actualizar proveedor')
			return null
		} finally {
			this.loading = false
		}
	},

	async deleteSupplier(id: number) {
		this.loading = true
		this.error = null
		const toastStore = useToastStore()
		try {
			const response = await apiFetch(`/api/suppliers/${id}/`, {
				method: 'DELETE',
			})
			if (!response.ok) throw new Error('Failed to delete supplier')
			this.suppliers = this.suppliers.filter(s => s.id !== id)
			toastStore.success('Proveedor eliminado correctamente')
		} catch (e: any) {
			this.error = e.message
			toastStore.error(e.message || 'Error al eliminar proveedor')
		} finally {
			this.loading = false
		}
	},

		async fetchPurchases(params: {
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
	},

	getters: {
		activeSuppliers: (state) => state.suppliers.filter(s => s.is_active),
		supplierById: (state) => (id: number) => state.suppliers.find(s => s.id === id),
	},
})