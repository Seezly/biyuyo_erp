<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import router from '@/router'

import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCheckbox from '@/components/ui/BaseCheckbox.vue'

import { apiFetch } from '@/utils/helpers'

const form = ref({
	name: '',
	is_subcategory: false,
	parent_category: null,
})

const categories = ref(null)

const getCategories = async () => {
	try {
		const response = await apiFetch('/api/categories/', {
			method: 'GET',
		})

		if (!response.ok) {
			const errorData = await response.json()
			console.error('Category fetching failed:', errorData)
			return
		}

		const data = await response.json()

		categories.value = data
	} catch (error) {
		console.error('Network error:', error)
	}
}

const submit = async () => {
	try {
		const response = await apiFetch('/api/categories/', {
			method: 'POST',
			body: JSON.stringify(form.value),
		})

		if (!response.ok) {
			const errorData = await response.json()
			console.error('Category creation failed:', errorData)
			return
		}

		window.location.reload()
	} catch (error) {
		console.error('Network error:', error)
	}
}

onBeforeMount(() => {
	getCategories()
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
			<BaseCheckbox v-model="form.is_subcategory" name="isSubcategory" text="¿Es una subcategoría?" />
			<Transition name="fade">
				<div v-if="form.is_subcategory" class="w-full max-h-64 flex flex-col gap-4">
					<label class="w-full flex flex-col text-dark">
						Seleccione la categoría a la que pertenece
						<select
							name="category"
							id=""
							class="py-2 px-4 rounded-xl border border-secondary text-primary"
						>
							<option :value="null">Seleccione una categoría</option>
							<template v-for="category in categories" :key="category.id">
								<option :value="category.id">{{ category.name }}</option>
							</template>
						</select>
					</label>
				</div>
			</Transition>
			<BaseButton text="Agregar categoría" @click="submit" />
		</form>
	</section>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
	transition: all 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
	max-height: 0;
	opacity: 0;
	overflow: hidden;
}
</style>
