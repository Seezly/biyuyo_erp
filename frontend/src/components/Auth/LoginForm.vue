<script setup lang="ts">
import { ref } from 'vue'

import { apiFetch } from '@/utils/helpers'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

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
		const response = await apiFetch('/api/login/', {
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
	<form action="" class="flex justify-start items-center flex-col gap-4 w-full lg:w-md">
		<label class="w-full flex flex-col text-dark">
			Correo electrónico
			<BaseInput v-model="form.email" type="email" name="email" placeholder="Correo electrónico" />
		</label>
		<label class="w-full flex flex-col text-dark mb-8">
			<div class="flex justify-between items-center">
				Contraseña
				<a href="#" class="text-primary underline text-xs font-light">¿Olvidaste tu contraseña?</a>
			</div>
			<BaseInput v-model="form.password" type="password" name="password" placeholder="Contraseña" />
		</label>
		<BaseButton @click="submit" text="Iniciar sesión" />
		<BaseButton to="/register" text="Regístrate" variant="outlined" />
	</form>
</template>
