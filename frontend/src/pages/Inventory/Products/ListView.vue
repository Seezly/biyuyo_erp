<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useInventoryStore } from '@/stores/inventory'
import { useToastStore } from '@/stores/toast'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseAlert from '@/components/ui/BaseAlert.vue'

const router = useRouter()
const route = useRoute()
const inventoryStore = useInventoryStore()
const toastStore = useToastStore()

const search = ref('')
const stockFilter = ref<'all' | 'low' | 'out'>('all')
const showDeleteAlert = ref(false)
const productToDelete = ref<number | null>(null)

// Initialize filters from URL query params
onMounted(() => {
	search.value = (route.query.search as string) || ''
	stockFilter.value = ((route.query.stock as string) || 'all') as 'all' | 'low' | 'out'
	fetchProducts()
})

// Fetch products with current filter params
const fetchProducts = () => {
	const params: {
		search?: string
		stock?: string
		ordering?: string
		page?: string
	} = {}

	if (search.value) params.search = search.value

	// Stock filter: send the filter value for backend to handle
	// The backend will filter based on stock value
	if (stockFilter.value === 'low') {
		// Products where stock <= min_stock (low stock)
		// Backend filtering will be handled by the store
	} else if (stockFilter.value === 'out') {
		params.stock = '0'
	}

	if (route.query.ordering) params.ordering = route.query.ordering as string
	if (route.query.page) params.page = route.query.page as string

	inventoryStore.fetchProducts(params)
}

// Watch for filter changes and update URL
watch([search, stockFilter], () => {
	const query: Record<string, string> = {}
	if (search.value) query.search = search.value
	if (stockFilter.value !== 'all') query.stock = stockFilter.value

	router.push({ query })
}, { deep: true })

// Watch for pagination from store
watch(() => inventoryStore.pagination, () => {
	// Pagination is handled by the store
}, { deep: true })

const confirmDelete = (id: number) => {
	productToDelete.value = id
	showDeleteAlert.value = true
}

const handleDelete = async () => {
	if (productToDelete.value) {
		const result = await inventoryStore.deleteProduct(productToDelete.value)
		showDeleteAlert.value = false
		productToDelete.value = null

		if (inventoryStore.error) {
			toastStore.error('Error al eliminar el producto')
		} else {
			toastStore.success('Producto eliminado correctamente')
		}
	}
}

const cancelDelete = () => {
	showDeleteAlert.value = false
	productToDelete.value = null
}

const getStockStatus = (product: any) => {
	if (product.stock === 0) return 'Sin stock'
	if (product.stock <= product.min_stock) return 'Bajo stock'
	return 'Normal'
}

const getStockClass = (product: any) => {
	if (product.stock === 0) return 'bg-red-500'
	if (product.stock <= product.min_stock) return 'bg-yellow-500'
	return 'bg-green-500'
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Lista de productos</h1>
			<p>Administra los productos en tu inventario</p>
		</div>
		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseButton to="/inventory/products/add" text="Añadir producto" class="col-span-12 lg:col-span-3" />
			<BaseInput v-model="search" placeholder="Buscar producto por nombre o SKU" class="col-span-12 lg:col-span-5" />
			<div class="flex lg:justify-end justify-between items-center gap-2 col-span-12 lg:col-span-4">
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Todos
					<input type="radio" v-model="stockFilter" value="all" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Bajo stock ({{ inventoryStore.lowStockProducts.length }})
					<input type="radio" v-model="stockFilter" value="low" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-white relative transition cursor-pointer">
					Sin stock ({{ inventoryStore.outOfStockProducts.length }})
					<input type="radio" v-model="stockFilter" value="out" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
			</div>
		</div>

		<div v-if="inventoryStore.loading" class="w-full text-center py-8">
			<p>Cargando productos...</p>
		</div>

		<div v-else-if="inventoryStore.products.length === 0" class="w-full text-center py-8">
			<p class="text-gray-500">No hay productos disponibles</p>
		</div>

		<div v-else class="grid grid-cols-12 gap-4 w-full">
			<BaseCard v-for="product in inventoryStore.products" :key="product.id" variant="outlined" class="col-span-full lg:col-span-3 row-span-3">
				<div class="flex flex-col gap-4 justify-start items-start">
					<div class="flex justify-between w-full items-center">
						<div class="flex justify-center items-center size-10 rounded-full bg-secondary">
							<i class="fa-solid fa-barcode text-lg"></i>
						</div>
						<div class="flex flex-col gap-2">
							<span :class="['rounded-full py-2 px-4 font-bold text-sm uppercase text-white', getStockClass(product)]">
								{{ getStockStatus(product) }}
							</span>
							<p class="text-sm text-right">SKU: {{ product.sku }}</p>
						</div>
					</div>
					<div class="flex flex-col gap-2">
						<h2 class="font-bold text-2xl">{{ product.name }}</h2>
						<p class="text-sm">{{ product.description || 'Sin descripción' }}</p>
						<p class="text-xl font-bold text-primary">${{ product.sell_price }}</p>
					</div>
					<hr class="w-full" />
					<div class="flex flex-row lg:flex-col w-full justify-between items-center gap-2">
						<div class="w-full">
							<p class="text-sm">Cantidad disponible</p>
							<p class="text-lg font-bold text-primary">{{ product.stock }}</p>
						</div>
						<div class="flex w-full gap-2">
							<BaseButton :to="'/inventory/products/edit/' + product.id" text="Editar" variant="secondary" />
							<BaseButton text="Eliminar" @click="confirmDelete(product.id)" />
						</div>
					</div>
				</div>
			</BaseCard>
		</div>
	</section>

	<BaseAlert
		:visible="showDeleteAlert"
		title="Confirmar eliminación"
		subtitle="Esta acción no se puede deshacer"
		description="¿Estás seguro de que deseas eliminar este producto? Se eliminará permanentemente del inventario."
		variant="delete"
		:cta="'Eliminar'"
		:cancel="true"
		@update="showDeleteAlert = false"
		@close="cancelDelete"
		@next="handleDelete"
	/>
</template>
