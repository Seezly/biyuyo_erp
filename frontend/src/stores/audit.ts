import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/helpers'

interface AuditLogEntry {
  id: number
  user: {
    id: number
    email: string
    first_name: string
    last_name: string
  } | null
  action: string
  model_name: string
  object_id: string | null
  object_repr: string | null
  changes: Record<string, any> | null
  description: string | null
  ip_address: string | null
  user_agent: string | null
  timestamp: string
}

export const useAuditStore = defineStore('audit', {
	state: () => ({
    logs: [] as AuditLogEntry[],
    loading: false,
    error: null as string | null,
    pagination: {
      count: 0,
      next: null as string | null,
      previous: null as string | null,
    },
  }),

  actions: {
    async fetchAuditLogs(params: {
      user_id?: number | null
      action?: string | null
      model_name?: string | null
      start_date?: string | null
      end_date?: string | null
      ordering?: string
      page?: string
    } = {}) {
      this.loading = true
      this.error = null
      try {
        const queryParams = new URLSearchParams()
        if (params.user_id !== null && params.user_id !== undefined) queryParams.set('user_id', params.user_id.toString())
        if (params.action) queryParams.set('action', params.action)
        if (params.model_name) queryParams.set('model_name', params.model_name)
        if (params.start_date) queryParams.set('start_date', params.start_date)
        if (params.end_date) queryParams.set('end_date', params.end_date)
        if (params.ordering) queryParams.set('ordering', params.ordering)
        if (params.page) queryParams.set('page', params.page)

        const queryString = queryParams.toString()
        const url = `/api/audit/logs/${queryString ? '?' + queryString : ''}`
        const response = await apiFetch(url)

        if (!response.ok) throw new Error('Failed to fetch audit logs')
        const data = await response.json()
        this.logs = data.results || data
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

    async fetchAuditLog(id: number) {
      this.loading = true
      this.error = null
      try {
        const response = await apiFetch(`/api/audit/logs/${id}/`)
        if (!response.ok) throw new Error('Failed to fetch audit log')
        const log = await response.json()
        return log
      } catch (e: any) {
        this.error = e.message
        return null
      } finally {
        this.loading = false
      }
    },
  },
})