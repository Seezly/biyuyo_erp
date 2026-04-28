<script setup lang="ts">
import { ref } from 'vue'
import router from '@/router'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { apiFetch } from '@/utils/helpers'

interface PurchaseForm {
	name: string
	product: string
	amount: string
	quantity: string
	date: string
}
const emit = defineEmits(['submit', 'incrementStep'])

const form = ref<PurchaseForm>({
	name: '',
	product: '',
	amount: '',
	quantity: '',
	date: '',
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
			<h1 class="text-primary text-2xl font-bold">Editar compra o gasto</h1>
			<p>Actualiza la información de tu compra o gasto</p>
		</div>
		<form action="" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				¿Dónde o a quién se le pagó?
				<BaseInput
					v-model="form.name"
					type="text"
					name="name"
					placeholder="Nombre del negocio o persona"
				/>
			</label>
			<label class="w-full flex flex-col text-dark">
				¿Qué se pagó?
				<BaseInput
					v-model="form.product"
					type="text"
					name="product"
					placeholder="Producto, servicio o deuda"
				/>
			</label>
			<label class="w-full flex flex-col text-dark">
				Monto pagado
				<BaseInput v-model="form.amount" type="number" name="amount" placeholder="Monto pagado" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Cantidad o unidades
				<BaseInput
					v-model="form.quantity"
					type="number"
					name="quantity"
					placeholder="Cantidad o unidades"
					min="1"
				/>
			</label>
			<label class="w-full flex flex-col text-dark">
				Fecha del pago
				<BaseInput type="date" v-model="form.date" name="" id="" />
			</label>
			<BaseButton text="Editar pago" />
		</form>
	</section>
</template>
