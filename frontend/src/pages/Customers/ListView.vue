<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCustomersStore } from '@/stores/customers'
import { useAuthStore } from '@/stores/auth'
import { useBusinessesStore } from '@/stores/businesses'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseAlert from '@/components/ui/BaseAlert.vue'

const router = useRouter()
const route = useRoute()
const customersStore = useCustomersStore()
const authStore = useAuthStore()
const businessesStore = useBusinessesStore()

const isSuperadmin = computed(() => authStore.user?.is_superuser === true)
const selectedBusinessId = ref<number | null>(null)

const search = ref('')
const showDeleteAlert = ref(false)
const customerToDelete = ref<number | null>(null)

onMounted(async () => {
	if (isSuperadmin.value) {
		await businessesStore.fetchBusinesses()
	}
	search.value = (route.query.search as string) || ''
	fetchCustomers()
})

const fetchCustomers = () => {
	const params: {
		search?: string
		ordering?: string
		page?: string
		business_id?: number | null
	} = {}

	if (search.value) params.search = search.value
	if (isSuperadmin.value && selectedBusinessId.value) {
		params.business_id = selectedBusinessId.value
	}
	if (route.query.ordering) params.ordering = route.query.ordering as string
	if (route.query.page) params.page = route.query.page as string

	customersStore.fetchCustomers(params)
}

watch([search, selectedBusinessId], () => {
	const query: Record<string, string> = {}
	if (search.value) query.search = search.value
	router.push({ query })
})

const confirmDelete = (id: number) => {
	customerToDelete.value = id
	showDeleteAlert.value = true
}

const handleDelete = async () => {
	if (customerToDelete.value) {
		await customersStore.deleteCustomer(customerToDelete.value)
		showDeleteAlert.value = false
		customerToDelete.value = null
	}
}

const cancelDelete = () => {
	showDeleteAlert.value = false
	customerToDelete.value = null
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
			<h1 class="text-primary text-2xl font-bold">Clientes</h1>
			<p>Administra a todos tus clientes desde un solo lugar</p>
		</div>

		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseButton to="/customers/add" text="Añadir cliente" class="col-span-12 lg:col-span-3" />
			<BaseInput v-model="search" placeholder="Buscar cliente por nombre, teléfono o identificación" class="col-span-12 lg:col-span-6" />
			<label v-if="isSuperadmin" class="w-full flex flex-col text-dark col-span-12 lg:col-span-3">
				<select v-model="selectedBusinessId" class="py-2 px-4 rounded-xl border border-secondary text-primary">
					<option :value="null">Todos los negocios</option>
					<option v-for="b in businessesStore.businesses" :key="b.id" :value="b.id">
						{{ b.name }}
					</option>
				</select>
			</label>
		</div>

		<div v-if="customersStore.loading" class="w-full text-center py-8">
			<p>Cargando clientes...</p>
		</div>

		<div v-else-if="customersStore.customers.length === 0" class="w-full text-center py-8">
			<p class="text-gray-500">No hay clientes disponibles</p>
		</div>

		<div v-else class="w-full">
			<BaseCard variant="outlined" class="col-span-12 overflow-x-auto">
				<table class="min-w-full divide-y-2 divide-gray-200">
					<thead class="ltr:text-left rtl:text-right">
						<tr class="*:font-medium *:text-gray-900">
							<th class="px-4 py-2 whitespace-nowrap">Nombre</th>
							<th class="px-4 py-2 whitespace-nowrap">Teléfono</th>
							<th class="px-4 py-2 whitespace-nowrap">Identificación</th>
							<th class="px-4 py-2 whitespace-nowrap">Desde</th>
							<th class="px-4 py-2 whitespace-nowrap text-right">Acciones</th>
						</tr>
					</thead>

					<tbody class="divide-y divide-gray-200 *:even:bg-gray-50">
						<tr v-for="customer in customersStore.customers" :key="customer.id" class="*:text-gray-900 *:first:font-medium">
							<td class="px-4 py-2 whitespace-nowrap">{{ customer.name }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ customer.phone }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ customer.identification_number }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ formatDate(customer.created_at) }}</td>
							<td class="px-4 py-2 whitespace-nowrap flex justify-end items-center gap-2">
								<BaseButton :to="'/customers/edit/' + customer.id" text="Editar" variant="secondary" width="auto" />
								<BaseButton text="Eliminar" width="auto" @click="confirmDelete(customer.id)" />
							</td>
						</tr>
					</tbody>
				</table>
			</BaseCard>
		</div>

		<BaseAlert
			:visible="showDeleteAlert"
			title="Eliminar cliente"
			subtitle="Esta acción no se puede deshacer"
			description="¿Estás seguro de que deseas eliminar este cliente?"
			variant="delete"
			:cta="'Eliminar'"
			:cancel="true"
			@update="showDeleteAlert = false"
			@close="cancelDelete"
			@next="handleDelete"
		/>
	</section>
</template>