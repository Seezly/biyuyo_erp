import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'
import { type Role, type RoleForm } from '@/types/role'

export const useRolesStore = defineStore('roles', {
  state: () => ({
    roles: [] as Role[],
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
      is_active?: string
      ordering?: string
      page?: string
    } = {}) {
      this.loading = true
      this.error = null
      try {
        const queryParams = new URLSearchParams()
        if (params.search) queryParams.set('search', params.search)
        if (params.is_active) queryParams.set('is_active', params.is_active)
        if (params.ordering) queryParams.set('ordering', params.ordering)
        if (params.page) queryParams.set('page', params.page)

        const queryString = queryParams.toString()
        const url = `/api/roles/${queryString ? '?' + queryString : ''}`
        const response = await apiFetch(url)

        if (!response.ok) throw new Error('Failed to fetch roles')
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

    async getRole(id: number): Promise<Role | null> {
      try {
        const response = await apiFetch(`/api/roles/${id}/`)
        if (!response.ok) return null
        return await response.json()
      } catch (e) {
        return null
      }
    },

    async createRole(data: RoleForm): Promise<Role | null> {
      this.loading = true
      this.error = null
      try {
        const response = await apiFetch('/api/roles/', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) throw new Error('Failed to create role')
        const role = await response.json()
        this.roles.push(role)
        return role
      } catch (e: any) {
        this.error = e.message
        return null
      } finally {
        this.loading = false
      }
    },

    async updateRole(id: number, data: Partial<RoleForm>): Promise<Role | null> {
      this.loading = true
      this.error = null
      try {
        const response = await apiFetch(`/api/roles/${id}/`, {
          method: 'PATCH',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) throw new Error('Failed to update role')
        const role = await response.json()
        
        // Update in local state
        const index = this.roles.findIndex(r => r.id === id)
        if (index !== -1) {
          this.roles[index] = role
        }
        
        return role
      } catch (e: any) {
        this.error = e.message
        return null
      } finally {
        this.loading = false
      }
    },

    async deleteRole(id: number): Promise<boolean> {
      this.loading = true
      this.error = null
      try {
        const response = await apiFetch(`/api/roles/${id}/`, {
          method: 'DELETE'
        })

        if (!response.ok) throw new Error('Failed to delete role')
        
        // Remove from local state
        this.roles = this.roles.filter(r => r.id !== id)
        return true
      } catch (e: any) {
        this.error = e.message
        return false
      } finally {
        this.loading = false
      }
    },
  },
})