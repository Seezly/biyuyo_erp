import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useToastStore } from '@/stores/toast'
import { useInventoryStore } from '@/stores/inventory'
import { useSalesStore } from '@/stores/sales'
import { useCustomersStore } from '@/stores/customers'
import { useSuppliersStore } from '@/stores/suppliers'

vi.mock('@/utils/helpers', () => ({
	apiFetch: vi.fn(),
}))

import { apiFetch } from '@/utils/helpers'

describe('Toast Store', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
	})

	it('should show a success toast', () => {
		const store = useToastStore()
		const id = store.success('Test message')
		
		expect(store.toasts.length).toBe(1)
		expect(store.toasts[0].type).toBe('success')
		expect(store.toasts[0].message).toBe('Test message')
		expect(id).toBe(1)
	})

	it('should show an error toast', () => {
		const store = useToastStore()
		store.error('Error message')
		
		expect(store.toasts[0].type).toBe('error')
		expect(store.toasts[0].message).toBe('Error message')
	})

	it('should show a warning toast', () => {
		const store = useToastStore()
		store.warning('Warning message')
		
		expect(store.toasts[0].type).toBe('warning')
	})

	it('should show an info toast', () => {
		const store = useToastStore()
		store.info('Info message')
		
		expect(store.toasts[0].type).toBe('info')
	})

	it('should remove a toast by id', () => {
		const store = useToastStore()
		const id = store.success('Message')
		store.remove(id)
		
		expect(store.toasts.length).toBe(0)
	})

	it('should clear all toasts', () => {
		const store = useToastStore()
		store.success('Message 1')
		store.error('Message 2')
		store.clear()
		
		expect(store.toasts.length).toBe(0)
	})

	it('should auto-remove toast after duration', async () => {
		const store = useToastStore()
		store.show('Quick message', 100)
		
		expect(store.toasts.length).toBe(1)
		
		await new Promise(resolve => setTimeout(resolve, 150))
		
		expect(store.toasts.length).toBe(0)
	})
})

describe('Inventory Store', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.clearAllMocks()
	})

	it('should fetch products from API', async () => {
		const mockProducts = [
			{ id: 1, name: 'Product 1', stock: 10, min_stock: 5 },
			{ id: 2, name: 'Product 2', stock: 3, min_stock: 5 },
		]
		
		vi.mocked(apiFetch).mockResolvedValue({
			ok: true,
			json: () => Promise.resolve(mockProducts),
		} as any)
		
		const store = useInventoryStore()
		await store.fetchProducts()
		
		expect(store.products).toEqual(mockProducts)
		expect(store.loading).toBe(false)
	})

	it('should handle fetch products error', async () => {
		vi.mocked(apiFetch).mockResolvedValue({
			ok: false,
		} as any)
		
		const store = useInventoryStore()
		await store.fetchProducts()
		
		expect(store.error).toBeDefined()
		expect(store.loading).toBe(false)
	})

	it('should filter low stock products', () => {
		const store = useInventoryStore()
		store.products = [
			{ id: 1, name: 'Normal', stock: 10, min_stock: 5 },
			{ id: 2, name: 'Low Stock', stock: 3, min_stock: 5 },
			{ id: 3, name: 'Out of Stock', stock: 0, min_stock: 5 },
		]
		
		expect(store.lowStockProducts.length).toBe(1)
		expect(store.lowStockProducts[0].name).toBe('Low Stock')
	})

	it('should filter out of stock products', () => {
		const store = useInventoryStore()
		store.products = [
			{ id: 1, name: 'Normal', stock: 10, min_stock: 5 },
			{ id: 2, name: 'Low Stock', stock: 3, min_stock: 5 },
			{ id: 3, name: 'Out of Stock', stock: 0, min_stock: 5 },
		]
		
		expect(store.outOfStockProducts.length).toBe(1)
		expect(store.outOfStockProducts[0].name).toBe('Out of Stock')
	})

	it('should fetch categories from API', async () => {
		const mockCategories = [
			{ id: 1, name: 'Category 1' },
			{ id: 2, name: 'Category 2' },
		]
		
		vi.mocked(apiFetch).mockResolvedValue({
			ok: true,
			json: () => Promise.resolve(mockCategories),
		} as any)
		
		const store = useInventoryStore()
		await store.fetchCategories()
		
		expect(store.categories).toEqual(mockCategories)
	})
})

