export interface Product {
	id: number
	name: string
	category_id: number
	business_id: number
	description: string
	cost_price: number
	sell_price: number
	sku: string
	stock: number
	min_stock: number
}

export interface ProductForm {
	id?: number
	name: string
	category_id: number
	description: string
	cost_price: number
	sell_price: number
	sku: string
	stock: number
	min_stock: number
}
