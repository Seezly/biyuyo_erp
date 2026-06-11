<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseCheckbox from '@/components/ui/BaseCheckbox.vue'
import { useSuppliersStore } from '@/stores/suppliers'
import { useAuthStore } from '@/stores/auth'


const router = useRouter()
const route = useRoute()
const suppliersStore = useSuppliersStore()
const authStore = useAuthStore()
const loading = ref(true)
const saving = ref(false)

const supplierId = Number(route.params.supplierId)
if (!supplierId) {
  router.back()
}

const validationSchema = toTypedSchema(
	z.object({
		name: z.string().min(1, 'El nombre es requerido'),
		rif: z.string().min(1, 'El RIF es requerido').regex(/^[JGVEjgve]-\d{8}-\d$/, 'RIF inválido'),
		email: z.string().min(1, 'El email es requerido').email('Email inválido'),
		address: z.string().min(1, 'La dirección es requerida'),
		phone: z.string().min(1, 'El teléfono es requerido'),
		is_active: z.boolean(),
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
		is_active: true,
	},
})

const { value: name } = useField<string>('name')
const { value: rif } = useField<string>('rif')
const { value: email } = useField<string>('email')
const { value: address } = useField<string>('address')
const { value: phone } = useField<string>('phone')
const { value: is_active } = useField<boolean>('is_active')

const fetchSupplier = async () => {
	loading.value = true
	try {
		const supplier = await suppliersStore.fetchSupplier(supplierId)
		if (supplier) {
			setValues({
				name: supplier.name || '',
				rif: supplier.rif || '',
				email: supplier.email || '',
				address: supplier.address || '',
				phone: supplier.phone || '',
				is_active: supplier.is_active ?? true,
			})
		}
	} finally {
		loading.value = false
	}
}

onMounted(async () => {
	fetchSupplier()
})

const onSubmit = handleSubmit(async (values) => {
	saving.value = true
	try {
		const updatedSupplier = await suppliersStore.updateSupplier(supplierId, values)
		if (updatedSupplier) {
			// Success toast will be handled by the store
			router.push('/suppliers')
		}
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
					Email *
					<BaseInput v-model="email" type="email" name="email" placeholder="Email del proveedor" />
					<span v-if="errors.email" class="text-red-500 text-sm">{{ errors.email }}</span>
				</label>
				<label class="w-full flex flex-col text-dark">
					Dirección *
					<BaseInput v-model="address" type="text" name="address" placeholder="Dirección del proveedor" />
					<span v-if="errors.address" class="text-red-500 text-sm">{{ errors.address }}</span>
				</label>
				<label class="w-full flex flex-col text-dark">
					Teléfono *
					<BaseInput v-model="phone" type="tel" name="phone" placeholder="Teléfono del proveedor" />
					<span v-if="errors.phone" class="text-red-500 text-sm">{{ errors.phone }}</span>
				</label>
				<BaseCheckbox v-model="is_active" name="is_active" text="Activo" />
				<BaseButton :text="saving ? 'Guardando...' : 'Guardar proveedor'" :loading="saving" :disabled="saving" type="submit" />
			</form>
		</div>
	</section>
</template>