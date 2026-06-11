import { useAuthStore } from '@/stores/auth'

// Function that takes the cookies object and search for a specific cookie
export function getCookie(name: string): string | undefined {
	const value = `; ${document.cookie}`
	const parts = value.split(`; ${name}=`)
	if (parts.length === 2) return parts.pop()?.split(';').shift()
}

/*
Function that wraps the functionality that retrieves the csrf token,
makes the fetch request, if the response is a status code 401
refresh the token, retry the fetch and returns the final response
*/
export async function apiFetch(url: string, options: RequestInit = {}) {
	const csrfToken = getCookie('csrftoken') || ''
	const { headers: userHeaders, ...restOptions } = options

	const auth = useAuthStore()
	const businessHeaders: Record<string, string> = {}
	if (auth.impersonatedBusinessId) {
		businessHeaders['X-Business-Id'] = auth.impersonatedBusinessId.toString()
	}

	const res = await fetch(import.meta.env.VITE_API_URL + url, {
		...restOptions,
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
			...businessHeaders,
			...(userHeaders || {}),
		},
	})

	if (res.status === 401) {
		const refreshResponse = await fetch(import.meta.env.VITE_API_URL + '/api/refresh/', {
			method: 'POST',
			credentials: 'include',
		})

		if (refreshResponse.ok) {
			const newCsrfToken = getCookie('csrftoken') || csrfToken
			const { headers: retryHeaders, ...retryRest } = options
			return fetch(import.meta.env.VITE_API_URL + url, {
				...retryRest,
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': newCsrfToken,
					...businessHeaders,
					...(retryHeaders || {}),
				},
			})
		} else {
			await fetch(import.meta.env.VITE_API_URL + '/api/logout/', {
				method: 'POST',
				credentials: 'include',
			})
			throw new Error('Session expired')
		}
	}

	return res
}
