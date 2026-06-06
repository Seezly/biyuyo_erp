<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useSuppliersStore } from '@/stores/suppliers'
import { useToastStore } from '@/stores/toast'
import { apiFetch } from '@/utils/helpers'

const router = useRouter()
const suppliersStore = useSuppliersStore()
const toastStore = useToastStore()
const loading = ref(false)

onMounted(async () => {
	await suppliersStore.fetchSuppliers()
})

const validationSchema = toTypedSchema(
	z.object({
		supplier: z.number().min(1, 'Selecciona un proveedor'),
		total: z.number().min(0, 'El total debe ser positivo').optional(),
	})
)

const { handleSubmit, errors } = useForm({
	validationSchema,
	initialValues: {
		supplier: undefined as number | undefined,
		total: undefined as number | undefined,
	},
})

const { value: supplier } = useField<number>('supplier')
const { value: total } = useField<number | undefined>('total')

const onSubmit = handleSubmit(async (values) => {
	loading.value = true
	try {
		const response = await apiFetch('/api/purchases/', {
			method: 'POST',
			body: JSON.stringify({
				supplier_id: values.supplier,
				total: values.total || 0,
			}),
		})

		if (!response.ok) {
			const errorData = await response.json()
			toastStore.error(errorData.detail || 'Error al crear compra')
			return
		}

		toastStore.success('Compra creada correctamente')
		router.push('/suppliers/purchases')
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
			<h1 class="text-primary text-2xl font-bold">Agregar compra</h1>
			<p>Registra una nueva compra a proveedor</p>
		</div>

		<form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				Proveedor *
				<select v-model="supplier" class="py-2 px-4 rounded-xl border border-secondary text-primary">
					<option :value="undefined">Seleccionar proveedor</option>
					<option v-for="s in suppliersStore.suppliers" :key="s.id" :value="s.id">
						{{ s.name }}
					</option>
				</select>
				<span v-if="errors.supplier" class="text-red-500 text-sm">{{ errors.supplier }}</span>
			</label>
			<label class="w-full flex flex-col text-dark">
				Total
				<BaseInput v-model="total" type="number" step="0.01" name="total" placeholder="Monto total" />
				<span v-if="errors.total" class="text-red-500 text-sm">{{ errors.total }}</span>
			</label>
			<BaseButton :text="loading ? 'Creando...' : 'Crear compra'" :disabled="loading" type="submit" />
		</form>
	</section>
</template>