import { defineStore } from 'pinia'
import { useToastStore } from '@/stores/toast'

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
  business_id: number
  created_at: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as null | User,
    users: [] as UserItem[],
    isAuthenticated: false,
    loading: true,
    error: null as string | null,
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
        await apiFetch('/api/logout/', {
          method: 'POST',
        })
      } catch (e) {
        console.error('Logout failed: ' + e)
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
      this.loading = true
      this.error = null
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
        this.error = e.message
      } finally {
        this.loading = false
      }
    },

    async fetchUserById(id: number) {
      this.loading = true
      this.error = null
      try {
        const response = await apiFetch(`/api/users/${id}/`)
        if (!response.ok) throw new Error('Failed to fetch user')
        const user = await response.json()
        return user
      } catch (e: any) {
        this.error = e.message
        return null
      } finally {
        this.loading = false
      }
    },

    async createUser(data: Record<string, any>) {
      this.loading = true
      this.error = null
      const toastStore = useToastStore()
      try {
        const response = await apiFetch('/api/users/', {
          method: 'POST',
          body: JSON.stringify(data),
        })
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(JSON.stringify(errorData))
        }
        const user = await response.json()
        this.users.unshift(user)
        toastStore.success('Usuario creado correctamente')
        return user
      } catch (e: any) {
        this.error = e.message
        toastStore.error(e.message || 'Error al crear el usuario')
        return null
      } finally {
        this.loading = false
      }
    },

    async updateUser(id: number, data: Partial<Record<string, any>>) {
      this.loading = true
      this.error = null
      const toastStore = useToastStore()
      try {
        const response = await apiFetch(`/api/users/${id}/`, {
          method: 'PATCH',
          body: JSON.stringify(data),
        })
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(JSON.stringify(errorData))
        }
        const updated = await response.json()
        const index = this.users.findIndex(u => u.id === id)
        if (index !== -1) this.users[index] = updated
        toastStore.success('Usuario actualizado correctamente')
        return updated
      } catch (e: any) {
        this.error = e.message
        toastStore.error(e.message || 'Error al actualizar el usuario')
        return null
      } finally {
        this.loading = false
      }
    },

    async deleteUser(id: number) {
      this.loading = true
      this.error = null
      const toastStore = useToastStore()
      try {
        const response = await apiFetch(`/api/users/${id}/`, {
          method: 'DELETE',
        })
        if (!response.ok) throw new Error('Failed to delete user')
        this.users = this.users.filter(u => u.id !== id)
        toastStore.success('Usuario eliminado correctamente')
        return true
      } catch (e: any) {
        this.error = e.message
        toastStore.error(e.message || 'Error al eliminar el usuario')
        return false
      } finally {
        this.loading = false
      }
    },
  },
})