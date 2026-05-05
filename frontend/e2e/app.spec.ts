import { test, expect } from '@playwright/test'

const BASE_URL = process.env.CI ? 'http://localhost:4173' : 'http://localhost:5173'

test.describe('Authentication Flow', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto(`${BASE_URL}/login`)
	})

	test('should display login form', async ({ page }) => {
		await expect(page.locator('h1')).toContainText('Iniciar sesión')
		await expect(page.locator('input[name="email"]')).toBeVisible()
		await expect(page.locator('input[name="password"]')).toBeVisible()
		await expect(page.getByRole('button', { name: 'Iniciar sesión' })).toBeVisible()
	})

	test('should show error with invalid credentials', async ({ page }) => {
		await page.fill('input[name="email"]', 'invalid@test.com')
		await page.fill('input[name="password"]', 'wrongpassword')
		await page.getByRole('button', { name: 'Iniciar sesión' }).click()
		
		await expect(page.locator('.bg-red-100')).toBeVisible()
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
		await expect(page.locator('h1')).toContainText('Regístrate')
	})

	test('should navigate to login from register', async ({ page }) => {
		await page.getByRole('link', { name: 'Iniciar sesión' }).click()
		await expect(page).toHaveURL(`${BASE_URL}/login`)
	})
})

test.describe('POS Flow', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto(`${BASE_URL}/sales/pos`)
	})

	test('should display POS page', async ({ page }) => {
		await expect(page.locator('h1')).toContainText('Punto de Venta')
	})

	test('should show product grid', async ({ page }) => {
		await expect(page.locator('.grid')).toBeVisible()
	})

	test('should have step indicator', async ({ page }) => {
		await expect(page.locator('text=Agregar productos')).toBeVisible()
		await expect(page.locator('text=Método de pago')).toBeVisible()
		await expect(page.locator('text=Recibo')).toBeVisible()
	})

	test('should have search input', async ({ page }) => {
		await expect(page.locator('input[placeholder*="Busca producto"]')).toBeVisible()
	})

	test('should display cart summary', async ({ page }) => {
		await expect(page.locator('text=Total del pedido')).toBeVisible()
		await expect(page.locator('text=Carrito vacío')).toBeVisible()
	})

	test('should navigate to payment step with products', async ({ page }) => {
		await page.getByRole('button', { name: 'Agregar' }).first().click()
		await page.getByRole('button', { name: 'Método de pago' }).click()
		
		await expect(page.locator('text=Selecciona el método de pago')).toBeVisible()
	})
})

test.describe('Products Page', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto(`${BASE_URL}/inventory/products`)
	})

	test('should display products page title', async ({ page }) => {
		await expect(page.locator('h1')).toContainText('Lista de productos')
	})

	test('should have add product button', async ({ page }) => {
		await expect(page.getByRole('link', { name: 'Añadir producto' })).toBeVisible()
	})

	test('should have search input', async ({ page }) => {
		await expect(page.locator('input[placeholder*="Buscar"]')).toBeVisible()
	})
})

test.describe('Sales List Page', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto(`${BASE_URL}/sales/all`)
	})

	test('should display sales list title', async ({ page }) => {
		await expect(page.locator('h1')).toContainText('Total de ventas')
	})

	test('should have new sale button', async ({ page }) => {
		await expect(page.getByRole('link', { name: 'Nueva venta' })).toBeVisible()
	})
})

test.describe('Customers Page', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto(`${BASE_URL}/customers`)
	})

	test('should display customers title', async ({ page }) => {
		await expect(page.locator('h1')).toContainText('Clientes')
	})
})

test.describe('Suppliers Page', () => {
	test.beforeEach(async ({ page }) => {
		await page.goto(`${BASE_URL}/suppliers`)
	})

	test('should display suppliers title', async ({ page }) => {
		await expect(page.locator('h1')).toContainText('Proveedores')
	})
})

test.describe('Navigation', () => {
	test('should have working navigation menu', async ({ page }) => {
		await page.goto(BASE_URL)
		
		await page.getByRole('link', { name: 'Inventario' }).click()
		await expect(page).toHaveURL(`${BASE_URL}/inventory`)
		
		await page.getByRole('link', { name: 'Ventas' }).click()
		await expect(page).toHaveURL(`${BASE_URL}/sales`)
		
		await page.getByRole('link', { name: 'Clientes' }).click()
		await expect(page).toHaveURL(`${BASE_URL}/customers`)
	})
})