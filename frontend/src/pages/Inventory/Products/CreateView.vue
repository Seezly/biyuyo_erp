<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useInventoryStore } from '@/stores/inventory'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { type ProductForm } from '@/types/product'

const router = useRouter()
const inventoryStore = useInventoryStore()

const form = ref<ProductForm>({
	name: '',
	category: 0,
	description: '',
	cost_price: 0,
	sell_price: 0,
	sku: '',
	stock: 0,
	min_stock: 0,
})

const loading = ref(false)
const error = ref('')

onMounted(async () => {
	await inventoryStore.fetchCategories()
})

const handleSubmit = async () => {
	if (!form.value.name || !form.value.sku) {
		error.value = 'El nombre y SKU son obligatorios'
		return
	}

	loading.value = true
	error.value = ''

	const result = await inventoryStore.createProduct(form.value)

	loading.value = false

	if (result) {
		router.push('/inventory/products')
	} else {
		error.value = inventoryStore.error || 'Error al crear el producto'
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Agregar producto</h1>
			<p>Añade un nuevo producto a tu inventario</p>
		</div>

		<div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
			{{ error }}
		</div>

		<form @submit.prevent="handleSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				SKU *
				<BaseInput v-model="form.sku" type="text" name="sku" placeholder="SKU" required />
			</label>
			<label class="w-full flex flex-col text-dark">
				Nombre del producto *
				<BaseInput v-model="form.name" type="text" name="name" placeholder="Nombre del producto" required />
			</label>
			<label class="w-full flex flex-col text-dark">
				Categoría
				<select v-model="form.category" class="py-2 px-4 rounded-xl border border-secondary text-primary">
					<option :value="0">Seleccionar categoría</option>
					<option v-for="cat in inventoryStore.categories" :key="cat.id" :value="cat.id">
						{{ cat.name }}
					</option>
				</select>
			</label>
			<label class="w-full flex flex-col text-dark">
				Descripción
				<BaseInput v-model="form.description" type="text" name="description" placeholder="Una descripción breve del producto" />
			</label>
			<div class="grid grid-cols-2 grid-rows-1 gap-4">
				<label class="w-full flex flex-col text-dark">
					Costo del producto
					<BaseInput v-model="form.cost_price" type="number" step="0.01" name="cost_price" placeholder="Cuánto te costó" />
				</label>
				<label class="w-full flex flex-col text-dark">
					Precio de venta
					<BaseInput v-model="form.sell_price" type="number" step="0.01" name="sell_price" placeholder="Precio al que venderás" />
				</label>
			</div>
			<div class="grid grid-cols-2 grid-rows-1 gap-4 mb-8">
				<label class="w-full flex flex-col text-dark">
					Stock
					<BaseInput v-model="form.stock" type="number" name="stock" placeholder="Cantidad en inventario" />
				</label>
				<label class="w-full flex flex-col text-dark">
					Stock mínimo
					<BaseInput v-model="form.min_stock" type="number" name="min_stock" placeholder="Cantidad mínima" />
				</label>
			</div>
			<BaseButton :text="loading ? 'Creando...' : 'Agregar producto'" :disabled="loading" />
		</form>
	</section>
</template>
