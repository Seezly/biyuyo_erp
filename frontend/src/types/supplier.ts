export interface Supplier {
	id: number
	name: string
	business_id: number
	rif: string
	email: string
	address: string
	phone: string
	is_active: boolean
	created_at: string
	updated_at: string
}

export interface Purchase {
	id: number
	business_id: number
	supplier_id: number
	status: string
	total: number
	created_at: string
	updated_at: string
	items?: PurchaseItem[]
}

export interface PurchaseItem {
	id: number
	purchase_id: number
	product_id: number
	quantity: number
	cost_price: number
	total_price: number
}