<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const route = useRoute()
const toastStore = useToastStore()
const loading = ref(true)
const saving = ref(false)

const supplierId = route.params.supplierId

const validationSchema = toTypedSchema(
	z.object({
		name: z.string().min(1, 'El nombre es requerido'),
		rif: z.string().min(1, 'El RIF es requerido').regex(/^[JGVEjgve]-\d{8}-\d$/, 'RIF inválido'),
		email: z.string().email('Email inválido').or(z.literal('')),
		address: z.string().optional(),
		phone: z.string().optional(),
	})
)

const { handleSubmit, errors, setValues } = useForm({
	validationSchema,
	initialValues: {
		name: '',
		rif: '',
		email: '',
		address: '',
		phone: '',
	},
})

const { value: name } = useField<string>('name')
const { value: rif } = useField<string>('rif')
const { value: email } = useField<string>('email')
const { value: address } = useField<string>('address')
const { value: phone } = useField<string>('phone')

const fetchSupplier = async () => {
	try {
		const response = await fetch(`/api/suppliers/${supplierId}/`)
		if (response.ok) {
			const data = await response.json()
			setValues({
				name: data.name || '',
				rif: data.rif || '',
				email: data.email || '',
				address: data.address || '',
				phone: data.phone || '',
			})
		}
	} catch (error) {
		toastStore.error('Error al cargar el proveedor')
	} finally {
		loading.value = false
	}
}

onMounted(() => {
	fetchSupplier()
})

const onSubmit = handleSubmit(async (values) => {
	saving.value = true
	try {
		const response = await fetch(`/api/suppliers/${supplierId}/`, {
			method: 'PATCH',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(values),
		})

		if (!response.ok) {
			const errorData = await response.json()
			toastStore.error(errorData.detail || 'Error al actualizar proveedor')
			return
		}

		toastStore.success('Proveedor actualizado correctamente')
		router.push('/suppliers')
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
			<h1 class="text-primary text-2xl font-bold">Editar proveedor</h1>
			<p>Actualiza los datos del proveedor</p>
		</div>

		<div v-if="loading" class="w-full text-center py-8">
			<p>Cargando proveedor...</p>
		</div>

		<div v-else>
			<form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
				<label class="w-full flex flex-col text-dark">
					Nombre del proveedor *
					<BaseInput v-model="name" type="text" name="name" placeholder="Nombre del proveedor" />
					<span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
				</label>
				<label class="w-full flex flex-col text-dark">
					RIF *
					<BaseInput v-model="rif" type="text" name="rif" placeholder="J-12345678-9" />
					<span v-if="errors.rif" class="text-red-500 text-sm">{{ errors.rif }}</span>
				</label>
				<label class="w-full flex flex-col text-dark">
					Email
					<BaseInput v-model="email" type="email" name="email" placeholder="Email del proveedor" />
					<span v-if="errors.email" class="text-red-500 text-sm">{{ errors.email }}</span>
				</label>
				<label class="w-full flex flex-col text-dark">
					Dirección
					<BaseInput v-model="address" type="text" name="address" placeholder="Dirección del proveedor" />
				</label>
				<label class="w-full flex flex-col text-dark">
					Teléfono
					<BaseInput v-model="phone" type="tel" name="phone" placeholder="Teléfono del proveedor" />
				</label>
				<BaseButton :text="saving ? 'Guardando...' : 'Guardar proveedor'" :disabled="saving" type="submit" />
			</form>
		</div>
	</section>
</template>