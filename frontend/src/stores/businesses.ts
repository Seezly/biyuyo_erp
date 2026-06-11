import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'
import { useToastStore } from '@/stores/toast'
import type { Business } from '@/types/business'

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

    async createBusiness(data: any): Promise<Business | null> {
      this.loading = true
      this.error = null
      const toastStore = useToastStore()
      try {
        const response = await apiFetch('/api/businesses/', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) throw new Error('Failed to create business')
        const business = await response.json()
        this.businesses.push(business)
        toastStore.success('Negocio creado correctamente')
        return business
      } catch (e: any) {
        this.error = e.message
        toastStore.error(e.message || 'Error al crear el negocio')
        return null
      } finally {
        this.loading = false
      }
    },

    async updateBusiness(id: number, data: any): Promise<Business | null> {
      this.loading = true
      this.error = null
      const toastStore = useToastStore()
      try {
        const response = await apiFetch(`/api/businesses/${id}/`, {
          method: 'PUT',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) throw new Error('Failed to update business')
        const business = await response.json()
        
        // Update in local state
        const index = this.businesses.findIndex(b => b.id === id)
        if (index !== -1) {
          this.businesses[index] = business
        }
        
        toastStore.success('Negocio actualizado correctamente')
        return business
      } catch (e: any) {
        this.error = e.message
        toastStore.error(e.message || 'Error al actualizar el negocio')
        return null
      } finally {
        this.loading = false
      }
    },

    async deleteBusiness(id: number): Promise<boolean> {
      this.loading = true
      this.error = null
      const toastStore = useToastStore()
      try {
        const response = await apiFetch(`/api/businesses/${id}/`, {
          method: 'DELETE'
        })

        if (!response.ok) throw new Error('Failed to delete business')
        
        // Remove from local state
        this.businesses = this.businesses.filter(b => b.id !== id)
        toastStore.success('Negocio eliminado correctamente')
        return true
      } catch (e: any) {
        this.error = e.message
        toastStore.error(e.message || 'Error al eliminar el negocio')
        return false
      } finally {
        this.loading = false
      }
    },
  },
})