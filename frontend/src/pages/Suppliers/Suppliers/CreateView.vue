<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useSuppliersStore } from '@/stores/suppliers'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const router = useRouter()
const suppliersStore = useSuppliersStore()

const form = ref({
	name: '',
	rif: '',
	email: '',
	address: '',
	phone: '',
})

const loading = ref(false)
const error = ref('')

const handleSubmit = async () => {
	if (!form.value.name || !form.value.rif) {
		error.value = 'El nombre y RIF son obligatorios'
		return
	}

	loading.value = true
	error.value = ''

	const result = await suppliersStore.createSupplier(form.value)

	loading.value = false

	if (result) {
		router.push('/suppliers')
	} else {
		error.value = suppliersStore.error || 'Error al crear el proveedor'
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Añadir proveedor</h1>
			<p>Completa los datos del nuevo proveedor</p>
		</div>

		<div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
			{{ error }}
		</div>

		<form @submit.prevent="handleSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				Nombre del proveedor *
				<BaseInput v-model="form.name" type="text" name="name" placeholder="Nombre del proveedor" required />
			</label>
			<label class="w-full flex flex-col text-dark">
				RIF *
				<BaseInput v-model="form.rif" type="text" name="rif" placeholder="J-12345678-9" required />
			</label>
			<label class="w-full flex flex-col text-dark">
				Email
				<BaseInput v-model="form.email" type="email" name="email" placeholder="Email del proveedor" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Dirección
				<BaseInput v-model="form.address" type="text" name="address" placeholder="Dirección del proveedor" />
			</label>
			<label class="w-full flex flex-col text-dark">
				Teléfono
				<BaseInput v-model="form.phone" type="text" name="phone" placeholder="Teléfono del proveedor" />
			</label>
			<BaseButton :text="loading ? 'Creando...' : 'Agregar proveedor'" :disabled="loading" />
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
