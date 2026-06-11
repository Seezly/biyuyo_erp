<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useCustomersStore } from '@/stores/customers'
import { useToastStore } from '@/stores/toast'
import { useAuthStore } from '@/stores/auth'
import { useBusinessesStore } from '@/stores/businesses'
import { onMounted } from 'vue'

const router = useRouter()
const customersStore = useCustomersStore()
const toastStore = useToastStore()
const authStore = useAuthStore()
const businessesStore = useBusinessesStore()
const loading = ref(false)

const isSuperadmin = computed(() => authStore.user?.is_superuser === true)
const selectedBusinessId = ref<number | null>(null)

onMounted(async () => {
	if (isSuperadmin.value) {
		await businessesStore.fetchBusinesses()
	}
})

const validationSchema = toTypedSchema(
	z.object({
		name: z.string().min(1, 'El nombre es requerido'),
		phone: z
			.string()
			.regex(/^0?\d{10,11}$/, 'TelǸfono invǭlido (ej: 04241234567)')
			.or(z.literal('')),
		identification_number: z
			.string()
			.regex(/^[VEJGvejg]\d{5,9}$/, 'CǸdula invǭlida (ej: V12345678)')
			.or(z.literal('')),
	}),
)

const { handleSubmit, errors } = useForm({
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

const onSubmit = handleSubmit(async (values) => {
	loading.value = true
	try {
		const payload = { ...values } as Record<string, unknown>
		if (isSuperadmin.value && selectedBusinessId.value) {
			payload.business_id = selectedBusinessId.value
		}
		const customer = await customersStore.createCustomer(payload as any)
		if (customer) {
			// Success toast will be handled by the store
			router.push('/customers')
		}
		// Error will be handled by the store
	} catch (error) {
		toastStore.error('Error de conexi\u00f3n')
	} finally {
		loading.value = false
	}
})
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Agregar cliente</h1>
			<p>Añade un nuevo cliente al registro de tu negocio</p>
		</div>

		<form
			@submit="onSubmit"
			class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md"
		>
			<label v-if="isSuperadmin" class="w-full flex flex-col text-dark">
				Negocio *
				<select v-model="selectedBusinessId" class="py-2 px-4 rounded-xl border border-secondary text-primary">
					<option :value="null">Seleccionar negocio</option>
					<option v-for="b in businessesStore.businesses" :key="b.id" :value="b.id">
						{{ b.name }}
					</option>
				</select>
			</label>
			<label class="w-full flex flex-col text-dark">
				Nombre del cliente *
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
				<BaseInput
					v-model="identification_number"
					name="identification_number"
					placeholder="V12345678"
				/>
				<span v-if="errors.identification_number" class="text-red-500 text-sm">{{
					errors.identification_number
				}}</span>
			</label>
			<BaseButton
				:text="loading ? 'Creando...' : 'Agregar cliente'"
				:loading="loading"
				:disabled="loading"
				type="submit"
			/>
		</form>
	</section>
</template>