describe('Sales Store', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.clearAllMocks()
	})

	it('should fetch sales from API', async () => {
		const mockSales = [
			{ id: 1, total: 100, created_at: '2024-01-01T10:00:00Z' },
			{ id: 2, total: 200, created_at: '2024-01-02T10:00:00Z' },
		]
		
		vi.mocked(apiFetch).mockResolvedValue({
			ok: true,
			json: () => Promise.resolve(mockSales),
		} as any)
		
		const store = useSalesStore()
		await store.fetchSales()
		
		expect(store.sales).toEqual(mockSales)
	})

	it('should calculate today total', () => {
		const store = useSalesStore()
		const today = new Date().toISOString().split('T')[0]
		
		store.sales = [
			{ id: 1, total: 100, created_at: `${today}T10:00:00Z` },
			{ id: 2, total: 200, created_at: `${today}T11:00:00Z` },
			{ id: 3, total: 50, created_at: '2023-01-01T10:00:00Z' },
		]
		
		expect(store.todayTotal).toBe(300)
	})

	it('should return 0 when no sales today', () => {
		const store = useSalesStore()
		store.sales = [
			{ id: 1, total: 100, created_at: '2023-01-01T10:00:00Z' },
		]
		
		expect(store.todayTotal).toBe(0)
	})

	it('should clear current sale', () => {
		const store = useSalesStore()
		store.currentSale = { id: 1, total: 100 } as any
		
		store.clearCurrentSale()
		
		expect(store.currentSale).toBeNull()
	})
})

describe('Customers Store', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.clearAllMocks()
	})

	it('should fetch customers from API', async () => {
		const mockCustomers = [
			{ id: 1, name: 'Customer 1', phone: '04121234567' },
			{ id: 2, name: 'Customer 2', phone: '04129876543' },
		]
		
		vi.mocked(apiFetch).mockResolvedValue({
			ok: true,
			json: () => Promise.resolve(mockCustomers),
		} as any)
		
		const store = useCustomersStore()
		await store.fetchCustomers()
		
		expect(store.customers).toEqual(mockCustomers)
	})

	it('should search customers by name', () => {
		const store = useCustomersStore()
		store.customers = [
			{ id: 1, name: 'John Doe', phone: '04121234567', identification_number: 'V12345678' },
			{ id: 2, name: 'Jane Smith', phone: '04129876543', identification_number: 'V87654321' },
		]
		
		const results = store.searchCustomers('john')
		
		expect(results.length).toBe(1)
		expect(results[0].name).toBe('John Doe')
	})

	it('should search customers by phone', () => {
		const store = useCustomersStore()
		store.customers = [
			{ id: 1, name: 'John Doe', phone: '04121234567', identification_number: 'V12345678' },
			{ id: 2, name: 'Jane Smith', phone: '04129876543', identification_number: 'V87654321' },
		]
		
		const results = store.searchCustomers('0412123')
		
		expect(results.length).toBe(1)
	})

	it('should get customer count', () => {
		const store = useCustomersStore()
		store.customers = [
			{ id: 1, name: 'Customer 1' },
			{ id: 2, name: 'Customer 2' },
		]
		
		expect(store.customerCount).toBe(2)
	})

	it('should find customer by id', () => {
		const store = useCustomersStore()
		store.customers = [
			{ id: 1, name: 'Customer 1' },
			{ id: 2, name: 'Customer 2' },
		]
		
		const customer = store.customerById(2)
		
		expect(customer?.name).toBe('Customer 2')
	})
})

describe('Suppliers Store', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.clearAllMocks()
	})

	it('should fetch suppliers from API', async () => {
		const mockSuppliers = [
			{ id: 1, name: 'Supplier 1', is_active: true },
			{ id: 2, name: 'Supplier 2', is_active: false },
		]
		
		vi.mocked(apiFetch).mockResolvedValue({
			ok: true,
			json: () => Promise.resolve(mockSuppliers),
		} as any)
		
		const store = useSuppliersStore()
		await store.fetchSuppliers()
		
		expect(store.suppliers).toEqual(mockSuppliers)
	})

	it('should filter active suppliers', () => {
		const store = useSuppliersStore()
		store.suppliers = [
			{ id: 1, name: 'Active', is_active: true },
			{ id: 2, name: 'Inactive', is_active: false },
		]
		
		expect(store.activeSuppliers.length).toBe(1)
		expect(store.activeSuppliers[0].name).toBe('Active')
	})

	it('should find supplier by id', () => {
		const store = useSuppliersStore()
		store.suppliers = [
			{ id: 1, name: 'Supplier 1' },
			{ id: 2, name: 'Supplier 2' },
		]
		
		const supplier = store.supplierById(2)
		
		expect(supplier?.name).toBe('Supplier 2')
	})
})