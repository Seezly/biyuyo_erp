<script setup lang="ts">
import { ref } from 'vue'

import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

import { type ProductForm } from '@/types/product'

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
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Agregar producto</h1>
			<p>Añade un nuevo producto a tu inventario</p>
		</div>
		<form action="" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				SKU
				<BaseInput v-model="form.sku" type="text" name="name" placeholder="SKU" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Nombre del producto
				<BaseInput v-model="form.name" type="text" name="name" placeholder="Nombre del producto" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Categoría
				<select name="category" id="" class="py-2 px-4 rounded-xl border border-secondary text-primary">
					<option value="0">Categoría 1</option>
				</select>
			</label>
			<label class="w-full flex flex-col text-dark">
				Descripción
				<BaseInput
					v-model="form.description"
					type="text"
					name="name"
					placeholder="Una descripción breve del producto"
				/>
			</label>
			<div class="grid grid-cols-2 grid-rows-1 gap-4">
				<label class="w-full flex flex-col text-dark">
					Costo del producto
					<BaseInput
						v-model="form.cost_price"
						type="text"
						name="name"
						placeholder="Cuánto te costó el producto"
					/>
				</label>
				<label class="w-full flex flex-col text-dark">
					Precio de venta
					<BaseInput
						v-model="form.sell_price"
						type="text"
						name="name"
						placeholder="Precio al que venderás el producto"
					/>
				</label>
			</div>
			<div class="grid grid-cols-2 grid-rows-1 gap-4 mb-8">
				<label class="w-full flex flex-col text-dark">
					Stock
					<BaseInput v-model="form.stock" type="text" name="name" placeholder="Cantidad en inventario" />
				</label>
				<label class="w-full flex flex-col text-dark">
					Stock mínimo
					<BaseInput
						v-model="form.min_stock"
						type="text"
						name="name"
						placeholder="Cantidad mínima en inventario del producto"
					/>
				</label>
			</div>
			<BaseButton text="Agregar producto" />
		</form>
	</section>
</template>
