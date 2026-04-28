export interface Product {
	id: number
	name: string
	category: number
	business: number
	description: string
	cost_price: number
	sell_price: number
	sku: string
	stock: number
	min_stock: number
}

export interface ProductForm {
	name: string
	category: number
	description: string
	cost_price: number
	sell_price: number
	sku: string
	stock: number
	min_stock: number
}
