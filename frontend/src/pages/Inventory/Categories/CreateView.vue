<script setup lang="ts">
import { ref } from 'vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const form = ref({
	name: '',
	is_subcategory: false,
	parent_category: null,
})
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Crear categoría</h1>
			<p>Crea nuevas categorías para organizar tu inventario</p>
		</div>
		<form action="" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				Nombre de la categoría
				<BaseInput v-model="form.name" type="text" name="name" placeholder="Nombre de la categoría" />
			</label>
			<label class="w-full flex flex-col text-dark">
				¿Es una subcategoría?
				<input type="checkbox" name="" id="" />
				<!-- <BaseInput v-model="form.name" type="text" name="name" placeholder="Nombre del producto" /> -->
			</label>
			<label class="w-full flex flex-col text-dark">
				Seleccione la categoría a la que pertenece
				<select name="category" id="" class="py-2 px-4 rounded-xl border border-secondary text-primary">
					<option value="0">Categoría 1</option>
				</select>
			</label>
			<BaseButton text="Agregar categoría" />
		</form>
	</section>
</template>
