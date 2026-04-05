export default async function csrfToken(): Promise<void> {
	await fetch(import.meta.env.BASE_URL + '/api/csrf/', {
		method: 'GET',
		credentials: 'include',
	})
}
