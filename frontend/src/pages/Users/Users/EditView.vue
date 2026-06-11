<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const toastStore = useToastStore()
const loading = ref(false)

const userId = Number(route.params.userId)
if (!userId) {
	router.back()
}

const validationSchema = toTypedSchema(
	z
		.object({
			first_name: z.string().min(1, 'El nombre es requerido'),
			last_name: z.string().min(1, 'El apellido es requerido'),
			identification_number: z
				.string()
				.min(1, 'La identificación es requerida')
				.regex(/^[VEJGvejg]\d{5,9}$/, 'Formato: V12345678 o E123456789'),
			email: z.string().min(1, 'El email es requerido').email('Email inválido'),
			phone: z.string().min(1, 'El teléfono es requerido'),
			role: z.string().min(1, 'El rol es requerido'),
			password: z.string().optional(),
			confirm_password: z.string().optional(),
		})
		.refine((data) => !data.password || data.password === data.confirm_password, {
			message: 'Las contraseñas no coinciden',
			path: ['confirm_password'],
		}),
)

const { handleSubmit, errors, setValues } = useForm({
	validationSchema,
	initialValues: {
		first_name: '',
		last_name: '',
		identification_number: '',
		email: '',
		phone: '',
		role: 'EMPLOYEE',
		password: '',
		confirm_password: '',
	},
})

const { value: first_name } = useField<string>('first_name')
const { value: last_name } = useField<string>('last_name')
const { value: identification_number } = useField<string>('identification_number')
const { value: email } = useField<string>('email')
const { value: phone } = useField<string>('phone')
const { value: role } = useField<string>('role')
const { value: password } = useField<string>('password')
const { value: confirm_password } = useField<string>('confirm_password')

const fetchUser = async () => {
	try {
		const user = await authStore.fetchUserById(userId)
		if (user) {
			setValues({
				first_name: user.first_name || '',
				last_name: user.last_name || '',
				identification_number: user.identification_number || '',
				email: user.email || '',
				phone: user.phone || '',
				role: user.role || 'EMPLOYEE',
				password: '',
				confirm_password: '',
			})
		}
	} catch (error) {
		toastStore.error('Error al cargar el usuario')
	}
}

onMounted(() => {
	fetchUser()
})

const onSubmit = handleSubmit(async (values) => {
	loading.value = true
	try {
		const payload: Record<string, any> = {
			first_name: values.first_name,
			last_name: values.last_name,
			identification_number: values.identification_number,
			email: values.email,
			phone: values.phone,
			role: values.role,
		}

		if (values.password) {
			payload.password = values.password
		}

		const updatedUser = await authStore.updateUser(userId, payload)
		if (updatedUser) {
			router.push('/users')
		}
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
			<h1 class="text-primary text-2xl font-bold">Editar usuario</h1>
			<p>Actualiza los datos del usuario</p>
		</div>
		<form
			@submit="onSubmit"
			class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md"
		>
			<div class="grid grid-cols-2 grid-rows-1 gap-4">
				<label class="w-full flex flex-col text-dark">
					Primer nombre
					<BaseInput v-model="first_name" type="text" name="first_name" placeholder="Nombre" />
					<span v-if="errors.first_name" class="text-red-500 text-sm">{{ errors.first_name }}</span>
				</label>
				<label class="w-full flex flex-col text-dark">
					Primer apellido
					<BaseInput v-model="last_name" type="text" name="last_name" placeholder="Apellido" />
					<span v-if="errors.last_name" class="text-red-500 text-sm">{{ errors.last_name }}</span>
				</label>
			</div>
			<label class="w-full flex flex-col text-dark">
				Cédula de Identidad
				<BaseInput
					v-model="identification_number"
					type="text"
					name="identification_number"
					placeholder="V12345678"
				/>
				<span v-if="errors.identification_number" class="text-red-500 text-sm">{{
					errors.identification_number
				}}</span>
			</label>
			<label class="w-full flex flex-col text-dark">
				Email
				<BaseInput v-model="email" type="email" name="email" placeholder="Email" />
				<span v-if="errors.email" class="text-red-500 text-sm">{{ errors.email }}</span>
			</label>
			<label class="w-full flex flex-col text-dark">
				Teléfono
				<BaseInput v-model="phone" type="text" name="phone" placeholder="Teléfono" />
				<span v-if="errors.phone" class="text-red-500 text-sm">{{ errors.phone }}</span>
			</label>
			<label class="w-full flex flex-col text-dark">
				Rol
				<select v-model="role" class="py-2 px-4 rounded-xl border border-secondary text-primary">
					<option value="EMPLOYEE">Empleado</option>
					<option value="OWNER">Dueño</option>
				</select>
				<span v-if="errors.role" class="text-red-500 text-sm">{{ errors.role }}</span>
			</label>
			<div class="grid grid-cols-2 grid-rows-1 gap-4 mb-8">
				<label class="w-full flex flex-col text-dark">
					Contraseña (opcional)
					<BaseInput v-model="password" type="password" name="password" placeholder="Nueva contraseña" />
					<span v-if="errors.password" class="text-red-500 text-sm">{{ errors.password }}</span>
				</label>
				<label class="w-full flex flex-col text-dark">
					Confirmar Contraseña
					<BaseInput
						v-model="confirm_password"
						type="password"
						name="confirm_password"
						placeholder="Confirmar"
					/>
					<span v-if="errors.confirm_password" class="text-red-500 text-sm">{{
						errors.confirm_password
					}}</span>
				</label>
			</div>
			<BaseButton
				:text="loading ? 'Guardando...' : 'Editar usuario'"
				:loading="loading"
				:disabled="loading"
				type="submit"
			/>
		</form>
	</section>
</template>
