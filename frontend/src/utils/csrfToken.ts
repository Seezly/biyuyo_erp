export default async function csrfToken(): Promise<void> {
	await fetch(import.meta.env.VITE_API_URL + '/api/csrf/', {
		method: 'GET',
		credentials: 'include',
	})
}
