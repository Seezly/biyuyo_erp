import { defineStore } from 'pinia'

import { type User } from '@/types/Auth'
import { apiFetch } from '@/utils/helpers'

export const useAuthStore = defineStore('auth', {
	state: () => ({
		user: null as null | User,
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
				await fetch(`http://localhost:8000/api/logout/`, {
					method: 'POST',
					credentials: 'include',
				})
			} catch (e) {
				console.log('Logout failed: ' + e)
			}
		},

		async fetchUser() {
			try {
				const res = await apiFetch('http://localhost:8000/api/me/')

				if (!res.ok) throw new Error()

				const data = await res.json()

				this.setUser(data)
			} catch (e) {
				console.error('fetchUser error:', e)
			} finally {
				this.loading = false
			}
		},
	},
})
