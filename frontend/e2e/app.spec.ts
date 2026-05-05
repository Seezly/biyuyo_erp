import { test, expect } from '@playwright/test'

const BASE_URL = 'http://localhost:5173'

test.describe('Authentication Flow', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto(`${BASE_URL}/login`)
	})

	test('should display login form', async ({ page }) => {
		await expect(page.getByRole('heading', { name: 'Iniciar sesión' })).toBeVisible()
		await expect(page.locator('input[name="email"]')).toBeVisible()
		await expect(page.locator('input[name="password"]')).toBeVisible()
		await expect(page.locator('form button').last()).toBeVisible()
	})

	test('should navigate to register page', async ({ page }) => {
		await page.getByRole('link', { name: 'Regístrate' }).click()
		await expect(page).toHaveURL(`${BASE_URL}/register`)
	})

	test('should have email validation', async ({ page }) => {
		const emailInput = page.locator('input[name="email"]')
		await emailInput.fill('notanemail')
		await emailInput.blur()
		await expect(page.locator('input[type="email"]')).toHaveAttribute('type', 'email')
	})
})

test.describe('Register Flow', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto(`${BASE_URL}/register`)
	})

	test('should display register form', async ({ page }) => {
		await expect(page.getByRole('heading', { name: 'Crear cuenta' })).toBeVisible()
	})

	test('should navigate to login from register', async ({ page }) => {
		await page.getByRole('link', { name: 'Iniciar sesión' }).click()
		await expect(page).toHaveURL(`${BASE_URL}/login`)
	})
})

test.describe('Navigation', () => {
	test('should display logo on home', async ({ page }) => {
		await page.goto(BASE_URL)
		await expect(page.getByRole('heading', { name: 'Biyuyo' })).toBeVisible()
	})
})