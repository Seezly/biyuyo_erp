<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useInventoryStore } from '@/stores/inventory'
import { useToastStore } from '@/stores/toast'
import { useAuthStore } from '@/stores/auth'
import { apiFetch } from '@/utils/helpers'

const route = useRoute()
const router = useRouter()
const inventoryStore = useInventoryStore()
const toastStore = useToastStore()
const authStore = useAuthStore()
const apiFetchHelper = apiFetch

const categoryId = Number(route.params.categoryId)
if (!categoryId) {
  router.back()
}
const loading = ref(true)
const saving = ref(false)

onMounted(async () => {
	await inventoryStore.fetchCategories()
	try {
		const response = await apiFetch(`/api/categories/${categoryId}/`)
		if (response.ok) {
			const data = await response.json()
			setValues({
				name: data.name || '',
				parent_id: data.parent_id || null,
			})
		}
	} catch (error) {
		toastStore.error('Error al cargar la categoría')
	} finally {
		loading.value = false
	}
})

const validationSchema = toTypedSchema(
	z.object({
		name: z.string().min(1, 'El nombre es requerido'),
		parent_id: z.number().nullable().optional(),
	})
)

const { handleSubmit, errors, setValues } = useForm({
	validationSchema,
	initialValues: {
		name: '',
		parent_id: null as number | null,
	},
})

const { value: name } = useField<string>('name')
const { value: parent_id } = useField<number | null>('parent_id')

const onSubmit = handleSubmit(async (values) => {
	saving.value = true
	try {
		const payload: Record<string, unknown> = {
			name: values.name,
		}

		if (values.parent_id) {
			payload.parent_id = values.parent_id
		}

		const response = await apiFetch(`/api/categories/${categoryId}/`, {
			method: 'PATCH',
			body: JSON.stringify(payload),
		})

		if (!response.ok) {
			const errorData = await response.json()
			toastStore.error(errorData.detail || 'Error al actualizar categoría')
			return
		}

		toastStore.success('Categoría actualizada correctamente')
		router.push('/inventory/categories')
	} catch (error) {
		toastStore.error('Error de conexión')
	} finally {
		saving.value = false
	}
})
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

		<div v-else>
			<form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
				<label class="w-full flex flex-col text-dark">
					Nombre de la categoría *
					<BaseInput v-model="name" type="text" name="name" placeholder="Nombre de la categoría" />
					<span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
				</label>
				<label class="w-full flex flex-col text-dark">
					Categoría padre (opcional)
					<select v-model="parent_id" class="py-2 px-4 rounded-xl border border-secondary text-primary">
						<option :value="null">Sin categoría padre</option>
						<option v-for="cat in inventoryStore.categories" :key="cat.id" :value="cat.id">
							{{ cat.name }}
						</option>
					</select>
				</label>
				<BaseButton :text="saving ? 'Guardando...' : 'Guardar categoría'" :loading="saving" :disabled="saving" type="submit" />
			</form>
		</div>
	</section>
</template>