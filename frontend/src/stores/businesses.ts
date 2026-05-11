import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'

interface Business {
	id: number
	name: string
	rif: string
	email: string
	phone: string
	address: string
	state: string
	municipality: string
	is_active: boolean
	start_date: string
	created_at: string
	updated_at: string
}

export const useBusinessesStore = defineStore('businesses', {
	state: () => ({
		businesses: [] as Business[],
		loading: false,
		error: null as string | null,
		pagination: {
			count: 0,
			next: null as string | null,
			previous: null as string | null,
		},
	}),

	actions: {
		async fetchBusinesses(params: {
			search?: string
			is_active?: string
			state?: string
			ordering?: string
			page?: string
		} = {}) {
			this.loading = true
			this.error = null
			try {
				const queryParams = new URLSearchParams()
				if (params.search) queryParams.set('search', params.search)
				if (params.is_active) queryParams.set('is_active', params.is_active)
				if (params.state) queryParams.set('state', params.state)
				if (params.ordering) queryParams.set('ordering', params.ordering)
				if (params.page) queryParams.set('page', params.page)

				const queryString = queryParams.toString()
				const url = `/api/businesses/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch businesses')
				const data = await response.json()
				this.businesses = data.results || data
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

		async getBusiness(id: number): Promise<Business | null> {
			try {
				const response = await apiFetch(`/api/businesses/${id}/`)
				if (!response.ok) return null
				return await response.json()
			} catch (e) {
				return null
			}
		},
	},
})