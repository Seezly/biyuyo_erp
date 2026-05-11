export interface Plan {
	id: number
	name: string
	price: number
	max_users: number
	max_products: number
	created_at: string
	updated_at: string
}

export interface Subscription {
	id: number
	business_id: number
	plan_id: number
	status: string
	start_date: string
	end_date?: string
	created_at: string
	updated_at: string
}

export interface Invoice {
	id: number
	subscription_id: number
	amount: number
	method: string
	status: string
	created_at: string
	updated_at: string
}