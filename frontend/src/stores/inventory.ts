import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'
import type { Product, ProductForm } from '@/types/product'
import { useToastStore } from '@/stores/toast'

interface Category {
	id: number
	name: string
	parent_id: number | null
	business: number
	created_at: string
	updated_at: string
}

interface InventoryMovement {
	id: number
	business: number
	product: number
	type: 'in' | 'out' | 'adjustment'
	quantity: number
	reason: string
	created_at: string
}

export const useInventoryStore = defineStore('inventory', {
	state: () => ({
		products: [] as Product[],
		categories: [] as Category[],
		movements: [] as InventoryMovement[],
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
		async fetchProducts(params: {
			search?: string
			category_id?: string
			stock?: string
			ordering?: string
			page?: string
		} = {}) {
			this.loading = true
			this.error = null
			try {
				// Build query string from params
				const queryParams = new URLSearchParams()
				if (params.search) queryParams.set('search', params.search)
				if (params.category_id) queryParams.set('category_id', params.category_id)
				if (params.stock) queryParams.set('stock', params.stock)
				if (params.ordering) queryParams.set('ordering', params.ordering)
				if (params.page) queryParams.set('page', params.page)

				const queryString = queryParams.toString()
				const url = `/api/products/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch products')
				const data = await response.json()
				this.products = data.results || data
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

	async createProduct(data: ProductForm) {
		this.loading = true
		this.error = null
		const toastStore = useToastStore()
		try {
			const response = await apiFetch('/api/products/', {
				method: 'POST',
				body: JSON.stringify(data),
			})
			if (!response.ok) throw new Error('Failed to create product')
			const product = await response.json()
			this.products.push(product)
			toastStore.success('Producto creado correctamente')
		} catch (e: any) {
			this.error = e.message
			toastStore.error(e.message || 'Error al crear producto')
		} finally {
			this.loading = false
		}
	},

	async updateProduct(id: number, data: Partial<ProductForm>): Promise<Product | null> {
		this.loading = true
		this.error = null
		const toastStore = useToastStore()
		try {
			const response = await apiFetch(`/api/products/${id}/`, {
				method: 'PATCH',
				body: JSON.stringify(data),
			})
			if (!response.ok) throw new Error('Failed to update product')
			const updated = await response.json()
			const index = this.products.findIndex(p => p.id === id)
			if (index !== -1) this.products[index] = updated
			toastStore.success('Producto actualizado correctamente')
			return updated
		} catch (e: any) {
			this.error = e.message
			toastStore.error(e.message || 'Error al actualizar producto')
			return null
		} finally {
			this.loading = false
		}
	},

	async deleteProduct(id: number) {
		this.loading = true
		this.error = null
		const toastStore = useToastStore()
		try {
			const response = await apiFetch(`/api/products/${id}/`, {
				method: 'DELETE',
			})
			if (!response.ok) throw new Error('Failed to delete product')
			this.products = this.products.filter(p => p.id !== id)
			toastStore.success('Producto eliminado correctamente')
		} catch (e: any) {
			this.error = e.message
			toastStore.error(e.message || 'Error al eliminar producto')
		} finally {
			this.loading = false
		}
	},

	async fetchProductById(id: number) {
		this.loading = true
		try {
			const response = await apiFetch(`/api/products/${id}/`)
			if (!response.ok) throw new Error('Failed to fetch product')
			const product = await response.json()
			return product
		} catch (e: any) {
			this.error = e.message
			return null
		} finally {
			this.loading = false
		}
	},

		async fetchCategories(params: {
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
				const url = `/api/categories/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch categories')
				const data = await response.json()
				this.categories = data.results || data
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async createCategory(data: { name: string; parent_id?: number }) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/categories/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to create category')
				const category = await response.json()
				this.categories.push(category)
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async updateCategory(id: number, data: { name: string; parent_id?: number }) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/categories/${id}/`, {
					method: 'PATCH',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to update category')
				const updated = await response.json()
				const index = this.categories.findIndex(c => c.id === id)
				if (index !== -1) this.categories[index] = updated
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async deleteCategory(id: number) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/categories/${id}/`, {
					method: 'DELETE',
				})
				if (!response.ok) throw new Error('Failed to delete category')
				this.categories = this.categories.filter(c => c.id !== id)
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async fetchCategoryById(id: number) {
			this.loading = true
			try {
				const response = await apiFetch(`/api/categories/${id}/`)
				if (!response.ok) throw new Error('Failed to fetch category')
				return await response.json()
			} catch (e: any) {
				this.error = e.message
				return null
			} finally {
				this.loading = false
			}
		},

		async fetchMovements() {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/inventory-movements/')
				if (!response.ok) throw new Error('Failed to fetch movements')
				this.movements = await response.json()
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async createMovement(data: {
			product: number
			type: 'in' | 'out' | 'adjustment'
			quantity: number
			reason: string
		}) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/inventory-movements/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to create movement')
				const movement = await response.json()
				this.movements.push(movement)
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},
	},

	getters: {
		lowStockProducts: (state) => state.products.filter(p => p.stock > 0 && p.stock <= p.min_stock),
		outOfStockProducts: (state) => state.products.filter(p => p.stock === 0),
	},
})