export interface SalesReport {
	id: number
	business_id: number
	start_date: string
	end_date: string
	total_sales: number
	total_items_sold: number
	average_sale: number
	created_at: string
}

export interface InventoryReport {
	id: number
	business_id: number
	total_products: number
	total_value: number
	low_stock_count: number
	out_of_stock_count: number
	report_date: string
	created_at: string
}

export interface FinancialReport {
	id: number
	business_id: number
	start_date: string
	end_date: string
	total_income: number
	total_expenses: number
	net_profit: number
	created_at: string
}