<script setup lang="ts">
import { ref } from 'vue'
import router from '@/router'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { apiFetch } from '@/utils/helpers'

interface CustomerForm {
	name: string
	phone: string
	identification_number: string
}
const emit = defineEmits(['submit', 'incrementStep'])

const form = ref<CustomerForm>({
	name: '',
	phone: '',
	identification_number: '',
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
			<h1 class="text-primary text-2xl font-bold">Editar cliente</h1>
			<p>Edita a un cliente existente</p>
		</div>
		<form action="" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				Nombre del cliente
				<BaseInput v-model="form.name" type="text" name="name" placeholder="Nombre del cliente" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Número de teléfono
				<BaseInput v-model="form.phone" type="text" name="product" placeholder="04241234567" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Cédula de Identidad
				<BaseInput
					v-model="form.identification_number"
					name="amount"
					placeholder="V12345678"
					maxlength="9"
				/>
			</label>
			<BaseButton text="Editar cliente" />
		</form>
	</section>
</template>
