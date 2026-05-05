<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSuppliersStore } from '@/stores/suppliers'
import { apiFetch } from '@/utils/helpers'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const router = useRouter()
const route = useRoute()
const suppliersStore = useSuppliersStore()

const purchaseId = Number(route.params.id)

const form = ref({
	supplier: 0,
	total: 0,
})

const loading = ref(true)
const saving = ref(false)
const error = ref('')

onMounted(async () => {
	await suppliersStore.fetchSuppliers()

	try {
		const response = await apiFetch(`/api/purchases/${purchaseId}/`)
		if (response.ok) {
			const purchase = await response.json()
			form.value = {
				supplier: purchase.supplier,
				total: purchase.total,
			}
		} else {
			error.value = 'Compra no encontrada'
		}
	} catch (e: any) {
		error.value = 'Error al cargar la compra'
	} finally {
		loading.value = false
	}
})

const handleSubmit = async () => {
	saving.value = true
	error.value = ''

	try {
		const response = await apiFetch(`/api/purchases/${purchaseId}/`, {
			method: 'PATCH',
			body: JSON.stringify(form.value),
		})

		if (response.ok) {
			router.push('/suppliers/purchases')
		} else {
			const errorData = await response.json()
			error.value = JSON.stringify(errorData)
		}
	} catch (e: any) {
		error.value = e.message
	} finally {
		saving.value = false
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Editar compra</h1>
			<p>Actualiza la información de la compra</p>
		</div>

		<div v-if="loading" class="w-full text-center py-8">
			<p>Cargando compra...</p>
		</div>

		<div v-else-if="error && !form.supplier" class="w-full text-center py-8">
			<p class="text-red-500">{{ error }}</p>
		</div>

		<div v-else>
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
				<BaseButton :text="saving ? 'Guardando...' : 'Guardar compra'" :disabled="saving" />
			</form>
		</div>
	</section>
</template>
