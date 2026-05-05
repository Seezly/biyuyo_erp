import { defineStore } from 'pinia'

export interface Toast {
	id: number
	type: 'success' | 'error' | 'warning' | 'info'
	message: string
	duration?: number
}

let toastId = 0

export const useToastStore = defineStore('toast', {
	state: () => ({
		toasts: [] as Toast[],
	}),

	actions: {
		show(type: Toast['type'], message: string, duration = 4000) {
			const id = ++toastId
			const toast: Toast = { id, type, message, duration }

			this.toasts.push(toast)

			if (duration > 0) {
				setTimeout(() => {
					this.remove(id)
				}, duration)
			}

			return id
		},

		success(message: string, duration?: number) {
			return this.show('success', message, duration)
		},

		error(message: string, duration?: number) {
			return this.show('error', message, duration)
		},

		warning(message: string, duration?: number) {
			return this.show('warning', message, duration)
		},

		info(message: string, duration?: number) {
			return this.show('info', message, duration)
		},

		remove(id: number) {
			this.toasts = this.toasts.filter(t => t.id !== id)
		},

		clear() {
			this.toasts = []
		},
	},
})