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
const showDeleteAlert = ref(false)
const categoryToDelete = ref<number | null>(null)

onMounted(() => {
	search.value = (route.query.search as string) || ''
	fetchCategories()
})

const fetchCategories = () => {
	const params: {
		search?: string
		ordering?: string
		page?: string
	} = {}

	if (search.value) params.search = search.value
	if (route.query.ordering) params.ordering = route.query.ordering as string
	if (route.query.page) params.page = route.query.page as string

	inventoryStore.fetchCategories(params)
}

watch(search, () => {
	const query: Record<string, string> = {}
	if (search.value) query.search = search.value
	router.push({ query })
})

const confirmDelete = (id: number) => {
	categoryToDelete.value = id
	showDeleteAlert.value = true
}

const handleDelete = async () => {
	if (categoryToDelete.value) {
		await inventoryStore.deleteCategory(categoryToDelete.value)
		showDeleteAlert.value = false
		categoryToDelete.value = null
	}
}

const cancelDelete = () => {
	showDeleteAlert.value = false
	categoryToDelete.value = null
}

const formatDate = (dateString: string) => {
	if (!dateString) return '-'
	const date = new Date(dateString)
	return date.toLocaleDateString('es-VE', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric',
	})
}
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
				v-model="search"
				placeholder="Buscar categoría por nombre"
				class="col-span-12 lg:col-span-9"
			/>
		</div>

		<div v-if="inventoryStore.loading" class="w-full text-center py-8">
			<p>Cargando categorías...</p>
		</div>

		<div v-else-if="inventoryStore.categories.length === 0" class="w-full text-center py-8">
			<p class="text-gray-500">No hay categorías disponibles</p>
		</div>

		<div v-else class="grid grid-cols-12 gap-4 w-full">
			<BaseCard
				v-for="category in inventoryStore.categories"
				:key="category.id"
				variant="outlined"
				class="col-span-full lg:col-span-3 row-span-1"
			>
				<div class="flex flex-col gap-4 justify-start items-start">
					<div class="flex justify-between w-full items-center">
						<div class="flex flex-col gap-2">
							<h2 class="font-bold text-lg text-primary">{{ category.name }}</h2>
							<span class="text-xs text-gray-500">{{ formatDate(category.created_at) }}</span>
						</div>
						<div class="flex gap-2">
							<BaseButton
								variant="outlined"
								text=""
								icon="fa-solid fa-pencil"
								width="auto"
								:to="'/inventory/categories/edit/' + category.id"
							/>
							<BaseButton
								text=""
								icon="fa-solid fa-trash"
								width="auto"
								@click="confirmDelete(category.id)"
							/>
						</div>
					</div>
				</div>
			</BaseCard>
		</div>
	</section>

	<BaseAlert
		:visible="showDeleteAlert"
		title="Eliminar categoría"
		subtitle="Esta acción no se puede deshacer"
		description="¿Estás seguro de que deseas eliminar esta categoría?"
		variant="delete"
		:cta="'Eliminar'"
		:cancel="true"
		@update="showDeleteAlert = false"
		@close="cancelDelete"
		@next="handleDelete"
	/>
</template>
