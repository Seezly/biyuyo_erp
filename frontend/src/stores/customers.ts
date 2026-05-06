import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'

interface Customer {
	id: number
	name: string
	business: number
	phone: string
	identification_number: string
	created_at: string
	updated_at: string
}

interface CustomerForm {
	name: string
	phone: string
	identification_number: string
}

export const useCustomersStore = defineStore('customers', {
	state: () => ({
		customers: [] as Customer[],
		currentCustomer: null as Customer | null,
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
		async fetchCustomers(params: {
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
				const url = `/api/customers/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch customers')
				const data = await response.json()
				this.customers = data.results || data
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

		async fetchCustomer(id: number) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/customers/${id}/`)
				if (!response.ok) throw new Error('Failed to fetch customer')
				this.currentCustomer = await response.json()
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async createCustomer(data: CustomerForm) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch('/api/customers/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) {
					const errorData = await response.json()
					throw new Error(JSON.stringify(errorData))
				}
				const customer = await response.json()
				this.customers.unshift(customer)
				return customer
			} catch (e: any) {
				this.error = e.message
				return null
			} finally {
				this.loading = false
			}
		},

		async updateCustomer(id: number, data: Partial<CustomerForm>) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/customers/${id}/`, {
					method: 'PATCH',
					body: JSON.stringify(data),
				})
				if (!response.ok) {
					const errorData = await response.json()
					throw new Error(JSON.stringify(errorData))
				}
				const updated = await response.json()
				const index = this.customers.findIndex(c => c.id === id)
				if (index !== -1) this.customers[index] = updated
				return updated
			} catch (e: any) {
				this.error = e.message
				return null
			} finally {
				this.loading = false
			}
		},

		async deleteCustomer(id: number) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/customers/${id}/`, {
					method: 'DELETE',
				})
				if (!response.ok) throw new Error('Failed to delete customer')
				this.customers = this.customers.filter(c => c.id !== id)
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		clearCurrentCustomer() {
			this.currentCustomer = null
		},

		searchCustomers(query: string) {
			const lowerQuery = query.toLowerCase()
			return this.customers.filter(c => 
				c.name.toLowerCase().includes(lowerQuery) ||
				c.phone.includes(query) ||
				c.identification_number.includes(query)
			)
		},
	},

	getters: {
		customerCount: (state) => state.customers.length,
		customerById: (state) => (id: number) => state.customers.find(c => c.id === id),
	},
})