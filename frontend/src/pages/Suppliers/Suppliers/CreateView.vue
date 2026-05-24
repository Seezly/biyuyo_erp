<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useSuppliersStore } from '@/stores/suppliers'

const router = useRouter()
const suppliersStore = useSuppliersStore()
const loading = ref(false)

const validationSchema = toTypedSchema(
	z.object({
		name: z.string().min(1, 'El nombre es requerido'),
		rif: z.string().min(1, 'El RIF es requerido').regex(/^[JGVEjgve]-\d{8}-\d$/, 'RIF invǭlido (ej: J-12345678-9)'),
		email: z.string().email('Email invǭlido').or(z.literal('')),
		address: z.string().optional(),
		phone: z.string().optional(),
	})
)

const { handleSubmit, errors } = useForm({
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

const onSubmit = handleSubmit(async (values) => {
	loading.value = true
	try {
		const supplier = await suppliersStore.createSupplier(values)
		if (supplier) {
			// Success toast will be handled by the store
			router.push('/suppliers')
		}
		// Error will be handled by the store
	} catch (error) {
		// Error will be handled by the store
	} finally {
		loading.value = false
	}
})
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Añadir proveedor</h1>
			<p>Completa los datos del nuevo proveedor</p>
		</div>

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
			<BaseButton :text="loading ? 'Creando...' : 'Agregar proveedor'" :disabled="loading" type="submit" />
		</form>
	</section>
</template>