import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'
import { useToastStore } from '@/stores/toast'

interface Group {
  id: number
  url: string
  name: string
}

export const useRolesStore = defineStore('roles', {
  state: () => ({
    roles: [] as Group[],
    loading: false,
    error: null as string | null,
    pagination: {
      count: 0,
      next: null as string | null,
      previous: null as string | null,
    },
  }),

  actions: {
    async fetchRoles(params: {
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
        const url = `/api/groups/${queryString ? '?' + queryString : ''}`
        const response = await apiFetch(url)

        if (!response.ok) throw new Error('Failed to fetch groups')
        const data = await response.json()
        this.roles = data.results || data
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

    async getRole(id: number): Promise<Group | null> {
      try {
        const response = await apiFetch(`/api/groups/${id}/`)
        if (!response.ok) return null
        return await response.json()
      } catch {
        return null
      }
    },

    async createRole(data: { name: string }): Promise<Group | null> {
      this.loading = true
      this.error = null
      const toastStore = useToastStore()
      try {
        const response = await apiFetch('/api/groups/', {
          method: 'POST',
          body: JSON.stringify(data),
        })

        if (!response.ok) throw new Error('Failed to create group')
        const group = await response.json()
        this.roles.push(group)
        toastStore.success('Rol creado correctamente')
        return group
      } catch (e: any) {
        this.error = e.message
        toastStore.error(e.message || 'Error al crear rol')
        return null
      } finally {
        this.loading = false
      }
    },

    async updateRole(id: number, data: Partial<{ name: string }>): Promise<Group | null> {
      this.loading = true
      this.error = null
      const toastStore = useToastStore()
      try {
        const response = await apiFetch(`/api/groups/${id}/`, {
          method: 'PATCH',
          body: JSON.stringify(data),
        })

        if (!response.ok) throw new Error('Failed to update group')
        const group = await response.json()

        const index = this.roles.findIndex((r) => r.id === id)
        if (index !== -1) {
          this.roles[index] = group
        }

        toastStore.success('Rol actualizado correctamente')
        return group
      } catch (e: any) {
        this.error = e.message
        toastStore.error(e.message || 'Error al actualizar rol')
        return null
      } finally {
        this.loading = false
      }
    },

    async deleteRole(id: number): Promise<boolean> {
      this.loading = true
      this.error = null
      const toastStore = useToastStore()
      try {
        const response = await apiFetch(`/api/groups/${id}/`, {
          method: 'DELETE',
        })

        if (!response.ok) throw new Error('Failed to delete group')

        this.roles = this.roles.filter((r) => r.id !== id)
        toastStore.success('Rol eliminado correctamente')
        return true
      } catch (e: any) {
        this.error = e.message
        toastStore.error(e.message || 'Error al eliminar rol')
        return false
      } finally {
        this.loading = false
      }
    },
  },
})
