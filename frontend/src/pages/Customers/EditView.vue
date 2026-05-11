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
const loading = ref(false)

const customerId = route.params.customerId

const validationSchema = toTypedSchema(
	z.object({
		name: z.string().min(1, 'El nombre es requerido'),
		phone: z
			.string()
			.regex(/^0?\d{10,11}$/, 'Teléfono inválido (ej: 04241234567)')
			.or(z.literal('')),
		identification_number: z
			.string()
			.regex(/^[VEJGvejg]\d{5,9}$/, 'Cédula inválida (ej: V12345678)')
			.or(z.literal('')),
	})
)

const { handleSubmit, errors, setValues } = useForm({
	validationSchema,
	initialValues: {
		name: '',
		phone: '',
		identification_number: '',
	},
})

const { value: name } = useField<string>('name')
const { value: phone } = useField<string>('phone')
const { value: identification_number } = useField<string>('identification_number')

const fetchCustomer = async () => {
	try {
		const response = await fetch(`/api/customers/${customerId}/`)
		if (response.ok) {
			const data = await response.json()
			setValues({
				name: data.name || '',
				phone: data.phone || '',
				identification_number: data.identification_number || '',
			})
		}
	} catch (error) {
		console.error('Error fetching customer:', error)
	}
}

onMounted(() => {
	fetchCustomer()
})

const onSubmit = handleSubmit(async (values) => {
	loading.value = true
	try {
		const response = await fetch(`/api/customers/${customerId}/`, {
			method: 'PATCH',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(values),
		})

		if (!response.ok) {
			const errorData = await response.json()
			toastStore.error(errorData.detail || 'Error al actualizar cliente')
			return
		}

		toastStore.success('Cliente actualizado correctamente')
		router.push('/customers')
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
			<h1 class="text-primary text-2xl font-bold">Editar cliente</h1>
			<p>Edita un cliente existente</p>
		</div>
		<form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				Nombre del cliente
				<BaseInput v-model="name" type="text" name="name" placeholder="Nombre del cliente" />
				<span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
			</label>
			<label class="w-full flex flex-col text-dark">
				Número de teléfono
				<BaseInput v-model="phone" type="tel" name="phone" placeholder="04241234567" />
				<span v-if="errors.phone" class="text-red-500 text-sm">{{ errors.phone }}</span>
			</label>
			<label class="w-full flex flex-col text-dark">
				Cédula de Identidad
				<BaseInput v-model="identification_number" name="identification_number" placeholder="V12345678" maxlength="9" />
				<span v-if="errors.identification_number" class="text-red-500 text-sm">{{ errors.identification_number }}</span>
			</label>
			<BaseButton :text="loading ? 'Guardando...' : 'Editar cliente'" :disabled="loading" type="submit" />
		</form>
	</section>
</template>