<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useToastStore } from '@/stores/toast'
import { apiFetch } from '@/utils/helpers'

const router = useRouter()
const toastStore = useToastStore()
const loading = ref(false)

const validationSchema = toTypedSchema(
	z.object({
		current_password: z.string().min(1, 'La contraseña actual es requerida'),
		new_password: z.string().min(6, 'La nueva contraseña debe tener al menos 6 caracteres'),
		confirm_password: z.string().min(1, 'Debe confirmar la contraseña'),
	}).refine((data) => data.new_password === data.confirm_password, {
		message: 'Las contraseñas no coinciden',
		path: ['confirm_password'],
	})
)

const { handleSubmit, errors } = useForm({
	validationSchema,
	initialValues: {
		current_password: '',
		new_password: '',
		confirm_password: '',
	},
})

const { value: current_password } = useField<string>('current_password')
const { value: new_password } = useField<string>('new_password')
const { value: confirm_password } = useField<string>('confirm_password')

const onSubmit = handleSubmit(async (values) => {
	loading.value = true
	try {
		const response = await apiFetch('/api/users/change-password/', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				current_password: values.current_password,
				new_password: values.new_password,
			}),
		})

		if (!response.ok) {
			const errorData = await response.json()
			toastStore.error(errorData.detail || 'Error al cambiar contraseña')
			return
		}

		toastStore.success('Contraseña cambiada correctamente')
		router.push('/profile')
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
			<h1 class="text-primary text-2xl font-bold">Cambiar contraseña</h1>
			<p>Cambia la contraseña de tu cuenta en cualquier momento</p>
		</div>
		<BaseCard variant="outlined" class="mx-auto">
			<div class="flex flex-col gap-4">
				<form @submit="onSubmit" class="flex justify-start items-start flex-col gap-4 w-md">
					<label class="w-full flex flex-col text-dark">
						Contraseña actual
						<BaseInput v-model="current_password" name="current_password" type="password" />
						<span v-if="errors.current_password" class="text-red-500 text-sm">{{ errors.current_password }}</span>
					</label>
					<label class="w-full flex flex-col text-dark">
						Contraseña nueva
						<BaseInput v-model="new_password" name="new_password" type="password" />
						<span v-if="errors.new_password" class="text-red-500 text-sm">{{ errors.new_password }}</span>
					</label>
					<label class="w-full flex flex-col text-dark">
						Repite la contraseña
						<BaseInput v-model="confirm_password" name="confirm_password" type="password" />
						<span v-if="errors.confirm_password" class="text-red-500 text-sm">{{ errors.confirm_password }}</span>
					</label>
					<BaseButton :text="loading ? 'Cambiando...' : 'Cambiar contraseña'" :loading="loading" :disabled="loading" type="submit" class="mt-4" />
				</form>
			</div>
		</BaseCard>
	</section>
</template>