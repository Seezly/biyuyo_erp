<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useInventoryStore } from '@/stores/inventory'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'

const inventoryStore = useInventoryStore()
const loading = ref(true)

onMounted(async () => {
  await inventoryStore.fetchProducts()
  loading.value = false
})

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('es-VE', {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Inventario</h1>
			<p>Consulta y gestiona el inventario en tiempo real</p>
		</div>
		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseButton
				to="/inventory/products/add"
				text="Añadir producto"
				class="col-span-12 lg:col-span-3"
			/>
			<BaseButton
				to="/inventory/categories/add"
				text="Añadir categoría"
				class="col-span-12 lg:col-span-3"
			/>
		</div>

		<div v-if="loading" class="w-full text-center py-8">
			<p>Cargando inventario...</p>
		</div>

		<template v-else>
			<div class="grid grid-cols-12 gap-4 w-full">
				<BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
					<div class="flex flex-col gap-2">
						<h3 class="text-sm text-gray-500 uppercase tracking-wider">Total productos</h3>
						<p class="text-3xl font-bold text-primary">{{ inventoryStore.products.length }}</p>
					</div>
				</BaseCard>
				<BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
					<div class="flex flex-col gap-2">
						<h3 class="text-sm text-gray-500 uppercase tracking-wider">Stock bajo</h3>
						<p class="text-3xl font-bold text-orange-500">{{ inventoryStore.lowStockProducts.length }}</p>
					</div>
				</BaseCard>
				<BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
					<div class="flex flex-col gap-2">
						<h3 class="text-sm text-gray-500 uppercase tracking-wider">Sin stock</h3>
						<p class="text-3xl font-bold text-red-500">{{ inventoryStore.outOfStockProducts.length }}</p>
					</div>
				</BaseCard>
			</div>

			<div v-if="inventoryStore.lowStockProducts.length > 0" class="w-full">
				<h2 class="text-primary text-lg font-semibold mb-4">Productos con stock bajo</h2>
				<div class="grid grid-cols-12 gap-4 w-full">
					<BaseCard
						v-for="product in inventoryStore.lowStockProducts.slice(0, 4)"
						:key="product.id"
						variant="outlined"
						class="col-span-12 lg:col-span-3"
					>
						<div class="flex flex-col gap-2">
							<h3 class="font-bold text-lg">{{ product.name }}</h3>
							<p class="text-sm text-gray-500">SKU: {{ product.sku }}</p>
							<p class="text-xl font-bold text-primary">{{ formatCurrency(product.sell_price) }}</p>
							<div class="flex justify-between items-center">
								<p class="text-sm">Stock: <span class="font-bold" :class="product.stock === 0 ? 'text-red-500' : 'text-orange-500'">{{ product.stock }}</span></p>
								<p class="text-sm text-gray-500">Mín: {{ product.min_stock }}</p>
							</div>
						</div>
					</BaseCard>
				</div>
			</div>
		</template>

		<div class="flex justify-between items-center w-full gap-8">
			<BaseButton to="/inventory/all" text="Ver todos los productos" />
			<BaseButton to="/inventory/categories" text="Ver todas las categorías" variant="outlined" />
		</div>
	</section>
</template>
