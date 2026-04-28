<script setup lang="ts">
import { ref } from 'vue'
import router from '@/router'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { apiFetch } from '@/utils/helpers'

interface SupplierForm {
	name: string
	rif: string
	email: string
	phone: string
	supply: string
	is_recurrent: boolean
	amount: string | undefined
	date: string | undefined
}
const emit = defineEmits(['submit', 'incrementStep'])

const form = ref<SupplierForm>({
	name: '',
	email: '',
	rif: '',
	phone: '',
	is_recurrent: false,
	amount: '',
	supply: '',
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
			<h1 class="text-primary text-2xl font-bold">Editar proveedor</h1>
			<p>Actualiza los datos del nuevo proveedor</p>
		</div>
		<form action="" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				Nombre del proveedor
				<BaseInput v-model="form.name" type="text" name="name" placeholder="Nombre del proveedor" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Nombre del producto
				<BaseInput v-model="form.supply" type="text" name="supply" placeholder="Nombre del producto" />
			</label>
			<label class="w-full flex flex-col text-dark">
				RIF del proveedor
				<BaseInput v-model="form.rif" type="text" name="rif" placeholder="RIF del proveedor" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Email del proveedor
				<BaseInput v-model="form.email" type="text" name="email" placeholder="Email del proveedor" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Teléfono del proveedor
				<BaseInput v-model="form.phone" type="text" name="phone" placeholder="Teléfono del proveedor" />
			</label>
			<label class="w-full flex gap-4 items-center text-dark">
				<input
					type="checkbox"
					v-model="form.is_recurrent"
					name="is_recurrent"
					id="is_recurrent"
					class="p-2 rounded-xl border border-secondary text-primary"
				/>
				¿Es un pago recurrente?
			</label>
			<Transition name="fade">
				<div v-if="form.is_recurrent" class="w-full max-h-64 flex flex-col gap-4">
					<label class="w-full flex flex-col text-dark">
						Monto del pago recurrente
						<BaseInput v-model="form.amount" type="number" name="amount" placeholder="Monto del pago" />
					</label>
					<label class="w-full flex flex-col text-dark">
						Fecha del pago recurrente
						<BaseInput type="date" v-model="form.date" name="" id="" />
					</label>
				</div>
			</Transition>
			<BaseButton text="Agregar proveedor" />
		</form>
	</section>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
	transition: all 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
	max-height: 0;
	opacity: 0;
	overflow: hidden;
}
</style>
