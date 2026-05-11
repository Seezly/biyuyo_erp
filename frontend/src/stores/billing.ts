import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'

interface Plan {
	id: number
	name: string
	price: number
	max_users: number
	max_products: number
	created_at: string
	updated_at: string
}

interface Subscription {
	id: number
	business: number
	plan: number
	plan_name?: string
	status: string
	start_date: string
	end_date: string | null
}

interface Invoice {
	id: number
	subscription: number
	amount: number
	method: string
	status: string
	created_at: string
	updated_at: string
}

export const useBillingStore = defineStore('billing', {
	state: () => ({
		plans: [] as Plan[],
		subscriptions: [] as Subscription[],
		invoices: [] as Invoice[],
		loading: false,
		error: null as string | null,
		pagination: {
			count: 0,
			next: null as string | null,
			previous: null as string | null,
		},
	}),

	actions: {
		async fetchPlans(params: {
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
				const url = `/api/plans/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch plans')
				const data = await response.json()
				this.plans = data.results || data
			} catch (e: any) {
				this.error = e.message
			} finally {
				this.loading = false
			}
		},

		async fetchSubscriptions(params: {
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
				const url = `/api/subscriptions/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch subscriptions')
				const data = await response.json()
				this.subscriptions = data.results || data
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

		async fetchInvoices(params: {
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
				const url = `/api/invoices/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch invoices')
				const data = await response.json()
				this.invoices = data.results || data
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
	},
})