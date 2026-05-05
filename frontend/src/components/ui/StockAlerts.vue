<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiFetch } from '@/utils/helpers'

interface LowStockProduct {
	id: number
	name: string
	stock: number
	min_stock: number
	sku: string
}

const lowStockProducts = ref<LowStockProduct[]>([])
const loading = ref(true)
const showAlerts = ref(false)

const fetchLowStock = async () => {
	try {
		const response = await apiFetch('/api/products/low_stock/')
		if (response.ok) {
			lowStockProducts.value = await response.json()
		}
	} catch (error) {
		console.error('Error fetching low stock products:', error)
	} finally {
		loading.value = false
	}
}

onMounted(() => {
	fetchLowStock()
})

const getAlertClass = (stock: number, minStock: number) => {
	if (stock === 0) return 'bg-red-500'
	if (stock <= minStock * 0.5) return 'bg-orange-500'
	return 'bg-yellow-500'
}
</script>

<template>
	<div class="relative">
		<button
			@click="showAlerts = !showAlerts"
			class="relative p-2 rounded-lg hover:bg-gray-100 transition-colors"
			title="Alertas de inventario"
		>
			<i class="fa-solid fa-bell text-xl text-gray-600"></i>
			<span
				v-if="lowStockProducts.length > 0"
				class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full size-5 flex items-center justify-center"
			>
				{{ lowStockProducts.length }}
			</span>
		</button>

		<div
			v-if="showAlerts && lowStockProducts.length > 0"
			class="absolute right-0 top-12 w-80 bg-white shadow-xl rounded-lg border border-gray-200 z-50"
		>
			<div class="p-3 border-b border-gray-100">
				<h3 class="font-bold text-gray-800">Alertas de inventario</h3>
				<p class="text-xs text-gray-500">Productos con stock bajo</p>
			</div>
			<div class="max-h-64 overflow-y-auto">
				<div
					v-for="product in lowStockProducts"
					:key="product.id"
					class="p-3 border-b border-gray-100 hover:bg-gray-50"
				>
					<div class="flex justify-between items-start">
						<div>
							<p class="font-medium text-sm text-gray-800">{{ product.name }}</p>
							<p class="text-xs text-gray-500">SKU: {{ product.sku }}</p>
						</div>
						<span
							:class="['px-2 py-1 text-xs font-bold text-white rounded', getAlertClass(product.stock, product.min_stock)]"
						>
							{{ product.stock }} / {{ product.min_stock }}
						</span>
					</div>
				</div>
			</div>
			<div class="p-2 border-t border-gray-100">
				<router-link
					to="/inventory/products?filter=low"
					class="text-xs text-primary hover:underline block text-center"
					@click="showAlerts = false"
				>
					Ver todos los productos
				</router-link>
			</div>
		</div>

		<div
			v-if="showAlerts && lowStockProducts.length === 0 && !loading"
			class="absolute right-0 top-12 w-64 bg-white shadow-xl rounded-lg border border-gray-200 z-50 p-4 text-center"
		>
			<i class="fa-solid fa-check-circle text-green-500 text-2xl mb-2"></i>
			<p class="text-sm text-gray-600">No hay alertas de inventario</p>
		</div>
	</div>
</template>