<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCustomersStore } from '@/stores/customers'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const router = useRouter()
const customersStore = useCustomersStore()

const form = ref({
	name: '',
	phone: '',
	identification_number: '',
})

const loading = ref(false)
const error = ref('')

const handleSubmit = async () => {
	if (!form.value.name) {
		error.value = 'El nombre es obligatorio'
		return
	}

	loading.value = true
	error.value = ''

	const result = await customersStore.createCustomer(form.value)

	loading.value = false

	if (result) {
		router.push('/customers')
	} else {
		error.value = customersStore.error || 'Error al crear el cliente'
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Agregar cliente</h1>
			<p>Añade un nuevo cliente al registro de tu negocio</p>
		</div>

		<div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
			{{ error }}
		</div>

		<form @submit.prevent="handleSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				Nombre del cliente *
				<BaseInput v-model="form.name" type="text" name="name" placeholder="Nombre del cliente" required />
			</label>
			<label class="w-full flex flex-col text-dark">
				Número de teléfono
				<BaseInput v-model="form.phone" type="text" name="phone" placeholder="04241234567" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Cédula de Identidad
				<BaseInput
					v-model="form.identification_number"
					name="identification_number"
					placeholder="V12345678"
					maxlength="9"
				/>
			</label>
			<BaseButton :text="loading ? 'Creando...' : 'Agregar cliente'" :disabled="loading" />
		</form>
	</section>
</template>
