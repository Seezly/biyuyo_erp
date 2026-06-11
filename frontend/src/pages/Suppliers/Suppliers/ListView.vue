<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSuppliersStore } from '@/stores/suppliers'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseAlert from '@/components/ui/BaseAlert.vue'

const router = useRouter()
const route = useRoute()
const suppliersStore = useSuppliersStore()
const authStore = useAuthStore()

const search = ref('')
const showDeleteAlert = ref(false)
const supplierToDelete = ref<number | null>(null)

onMounted(async () => {
	search.value = (route.query.search as string) || ''
	fetchSuppliers()
})

const fetchSuppliers = () => {
	const params: {
		search?: string
		ordering?: string
		page?: string
	} = {}

	if (search.value) params.search = search.value
	if (route.query.ordering) params.ordering = route.query.ordering as string
	if (route.query.page) params.page = route.query.page as string

	suppliersStore.fetchSuppliers(params)
}

watch([search], () => {
	const query: Record<string, string> = {}
	if (search.value) query.search = search.value
	router.push({ query })
})

const confirmDelete = (id: number) => {
	supplierToDelete.value = id
	showDeleteAlert.value = true
}

const handleDelete = async () => {
	if (supplierToDelete.value) {
		await suppliersStore.deleteSupplier(supplierToDelete.value)
		showDeleteAlert.value = false
		supplierToDelete.value = null
	}
}

const cancelDelete = () => {
	showDeleteAlert.value = false
	supplierToDelete.value = null
}

const formatDate = (dateString: string) => {
	if (!dateString) return '-'
	const date = new Date(dateString)
	return date.toLocaleDateString('es-VE', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric',
	})
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Proveedores</h1>
			<p>Administra a todos tus proveedores</p>
		</div>

		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseButton to="/suppliers/add" text="Añadir proveedor" class="col-span-12 lg:col-span-3" />
			<BaseInput v-model="search" placeholder="Buscar por nombre, RIF o teléfono" class="col-span-12 lg:col-span-9" />
		</div>

		<div v-if="suppliersStore.loading" class="w-full text-center py-8">
			<p>Cargando proveedores...</p>
		</div>

		<div v-else-if="suppliersStore.suppliers.length === 0" class="w-full text-center py-8">
			<p class="text-gray-500">No hay proveedores disponibles</p>
		</div>

		<div v-else class="w-full">
			<BaseCard variant="outlined" class="col-span-12 overflow-x-auto">
				<table class="min-w-full divide-y-2 divide-gray-200">
					<thead class="ltr:text-left rtl:text-right">
						<tr class="*:font-medium *:text-gray-900">
							<th class="px-4 py-2 whitespace-nowrap">Nombre</th>
							<th class="px-4 py-2 whitespace-nowrap">RIF</th>
							<th class="px-4 py-2 whitespace-nowrap">Teléfono</th>
							<th class="px-4 py-2 whitespace-nowrap">Email</th>
							<th class="px-4 py-2 whitespace-nowrap">Desde</th>
							<th class="px-4 py-2 whitespace-nowrap text-right">Acciones</th>
						</tr>
					</thead>

					<tbody class="divide-y divide-gray-200 *:even:bg-gray-50">
						<tr v-for="supplier in suppliersStore.suppliers" :key="supplier.id" class="*:text-gray-900 *:first:font-medium">
							<td class="px-4 py-2 whitespace-nowrap">{{ supplier.name }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ supplier.rif }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ supplier.phone }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ supplier.email || '-' }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ formatDate(supplier.created_at) }}</td>
							<td class="px-4 py-2 whitespace-nowrap flex justify-end items-center gap-2">
								<BaseButton :to="'/suppliers/edit/' + supplier.id" text="Editar" variant="secondary" width="auto" />
								<BaseButton text="Eliminar" width="auto" @click="confirmDelete(supplier.id)" />
							</td>
						</tr>
					</tbody>
				</table>
			</BaseCard>
		</div>

		<BaseAlert
			:visible="showDeleteAlert"
			title="Eliminar proveedor"
			subtitle="Esta acción no se puede deshacer"
			description="¿Estás seguro de que deseas eliminar este proveedor?"
			variant="delete"
			:cta="'Eliminar'"
			:cancel="true"
			@update="showDeleteAlert = false"
			@close="cancelDelete"
			@next="handleDelete"
		/>
	</section>
</template>