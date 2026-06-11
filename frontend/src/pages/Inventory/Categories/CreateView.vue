<script setup lang="ts">
import { ref, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCheckbox from '@/components/ui/BaseCheckbox.vue'
import { useToastStore } from '@/stores/toast'
import { useAuthStore } from '@/stores/auth'
import { apiFetch } from '@/utils/helpers'

const router = useRouter()
const toastStore = useToastStore()
const authStore = useAuthStore()
const loading = ref(false)

interface Category {
	id: number
	name: string
}

const categories = ref<Category[]>([])

const getCategories = async () => {
	try {
		const response = await apiFetch('/api/categories/')
		if (response.ok) {
			const data = await response.json()
			categories.value = data.results || data
		}
	} catch (error) {
		console.error('Error fetching categories:', error)
	}
}

onBeforeMount(async () => {
	getCategories()
})

const validationSchema = toTypedSchema(
	z.object({
		name: z.string().min(1, 'El nombre es requerido'),
		is_subcategory: z.boolean(),
		parent_id: z.number().nullable().optional(),
	}).refine(
		(data) => !data.is_subcategory || (data.is_subcategory && data.parent_id !== null),
		{
			message: 'Seleccione una categoría padre',
			path: ['parent_id'],
		}
	)
)

const { handleSubmit, errors } = useForm({
	validationSchema,
	initialValues: {
		name: '',
		is_subcategory: false,
		parent_id: null as number | null,
	},
})

const { value: name } = useField<string>('name')
const { value: is_subcategory } = useField<boolean>('is_subcategory')
const { value: parent_id } = useField<number | null>('parent_id')

const onSubmit = handleSubmit(async (values) => {
	loading.value = true
	try {
		const payload: Record<string, unknown> = {
			name: values.name,
		}

		if (values.is_subcategory && values.parent_id) {
			payload.parent_id = values.parent_id
		}

		const response = await apiFetch('/api/categories/', {
			method: 'POST',
			body: JSON.stringify(payload),
		})

		if (!response.ok) {
			const errorData = await response.json()
			toastStore.error(errorData.detail || 'Error al crear categoría')
			return
		}

		toastStore.success('Categoría creada correctamente')
		router.push('/inventory/categories')
	} catch (error) {
		toastStore.error('Error de conexión')
	} finally {
		loading.value = false
	}
})
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Crear categoría</h1>
			<p>Crea nuevas categorías para organizar tu inventario</p>
		</div>
		<form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				Nombre de la categoría
				<BaseInput v-model="name" type="text" name="name" placeholder="Nombre de la categoría" />
				<span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
			</label>
			<BaseCheckbox v-model="is_subcategory" name="is_subcategory" text="¿Es una subcategoría?" />
			<Transition name="fade">
				<div v-if="is_subcategory" class="w-full max-h-64 flex flex-col gap-4">
					<label class="w-full flex flex-col text-dark">
						Seleccione la categoría a la que pertenece
						<select
							v-model="parent_id"
							name="parent_id"
							class="py-2 px-4 rounded-xl border border-secondary text-primary"
						>
							<option :value="null">Seleccione una categoría</option>
							<option v-for="category in categories" :key="category.id" :value="category.id">
								{{ category.name }}
							</option>
						</select>
						<span v-if="errors.parent_id" class="text-red-500 text-sm">{{ errors.parent_id }}</span>
					</label>
				</div>
			</Transition>
			<BaseButton :text="loading ? 'Creando...' : 'Agregar categoría'" :loading="loading" :disabled="loading" type="submit" />
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