<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useBillingStore } from '@/stores/billing'

const router = useRouter()
const billingStore = useBillingStore()
const loading = ref(false)

const validationSchema = toTypedSchema(
	z.object({
		name: z.string().min(1, 'El nombre es requerido'),
		price: z.number().min(0, 'El precio debe ser mayor o igual a cero'),
		max_users: z.number().min(1, 'El número máximo de usuarios debe ser al menos 1'),
		max_products: z.number().min(1, 'El número máximo de productos debe ser al menos 1'),
	}),
)

const { handleSubmit, errors } = useForm({
	validationSchema,
	initialValues: {
		name: '',
		price: 0,
		max_users: 1,
		max_products: 1,
	},
})

const { value: name } = useField<string>('name')
const { value: price } = useField<number>('price')
const { value: max_users } = useField<number>('max_users')
const { value: max_products } = useField<number>('max_products')

const onSubmit = handleSubmit(async (values) => {
	loading.value = true
	try {
		const plan = await billingStore.createPlan(values)
		if (plan) {
			// Success toast will be handled by the store
			router.push('/billing/plans')
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
			<h1 class="text-primary text-2xl font-bold">Agregar plan</h1>
			<p>Crea un nuevo plan de suscripción para tu negocio</p>
		</div>

		<form
			@submit="onSubmit"
			class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md"
		>
			<label class="w-full flex flex-col text-dark">
				Nombre del plan
				<BaseInput v-model="name" type="text" name="name" placeholder="Nombre del plan" />
				<span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
			</label>
			<label class="w-full flex flex-col text-dark">
				Precio (USD)
				<BaseInput v-model="price" type="number" name="price" placeholder="0.00" step="0.01" min="0" />
				<span v-if="errors.price" class="text-red-500 text-sm">{{ errors.price }}</span>
			</label>
			<label class="w-full flex flex-col text-dark">
				Número máximo de usuarios
				<BaseInput v-model="max_users" type="number" name="max_users" placeholder="10" min="1" />
				<span v-if="errors.max_users" class="text-red-500 text-sm">{{ errors.max_users }}</span>
			</label>
			<label class="w-full flex flex-col text-dark">
				Número máximo de productos
				<BaseInput v-model="max_products" type="number" name="max_products" placeholder="100" min="1" />
				<span v-if="errors.max_products" class="text-red-500 text-sm">{{ errors.max_products }}</span>
			</label>
			<BaseButton
				:text="loading ? 'Creando...' : 'Agregar plan'"
				:loading="loading"
				:disabled="loading"
				type="submit"
			/>
		</form>
	</section>
</template>
