<script setup lang="ts">
import { ref } from 'vue'
import router from '@/router'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { apiFetch } from '@/utils/helpers'

interface RegisterForm {
	first_name: string
	last_name: string
	email: string
	identification_number: string
	rol: string
	phone: string
	password: string
	confirm_password: string
}

const form = ref<RegisterForm>({
	first_name: '',
	last_name: '',
	email: '',
	identification_number: '',
	rol: '',
	phone: '',
	password: '',
	confirm_password: '',
})

const submit = async () => {
	try {
		const response = await apiFetch('/api/register/', {
			method: 'POST',
			body: JSON.stringify(form.value),
		})

		if (!response.ok) {
			const errorData = await response.json()
			console.error('Register failed:', errorData)
			return
		}

		const data = await response.json()

		emit('submit', data)

		router.push({ path: '/login' })
	} catch (error) {
		console.error('Network error:', error)
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Añadir usuario</h1>
			<p>Completa los datos del nuevo usuario</p>
		</div>
		<form action="" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<div class="grid grid-cols-2 grid-rows-1 gap-4">
				<label class="w-full flex flex-col text-dark">
					Primer nombre
					<BaseInput
						v-model="form.first_name"
						type="text"
						name="name"
						placeholder="Nombre del usuario"
					/>
				</label>
				<label class="w-full flex flex-col text-dark">
					Primer apellido
					<BaseInput
						v-model="form.last_name"
						type="text"
						name="supply"
						placeholder="Apellido del usuario"
					/>
				</label>
			</div>
			<label class="w-full flex flex-col text-dark">
				Cédula de Identidad
				<BaseInput
					v-model="form.identification_number"
					type="text"
					name="identificationNumber"
					placeholder="V12345678 ó E123456789"
				/>
			</label>
			<label class="w-full flex flex-col text-dark">
				Email
				<BaseInput v-model="form.email" type="text" name="email" placeholder="Email" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Teléfono
				<BaseInput v-model="form.phone" type="text" name="phone" placeholder="Teléfono" />
			</label>
			<label for="" class="w-full flex flex-col text-dark">
				Rol
				<select
					name=""
					v-model="form.role"
					class="py-2 px-4 rounded-xl border border-secondary text-primary"
				>
					<option value="EMPLOYEE">Empleado</option>
					<option value="OWNER">Dueño</option>
				</select>
			</label>
			<div class="grid grid-cols-2 grid-rows-1 gap-4 mb-8">
				<label class="w-full flex flex-col text-dark">
					Contraseña
					<BaseInput v-model="form.password" type="password" name="password" placeholder="Contraseña" />
				</label>
				<label class="w-full flex flex-col text-dark">
					Confirmar Contraseña
					<BaseInput
						v-model="form.confirm_password"
						type="password"
						name="confirmPassword"
						placeholder="Confirmar Contraseña"
					/>
				</label>
			</div>
			<BaseButton text="Agregar usuario" />
		</form>
	</section>
</template>
