import { defineStore } from 'pinia'

import { type User } from '@/types/Auth'
import { apiFetch } from '@/utils/helpers'

interface UserItem {
	id: number
	first_name: string
	last_name: string
	email: string
	phone: string
	identification_number: string
	role: string
	business: number
	created_at: string
}

export const useAuthStore = defineStore('auth', {
	state: () => ({
		user: null as null | User,
		users: [] as UserItem[],
		isAuthenticated: false,
		loading: true,
	}),

	actions: {
		setUser(user: User) {
			this.user = user
			this.isAuthenticated = true
		},

		async logout() {
			this.user = null
			this.isAuthenticated = false

			try {
				await fetch('/api/logout/', {
					method: 'POST',
					credentials: 'include',
				})
			} catch (e) {
				console.log('Logout failed: ' + e)
			}
		},

		async fetchUser() {
			try {
				const res = await apiFetch('/api/me/')

				if (!res.ok) throw new Error()

				const data = await res.json()

				this.setUser(data)
			} catch (e) {
				console.error('fetchUser error:', e)
			} finally {
				this.loading = false
			}
		},

		async fetchUsers(params: {
			search?: string
			ordering?: string
			page?: string
		} = {}) {
			try {
				const queryParams = new URLSearchParams()
				if (params.search) queryParams.set('search', params.search)
				if (params.ordering) queryParams.set('ordering', params.ordering)
				if (params.page) queryParams.set('page', params.page)

				const queryString = queryParams.toString()
				const url = `/api/users/${queryString ? '?' + queryString : ''}`
				const response = await apiFetch(url)

				if (!response.ok) throw new Error('Failed to fetch users')
				const data = await response.json()
				this.users = data.results || data
			} catch (e: any) {
				console.error('fetchUsers error:', e)
			}
		},

		async deleteUser(id: number) {
			try {
				const response = await apiFetch(`/api/users/${id}/`, {
					method: 'DELETE',
				})
				if (!response.ok) throw new Error('Failed to delete user')
				this.users = this.users.filter(u => u.id !== id)
				return true
			} catch (e: any) {
				console.error('deleteUser error:', e)
				return false
			}
		},
	},
})
