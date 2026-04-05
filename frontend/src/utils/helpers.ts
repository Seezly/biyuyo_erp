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

	const res = await fetch(url, {
		credentials: 'include',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
			...(options.headers || {}),
		},
		...options,
	})

	if (res.status === 401) {
		const refreshResponse = await fetch('http://localhost:8000/api/refresh/', {
			method: 'POST',
			credentials: 'include',
		})

		if (refreshResponse.ok) {
			return fetch(url, {
				...options,
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrfToken,
					...(options.headers || {}),
				},
			})
		} else {
			await fetch('http://localhost:8000/api/logout/', { method: 'POST', credentials: 'include' })
			throw new Error('Session expired')
		}
	}

	return res
}
