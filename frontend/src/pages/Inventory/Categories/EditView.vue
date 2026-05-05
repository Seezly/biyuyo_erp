<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInventoryStore } from '@/stores/inventory'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { apiFetch } from '@/utils/helpers'

const route = useRoute()
const router = useRouter()
const inventoryStore = useInventoryStore()

const categoryId = Number(route.params.id)
const category = ref<any>(null)

const form = ref({
	name: '',
	parent_id: null as number | null,
})

const loading = ref(true)
const saving = ref(false)
const error = ref('')

onMounted(async () => {
	await inventoryStore.fetchCategories()

	try {
		const response = await apiFetch(`/api/categories/${categoryId}/`)
		if (response.ok) {
			const data = await response.json()
			category.value = data
			form.value = {
				name: data.name,
				parent_id: data.parent_id || null,
			}
		} else {
			error.value = 'Categoría no encontrada'
		}
	} catch (e: any) {
		error.value = 'Error al cargar la categoría'
	} finally {
		loading.value = false
	}
})

const handleSubmit = async () => {
	if (!form.value.name) {
		error.value = 'El nombre es obligatorio'
		return
	}

	saving.value = true
	error.value = ''

	await inventoryStore.updateCategory(categoryId, {
		name: form.value.name,
		parent_id: form.value.parent_id || undefined,
	})

	saving.value = false

	if (!inventoryStore.error) {
		router.push('/inventory/categories')
	} else {
		error.value = inventoryStore.error || 'Error al actualizar la categoría'
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Editar categoría</h1>
			<p>Actualiza la categoría para mantener tu inventario al día</p>
		</div>

		<div v-if="loading" class="w-full text-center py-8">
			<p>Cargando categoría...</p>
		</div>

		<div v-else-if="error && !form.name" class="w-full text-center py-8">
			<p class="text-red-500">{{ error }}</p>
		</div>

		<div v-else>
			<div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
				{{ error }}
			</div>

			<form @submit.prevent="handleSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
				<label class="w-full flex flex-col text-dark">
					Nombre de la categoría *
					<BaseInput
						v-model="form.name"
						type="text"
						name="name"
						placeholder="Nombre de la categoría"
						required
					/>
				</label>
				<label class="w-full flex flex-col text-dark">
					Categoría padre (opcional)
					<select v-model="form.parent_id" class="py-2 px-4 rounded-xl border border-secondary text-primary">
						<option :value="null">Sin categoría padre</option>
						<option v-for="cat in inventoryStore.categories" :key="cat.id" :value="cat.id">
							{{ cat.name }}
						</option>
					</select>
				</label>
				<BaseButton :text="saving ? 'Guardando...' : 'Guardar categoría'" :disabled="saving" />
			</form>
		</div>
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
