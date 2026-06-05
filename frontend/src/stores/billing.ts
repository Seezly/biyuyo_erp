import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'
import { useToastStore } from '@/stores/toast'

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

	async fetchPlan(id: number) {
		this.loading = true
		this.error = null
		try {
			const response = await apiFetch(`/api/plans/${id}/`)
			if (!response.ok) throw new Error('Failed to fetch plan')
			const plan = await response.json()
			return plan
		} catch (e: any) {
			this.error = e.message
			return null
		} finally {
			this.loading = false
		}
	},

		async createPlan(data: Omit<Plan, 'id' | 'created_at' | 'updated_at'>) {
			this.loading = true
			this.error = null
			const toastStore = useToastStore()
			try {
				const response = await apiFetch('/api/plans/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to create plan')
				const plan = await response.json()
				this.plans.push(plan)
				toastStore.success('Plan creado correctamente')
				return plan
			} catch (e: any) {
				this.error = e.message
				toastStore.error(e.message || 'Error al crear el plan')
				return null
			} finally {
				this.loading = false
			}
		},

	async updatePlan(id: number, data: Partial<Omit<Plan, 'created_at' | 'updated_at'>>) {
		this.loading = true
		this.error = null
		const toastStore = useToastStore()
		try {
			const response = await apiFetch(`/api/plans/${id}/`, {
				method: 'PATCH',
				body: JSON.stringify(data),
			})
			if (!response.ok) throw new Error('Failed to update plan')
			const updated = await response.json()
			const index = this.plans.findIndex(p => p.id === id)
			if (index !== -1) this.plans[index] = updated
			toastStore.success('Plan actualizado correctamente')
			return updated
		} catch (e: any) {
			this.error = e.message
			toastStore.error(e.message || 'Error al actualizar el plan')
			return null
		} finally {
			this.loading = false
		}
	},

		async deletePlan(id: number) {
			this.loading = true
			this.error = null
			const toastStore = useToastStore()
			try {
				const response = await apiFetch(`/api/plans/${id}/`, {
					method: 'DELETE',
				})
				if (!response.ok) throw new Error('Failed to delete plan')
				this.plans = this.plans.filter(p => p.id !== id)
				toastStore.success('Plan eliminado correctamente')
			} catch (e: any) {
				this.error = e.message
				toastStore.error(e.message || 'Error al eliminar el plan')
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

		async fetchSubscriptionById(id: number) {
			this.loading = true
			this.error = null
			try {
				const response = await apiFetch(`/api/subscriptions/${id}/`)
				if (!response.ok) throw new Error('Failed to fetch subscription')
				return await response.json()
			} catch (e: any) {
				this.error = e.message
				return null
			} finally {
				this.loading = false
			}
		},

		async createSubscription(data: Omit<Subscription, 'id' | 'created_at' | 'updated_at' | 'plan_name'>) {
			this.loading = true
			this.error = null
			const toastStore = useToastStore()
			try {
				const response = await apiFetch('/api/subscriptions/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to create subscription')
				const subscription = await response.json()
				this.subscriptions.push(subscription)
				toastStore.success('Suscripción creada correctamente')
				return subscription
			} catch (e: any) {
				this.error = e.message
				toastStore.error(e.message || 'Error al crear la suscripción')
				return null
			} finally {
				this.loading = false
			}
		},

		async updateSubscription(id: number, data: Partial<Omit<Subscription, 'created_at' | 'updated_at' | 'plan_name'>>) {
			this.loading = true
			this.error = null
			const toastStore = useToastStore()
			try {
				const response = await apiFetch(`/api/subscriptions/${id}/`, {
					method: 'PATCH',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to update subscription')
				const updated = await response.json()
				const index = this.subscriptions.findIndex(s => s.id === id)
				if (index !== -1) this.subscriptions[index] = updated
				toastStore.success('Suscripción actualizada correctamente')
			} catch (e: any) {
				this.error = e.message
				toastStore.error(e.message || 'Error al actualizar la suscripción')
			} finally {
				this.loading = false
			}
		},

		async deleteSubscription(id: number) {
			this.loading = true
			this.error = null
			const toastStore = useToastStore()
			try {
				const response = await apiFetch(`/api/subscriptions/${id}/`, {
					method: 'DELETE',
				})
				if (!response.ok) throw new Error('Failed to delete subscription')
				this.subscriptions = this.subscriptions.filter(s => s.id !== id)
				toastStore.success('Suscripción eliminada correctamente')
			} catch (e: any) {
				this.error = e.message
				toastStore.error(e.message || 'Error al eliminar la suscripción')
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

		async createInvoice(data: Omit<Invoice, 'id' | 'created_at' | 'updated_at'>) {
			this.loading = true
			this.error = null
			const toastStore = useToastStore()
			try {
				const response = await apiFetch('/api/invoices/', {
					method: 'POST',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to create invoice')
				const invoice = await response.json()
				this.invoices.push(invoice)
				toastStore.success('Factura creada correctamente')
				return invoice
			} catch (e: any) {
				this.error = e.message
				toastStore.error(e.message || 'Error al crear la factura')
				return null
			} finally {
				this.loading = false
			}
		},

		async updateInvoice(id: number, data: Partial<Omit<Invoice, 'created_at' | 'updated_at'>>) {
			this.loading = true
			this.error = null
			const toastStore = useToastStore()
			try {
				const response = await apiFetch(`/api/invoices/${id}/`, {
					method: 'PATCH',
					body: JSON.stringify(data),
				})
				if (!response.ok) throw new Error('Failed to update invoice')
				const updated = await response.json()
				const index = this.invoices.findIndex(i => i.id === id)
				if (index !== -1) this.invoices[index] = updated
				toastStore.success('Factura actualizada correctamente')
			} catch (e: any) {
				this.error = e.message
				toastStore.error(e.message || 'Error al actualizar la factura')
			} finally {
				this.loading = false
			}
		},

		async deleteInvoice(id: number) {
			this.loading = true
			this.error = null
			const toastStore = useToastStore()
			try {
				const response = await apiFetch(`/api/invoices/${id}/`, {
					method: 'DELETE',
				})
				if (!response.ok) throw new Error('Failed to delete invoice')
				this.invoices = this.invoices.filter(i => i.id !== id)
				toastStore.success('Factura eliminada correctamente')
			} catch (e: any) {
				this.error = e.message
				toastStore.error(e.message || 'Error al eliminar la factura')
			} finally {
				this.loading = false
			}
		},
	},
})