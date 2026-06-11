export interface Category {
	id: number
	name: string
	business_id: number
	parent_id: number | null
	created_at: string
	updated_at: string
}

export interface Product {
	id: number
	name: string
	description: string
	sku: string
	cost_price: number
	sell_price: number
	stock: number
	min_stock: number
	category_id: number
	business_id: number
	created_at: string
	updated_at: string
}

export interface InventoryMovement {
	id: number
	type: string
	quantity: number
	reference: string
	product_id: number
	business_id: number
	created_at: string
	updated_at: string
}