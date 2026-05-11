<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '@/utils/helpers'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import type { Product } from '@/types/inventory'

const route = useRoute()
const router = useRouter()
const productId = route.params.productId as string

const product = ref<Product | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const fetchProduct = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await apiFetch(`/api/inventory/products/${productId}/`)
    if (!response.ok) throw new Error('Failed to fetch product')
    const data = await response.json()
    product.value = data
  } catch (e: any) {
    error.value = e.message
    console.error('Error fetching product:', e)
  } finally {
    loading.value = false
  }
}

const updateStock = async (newStock: number) => {
  if (!product.value) return
  try {
    const response = await apiFetch(`/api/inventory/products/${productId}/`, {
      method: 'PATCH',
      body: JSON.stringify({ stock: newStock })
    })
    if (!response.ok) throw new Error('Failed to update stock')
    const data = await response.json()
    product.value = data
  } catch (e: any) {
    error.value = e.message
    console.error('Error updating stock:', e)
  }
}

const increaseStock = () => {
  if (product.value) {
    updateStock(product.value.stock + 1)
  }
}

const decreaseStock = () => {
  if (product.value && product.value.stock > 0) {
    updateStock(product.value.stock - 1)
  }
}

const generateAnalysis = () => {
  // Navigate to reports page for analysis
  router.push({ name: 'Reports' })
}

onMounted(() => {
  fetchProduct()
})
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
			<div class="flex lg:justify-end justify-between items-center gap-2 col-span-12 lg:col-span-6">
				<label
					for="1"
					class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition"
				>
					Todos
					<input
						type="checkbox"
						class="absolute opacity-0 cursor-pointer h-full w-full"
						name="1"
						id=""
						checked
					/>
				</label>
				<label
					for="2"
					class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition"
				>
					Bajo stock (n)
					<input
						type="checkbox"
						class="absolute opacity-0 cursor-pointer h-full w-full"
						name="2"
						id=""
					/>
				</label>
				<label
					for="3"
					class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-white relative transition"
				>
					Sin stock (n)
					<input
						type="checkbox"
						class="absolute opacity-0 cursor-pointer h-full w-full"
						name="3"
						id=""
					/>
				</label>
			</div>
		</div>
		<div class="grid grid-cols-12 gap-4 w-full">
			<BaseCard variant="outlined" class="col-span-full lg:col-span-3 row-span-3">
				<div class="flex flex-col gap-4 justify-start items-start">
					<div class="flex justify-between w-full items-center">
						<div class="flex justify-center items-center size-10 rounded-full bg-secondary">
							<i class="fa-solid fa-barcode text-lg"></i>
						</div>
						<div class="flex flex-col gap-2">
							<span class="rounded-full py-2 px-4 bg-secondary font-bold text-sm uppercase"
								>low stock</span
							>
							<p class="text-sm text-right">SKU: 12345</p>
						</div>
					</div>
					<div class="flex flex-col gap-2">
						<h2 class="font-bold text-2xl">Organic product in the business</h2>
						<p class="text-sm">Some variant for the product</p>
						<p class="text-xl font-bold text-primary">$100</p>
					</div>
					<hr />
					<div class="flex flex-row lg:flex-col w-full justify-between items-center gap-2">
						<div class="w-full">
							<p class="text-sm">Cantidad disponible</p>
							<p class="text-lg font-bold text-primary">10</p>
						</div>
						<div class="flex w-full gap-2">
							<BaseButton text="-" variant="secondary" @click="decreaseStock" />
							<BaseButton text="+" @click="increaseStock" />
						</div>
					</div>
				</div>
			</BaseCard>
		</div>
		<div class="flex justify-between items-center w-full gap-8">
			<BaseButton to="/inventory/all" text="Ver todos los productos" />
			<BaseButton to="/inventory/categories" text="Ver todas las categorías" variant="outlined" />
		</div>
		<div class="w-full">
			<BaseCard>
				<div class="flex flex-col lg:flex-row lg:items-center lg:justify-start w-full gap-4">
					<div><i class="fa-solid fa-square-poll-vertical text-4xl text-white"></i></div>
					<div>
						<h2 class="text-2xl mb-2 text-white font-bold">Análisis de inventario</h2>
						<p class="text-sm">
							Basado en las ventas de la semana anterior, se te acabarán los
							<span class="font-medium text-white">Granos de Café Sublime 800gr</span> en 4 días.
						</p>
					</div>
					<div class="lg:ml-auto">
						<BaseButton text="Generar Análisis" variant="secondary" />
					</div>
				</div>
			</BaseCard>
		</div>
	</section>
</template>
