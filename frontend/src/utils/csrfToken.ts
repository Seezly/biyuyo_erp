const API_BASE = import.meta.env.VITE_API_URL || ''

export default async function csrfToken(): Promise<void> {
	await fetch(API_BASE + '/api/csrf/', {
		method: 'GET',
		credentials: 'include',
	})
}
