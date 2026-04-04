export default async function csrfToken(): Promise<void> {
	await fetch('/api/csrf', {
		method: 'GET',
		credentials: 'include',
	})
}
