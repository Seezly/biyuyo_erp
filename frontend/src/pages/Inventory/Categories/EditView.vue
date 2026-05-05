<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router'

import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCheckbox from '@/components/ui/BaseCheckbox.vue'

import { apiFetch } from '@/utils/helpers'

const route = useRoute()

const category = ref(null)

const form = ref({
	name: category.value?.name ?? '',
	is_subcategory: category.value?.parent_name ? true : false,
	parent_category: category.value?.parent_name ?? null,
})

const getCategory = async () => {
	try {
		const response = await apiFetch(`/api/categories/route.params.categoryId/`, {
			method: 'GET',
		})

		if (!response.ok) {
			const errorData = await response.json()
			console.error('Category fetching failed:', errorData)
			return
		}

		const data = await response.json()

		category.value = data
	} catch (error) {
		console.error('Network error:', error)
	}
}

onBeforeMount(() => {
	getCategory()
})
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Editar categoría</h1>
			<p>Actualiza la categoría para mantener tu inventario al día</p>
		</div>
		<form action="" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				Nombre de la categoría
				<BaseInput
					v-model="form.name"
					type="text"
					name="name"
					placeholder="Nombre de la categoría"
					:value="category.name"
				/>
			</label>
			<BaseCheckbox
				v-model="form.is_subcategory"
				name="isSubcategory"
				text="¿Es una subcategoría?"
				:checked="category.is_subcategory"
			/>
			<Transition name="fade">
				<div v-if="form.is_subcategory" class="w-full max-h-64 flex flex-col gap-4">
					<label class="w-full flex flex-col text-dark">
						Seleccione la categoría a la que pertenece
						<select
							name="category"
							id=""
							class="py-2 px-4 rounded-xl border border-secondary text-primary"
							:value="category.parent_id"
						>
							<option value="0">Categoría 1</option>
						</select>
					</label>
				</div>
			</Transition>
			<BaseButton text="Editar categoría" />
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
