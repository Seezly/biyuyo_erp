<script setup lang="ts">
import { ref } from 'vue'

import { apiFetch } from '@/utils/helpers'

import ButtonItem from '@/components/ui/ButtonItem.vue'
import InputItem from '@/components/ui/InputItem.vue'

interface LoginForm {
	email: string
	password: string
}

const emit = defineEmits(['submit'])

const form = ref<LoginForm>({
	email: '',
	password: '',
})

const submit = async () => {
	try {
		const response = await apiFetch('http://localhost:8000/api/login/', {
			method: 'POST',
			body: JSON.stringify(form.value),
		})

		if (!response.ok) {
			const errorData = await response.json()
			console.error('Login failed:', errorData)
			return
		}

		const data = await response.json()

		emit('submit', data.user)
	} catch (error) {
		console.error('Network error:', error)
	}
}
</script>

<template>
	<form action="" class="flex justify-start items-center flex-col gap-4 w-md">
		<label class="w-full flex flex-col text-dark">
			Correo electrónico
			<InputItem v-model="form.email" type="email" name="email" placeholder="Correo electrónico" />
		</label>
		<label class="w-full flex flex-col text-dark mb-8">
			<div class="flex justify-between items-center">
				Contraseña
				<a href="#" class="text-primary underline text-xs font-light">¿Olvidaste tu contraseña?</a>
			</div>
			<InputItem v-model="form.password" type="password" name="password" placeholder="Contraseña" />
		</label>
		<ButtonItem @click.prevent="submit" text="Iniciar sesión" />
		<ButtonItem text="Regístrate" type="outlined" />
	</form>
</template>
