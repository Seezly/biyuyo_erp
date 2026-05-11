export interface Sale {
	id: number
	business_id: number
	customer_id: number
	user_id: number
	subtotal: number
	discount: number
	tax: number
	total: number
	status: string
	created_at: string
	updated_at: string
}

export interface SaleItem {
	id: number
	sale_id: number
	product_id: number
	quantity: number
	unit_price: number
	total_price: number
	created_at: string
	updated_at: string
}

export interface Payment {
	id: number
	sale_id: number
	method: string
	amount: number
	reference: string
	status: string
	created_at: string
	updated_at: string
}