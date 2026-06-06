<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useSuppliersStore } from '@/stores/suppliers'
import { useToastStore } from '@/stores/toast'
import { apiFetch } from '@/utils/helpers'

const router = useRouter()
const route = useRoute()
const suppliersStore = useSuppliersStore()
const toastStore = useToastStore()

const purchaseId = Number(route.params.purchaseId)
if (!purchaseId) {
  router.back()
}
const loading = ref(true)
const saving = ref(false)

onMounted(async () => {
	await suppliersStore.fetchSuppliers()
	try {
		const response = await apiFetch(`/api/purchases/${purchaseId}/`)
		if (response.ok) {
			const data = await response.json()
			setValues({
				supplier: data.supplier || undefined,
				total: data.total || undefined,
			})
		}
	} catch (error) {
		toastStore.error('Error al cargar la compra')
	} finally {
		loading.value = false
	}
})

const validationSchema = toTypedSchema(
	z.object({
		supplier: z.number().min(1, 'Selecciona un proveedor'),
		total: z.number().min(0, 'El total debe ser positivo').optional(),
	})
)

const { handleSubmit, errors, setValues } = useForm({
	validationSchema,
	initialValues: {
		supplier: undefined as number | undefined,
		total: undefined as number | undefined,
	},
})

const { value: supplier } = useField<number>('supplier')
const { value: total } = useField<number | undefined>('total')

const onSubmit = handleSubmit(async (values) => {
	saving.value = true
	try {
		const response = await apiFetch(`/api/purchases/${purchaseId}/`, {
			method: 'PATCH',
			body: JSON.stringify(values),
		})

		if (!response.ok) {
			const errorData = await response.json()
			toastStore.error(errorData.detail || 'Error al actualizar compra')
			return
		}

		toastStore.success('Compra actualizada correctamente')
		router.push('/suppliers/purchases')
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
			<h1 class="text-primary text-2xl font-bold">Editar compra</h1>
			<p>Actualiza la información de la compra</p>
		</div>

		<div v-if="loading" class="w-full text-center py-8">
			<p>Cargando compra...</p>
		</div>

		<div v-else>
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
				<BaseButton :text="saving ? 'Guardando...' : 'Guardar compra'" :loading="saving" :disabled="saving" type="submit" />
			</form>
		</div>
	</section>
</template>