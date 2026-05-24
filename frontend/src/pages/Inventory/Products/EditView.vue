<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useInventoryStore } from '@/stores/inventory'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const route = useRoute()
const inventoryStore = useInventoryStore()
const toastStore = useToastStore()

const productId = Number(route.params.productId)
const loading = ref(true)
const saving = ref(false)

onMounted(async () => {
	await inventoryStore.fetchCategories()
	try {
		const product = await inventoryStore.fetchProductById(productId)
		if (product) {
			setValues({
				sku: product.sku || '',
				name: product.name || '',
				category_id: product.category_id || undefined,
				description: product.description || '',
				cost_price: product.cost_price || undefined,
				sell_price: product.sell_price || undefined,
				stock: product.stock || undefined,
				min_stock: product.min_stock || undefined,
			})
		}
	} catch (error) {
		toastStore.error('Error al cargar el producto')
	} finally {
		loading.value = false
	}
})

const validationSchema = toTypedSchema(
	z.object({
		sku: z.string().min(1, 'El SKU es requerido'),
		name: z.string().min(1, 'El nombre es requerido'),
		category_id: z.number().optional(),
		description: z.string().optional(),
		cost_price: z.number().min(0, 'Debe ser positivo').optional(),
		sell_price: z.number().min(0, 'Debe ser positivo').optional(),
		stock: z.number().int('Debe ser entero').min(0, 'Debe ser positivo').optional(),
		min_stock: z.number().int('Debe ser entero').min(0, 'Debe ser positivo').optional(),
	})
)

const { handleSubmit, errors, setValues } = useForm({
	validationSchema,
	initialValues: {
		sku: '',
		name: '',
		category_id: undefined as number | undefined,
		description: '',
		cost_price: undefined as number | undefined,
		sell_price: undefined as number | undefined,
		stock: undefined as number | undefined,
		min_stock: undefined as number | undefined,
	},
})

const { value: sku } = useField<string>('sku')
const { value: name } = useField<string>('name')
const { value: category_id } = useField<number | undefined>('category_id')
const { value: description } = useField<string>('description')
const { value: cost_price } = useField<number | undefined>('cost_price')
const { value: sell_price } = useField<number | undefined>('sell_price')
const { value: stock } = useField<number | undefined>('stock')
const { value: min_stock } = useField<number | undefined>('min_stock')

const onSubmit = handleSubmit(async (values) => {
	saving.value = true
	try {
		const payload = {
			...values,
			category_id: values.category_id ?? undefined,
		}

		const updatedProduct = await inventoryStore.updateProduct(productId, payload)
		if (updatedProduct) {
			// Success toast will be handled by the store
			router.push('/inventory/products')
		}
	} catch (error) {
		toastStore.error('Error de conexi��n')
	} finally {
		saving.value = false
	}
})
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Editar producto</h1>
			<p>Modifica un producto de tu inventario</p>
		</div>

		<div v-if="loading" class="w-full text-center py-8">
			<p>Cargando producto...</p>
		</div>

		<div v-else>
			<form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
				<label class="w-full flex flex-col text-dark">
					SKU *
					<BaseInput v-model="sku" type="text" name="sku" placeholder="SKU" />
					<span v-if="errors.sku" class="text-red-500 text-sm">{{ errors.sku }}</span>
				</label>
				<label class="w-full flex flex-col text-dark">
					Nombre del producto *
					<BaseInput v-model="name" type="text" name="name" placeholder="Nombre del producto" />
					<span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
				</label>
				<label class="w-full flex flex-col text-dark">
					Categoría
					<select v-model="category_id" class="py-2 px-4 rounded-xl border border-secondary text-primary">
						<option :value="undefined">Seleccionar categoría</option>
						<option v-for="cat in inventoryStore.categories" :key="cat.id" :value="cat.id">
							{{ cat.name }}
						</option>
					</select>
				</label>
				<label class="w-full flex flex-col text-dark">
					Descripción
					<BaseInput v-model="description" type="text" name="description" placeholder="Una descripción breve" />
				</label>
				<div class="grid grid-cols-2 grid-rows-1 gap-4">
					<label class="w-full flex flex-col text-dark">
						Costo del producto
						<BaseInput v-model="cost_price" type="number" step="0.01" name="cost_price" placeholder="0.00" />
						<span v-if="errors.cost_price" class="text-red-500 text-sm">{{ errors.cost_price }}</span>
					</label>
					<label class="w-full flex flex-col text-dark">
						Precio de venta
						<BaseInput v-model="sell_price" type="number" step="0.01" name="sell_price" placeholder="0.00" />
						<span v-if="errors.sell_price" class="text-red-500 text-sm">{{ errors.sell_price }}</span>
					</label>
				</div>
				<div class="grid grid-cols-2 grid-rows-1 gap-4 mb-8">
					<label class="w-full flex flex-col text-dark">
						Stock
						<BaseInput v-model="stock" type="number" name="stock" placeholder="0" />
						<span v-if="errors.stock" class="text-red-500 text-sm">{{ errors.stock }}</span>
					</label>
					<label class="w-full flex flex-col text-dark">
						Stock mínimo
						<BaseInput v-model="min_stock" type="number" name="min_stock" placeholder="0" />
						<span v-if="errors.min_stock" class="text-red-500 text-sm">{{ errors.min_stock }}</span>
					</label>
				</div>
				<BaseButton :text="saving ? 'Guardando...' : 'Guardar producto'" :disabled="saving" type="submit" />
			</form>
		</div>
	</section>
</template>