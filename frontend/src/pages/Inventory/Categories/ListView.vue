<script setup lang="ts">
import { onBeforeMount, ref, watch } from 'vue'

import BaseInput from '@/components/ui/BaseInput.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseAlert from '@/components/ui/BaseAlert.vue'

import { apiFetch } from '@/utils/helpers'

const categories = ref([])
const filteredCategories = ref([])
const search = ref('')

watch(search, () => {
	const currentCategories = categories.value
	if (search.value.length > 0) {
		filteredCategories.value = currentCategories.filter((category: any) =>
			category.name.includes(search.value),
		)
	} else {
		filteredCategories.value = currentCategories
	}
})

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
		filteredCategories.value = data
	} catch (error) {
		console.error('Network error:', error)
	}
}

const handleDelete = async (id: string | number) => {
	try {
		const response = await apiFetch(`/api/categories/${id}/`, {
			method: 'DELETE',
		})

		if (!response.ok) {
			const errorData = await response.json()
			console.error('Category deletion failed:', errorData)
			return
		}

		categories.value = categories.value.filter((category: any) => category.id !== id)
		filteredCategories.value = filteredCategories.value.filter((category: any) => category.id !== id)
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
			<h1 class="text-primary text-2xl font-bold">Lista de categorías</h1>
			<p>Administra las categorías en tu inventario</p>
		</div>
		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseButton
				to="/inventory/categories/add"
				text="Añadir categoría"
				class="col-span-12 lg:col-span-3"
			/>
			<BaseInput
				type="search"
				placeholder="Buscar categoría por nombre"
				class="col-span-12 lg:col-span-5"
				v-model="search"
			/>
			<div class="flex lg:justify-end justify-between items-center gap-2 col-span-12 lg:col-span-4">
				<label
					for="1"
					class="px-4 py-2 text-ellipsis overflow-hidden whitespace-nowrap bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition"
				>
					Todas
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
					class="px-4 py-2 text-ellipsis overflow-hidden whitespace-nowrap bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition"
				>
					Subcategorías (n)
					<input
						type="checkbox"
						class="absolute opacity-0 cursor-pointer h-full w-full"
						name="2"
						id=""
					/>
				</label>
				<label
					for="3"
					class="px-4 py-2 text-ellipsis overflow-hidden whitespace-nowrap bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-white relative transition"
				>
					Categorías (n)
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
			<template v-for="category in filteredCategories" :key="category.id">
				<BaseCard variant="outlined" class="col-span-full lg:col-span-3 row-span-1">
					<div class="flex flex-col gap-4 justify-start items-start">
						<div class="flex justify-between w-full items-center">
							<div class="flex flex-col gap-2">
								<h2 class="font-bold text-lg text-primary">{{ category.name }}</h2>
								<span class="text-xs" v-if="category.parent_id">{{ category.parent_id }}</span>
							</div>
							<div>
								<BaseButton
									variant="outlined"
									text="Editar"
									icon="fa-solid fa-pencil"
									width="auto"
									:to="'/inventory/categories/edit/' + category.id"
								/>
								<BaseButton text="Eliminar" width="auto" @click="handleDelete(category.id)" />
							</div>
						</div>
					</div>
				</BaseCard>
			</template>
		</div>
	</section>
	<BaseAlert
		title="Hola"
		subtitle="Hola de nuevo"
		:visible="true"
		variant="info"
		description="lol q mal"
	/>
</template>
