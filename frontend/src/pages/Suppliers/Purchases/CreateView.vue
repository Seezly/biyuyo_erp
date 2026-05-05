<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSuppliersStore } from '@/stores/suppliers'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const router = useRouter()
const suppliersStore = useSuppliersStore()

const form = ref({
	supplier: 0,
	total: 0,
})

const loading = ref(false)
const error = ref('')

onMounted(async () => {
	await suppliersStore.fetchSuppliers()
})

const handleSubmit = async () => {
	if (!form.value.supplier) {
		error.value = 'Selecciona un proveedor'
		return
	}

	loading.value = true
	error.value = ''

	const result = await suppliersStore.createPurchase({
		supplier: form.value.supplier,
		total: form.value.total,
		items: [],
	})

	loading.value = false

	if (result) {
		router.push('/suppliers/purchases')
	} else {
		error.value = suppliersStore.error || 'Error al crear la compra'
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Agregar compra</h1>
			<p>Registra una nueva compra a proveedor</p>
		</div>

		<div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
			{{ error }}
		</div>

		<form @submit.prevent="handleSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
			<label class="w-full flex flex-col text-dark">
				Proveedor *
				<select v-model="form.supplier" class="py-2 px-4 rounded-xl border border-secondary text-primary" required>
					<option :value="0">Seleccionar proveedor</option>
					<option v-for="supplier in suppliersStore.suppliers" :key="supplier.id" :value="supplier.id">
						{{ supplier.name }}
					</option>
				</select>
			</label>
			<label class="w-full flex flex-col text-dark">
				Total
				<BaseInput v-model="form.total" type="number" step="0.01" name="total" placeholder="Monto total" />
			</label>
			<BaseButton :text="loading ? 'Creando...' : 'Crear compra'" :disabled="loading" />
		</form>
	</section>
</template>
