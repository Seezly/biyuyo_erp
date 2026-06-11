<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSalesStore } from '@/stores/sales'
import { useCustomersStore } from '@/stores/customers'
import { useAuthStore } from '@/stores/auth'
import { useBusinessesStore } from '@/stores/businesses'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseAlert from '@/components/ui/BaseAlert.vue'

const router = useRouter()
const route = useRoute()
const salesStore = useSalesStore()
const customersStore = useCustomersStore()
const authStore = useAuthStore()
const businessesStore = useBusinessesStore()

const isSuperadmin = computed(() => authStore.user?.is_superuser === true)
const selectedBusinessId = ref<number | null>(null)

const search = ref('')
const statusFilter = ref('')
const showDeleteAlert = ref(false)
const saleToDelete = ref<number | null>(null)

// Initialize filters from URL query params
onMounted(async () => {
	if (isSuperadmin.value) {
		await businessesStore.fetchBusinesses()
	}
	search.value = (route.query.search as string) || ''
	statusFilter.value = (route.query.status as string) || ''
	await Promise.all([
		fetchSales(),
		customersStore.fetchCustomers()
	])
})

// Fetch sales with current filter params
const fetchSales = () => {
	const params: {
		search?: string
		status?: string
		ordering?: string
		page?: string
		business_id?: number | null
	} = {}

	if (search.value) params.search = search.value
	if (statusFilter.value) params.status = statusFilter.value
	if (isSuperadmin.value && selectedBusinessId.value) {
		params.business_id = selectedBusinessId.value
	}
	if (route.query.ordering) params.ordering = route.query.ordering as string
	if (route.query.page) params.page = route.query.page as string

	salesStore.fetchSales(params)
}

// Watch for filter changes and update URL
watch([search, statusFilter, selectedBusinessId], () => {
	const query: Record<string, string> = {}
	if (search.value) query.search = search.value
	if (statusFilter.value) query.status = statusFilter.value

	router.push({ query })
}, { deep: true })

const formatDate = (dateString: string) => {
	const date = new Date(dateString)
	return date.toLocaleDateString('es-VE', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
	})
}

const getCustomerName = (customerId: number) => {
	const customer = customersStore.customers.find(c => c.id === customerId)
	return customer?.name || `Cliente #${customerId}`
}

const totalSales = computed(() => {
	return salesStore.sales.reduce((sum, s) => sum + Number(s.total), 0)
})

const todaySales = computed(() => {
	const today = new Date().toISOString().split('T')[0] as string
	return salesStore.sales
		.filter(s => {
			const createdAt = s.created_at as string | undefined
			return createdAt ? createdAt.startsWith(today) : false
		})
		.reduce((sum, s) => sum + Number(s.total), 0)
})

const confirmDelete = (id: number) => {
	saleToDelete.value = id
	showDeleteAlert.value = true
}

const handleDelete = async () => {
	if (saleToDelete.value) {
		await salesStore.deleteSale(saleToDelete.value)
		showDeleteAlert.value = false
		saleToDelete.value = null
	}
}

const cancelDelete = () => {
	showDeleteAlert.value = false
	saleToDelete.value = null
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Total de ventas</h1>
			<p>Consulta y gestiona las ventas de tu negocio</p>
		</div>

		<div class="grid grid-cols-1 md:grid-cols-3 gap-4 w-full">
			<BaseCard variant="outlined">
				<div class="flex flex-col gap-2">
					<p class="text-sm text-gray-500">Ventas totales</p>
					<p class="text-2xl font-bold text-primary">${{ totalSales.toFixed(2) }}</p>
				</div>
			</BaseCard>
			<BaseCard variant="outlined">
				<div class="flex flex-col gap-2">
					<p class="text-sm text-gray-500">Ventas de hoy</p>
					<p class="text-2xl font-bold text-primary">${{ todaySales.toFixed(2) }}</p>
				</div>
			</BaseCard>
			<BaseCard variant="outlined">
				<div class="flex flex-col gap-2">
					<p class="text-sm text-gray-500">Total de transacciones</p>
					<p class="text-2xl font-bold text-primary">{{ salesStore.sales.length }}</p>
				</div>
			</BaseCard>
		</div>

		<div class="w-full grid grid-cols-12 lg:grid-rows-6 gap-8">
			<div class="col-span-12 lg:col-span-3 lg:row-span-1">
				<BaseButton text="Nueva venta" to="/sales/pos" />
			</div>
			<div class="col-span-12 lg:col-span-4 lg:row-span-1">
				<BaseInput v-model="search" type="search" placeholder="Buscar por cliente o ID" class="w-full" />
			</div>
			<div class="col-span-12 lg:col-span-3 lg:row-span-1">
				<BaseInput v-model="statusFilter" type="search" placeholder="Filtrar por status" class="w-full" />
			</div>
			<label v-if="isSuperadmin" class="w-full flex flex-col text-dark col-span-12 lg:col-span-2 lg:row-span-1">
				<select v-model="selectedBusinessId" class="py-2 px-4 rounded-xl border border-secondary text-primary">
					<option :value="null">Todos los negocios</option>
					<option v-for="b in businessesStore.businesses" :key="b.id" :value="b.id">
						{{ b.name }}
					</option>
				</select>
			</label>

			<div class="col-span-12 lg:col-span-12 lg:row-span-5">
				<BaseCard variant="outlined">
					<h2 class="text-primary font-semibold text-xl mb-8">Últimas ventas</h2>

					<div v-if="salesStore.loading" class="text-center py-8">
						<p>Cargando ventas...</p>
					</div>

					<div v-else-if="salesStore.sales.length === 0" class="text-center py-8">
						<p class="text-gray-500">No hay ventas disponibles</p>
					</div>

					<div v-else class="flex flex-col gap-4 w-full">
						<div
							v-for="sale in salesStore.sales"
							:key="sale.id"
							class="flex flex-col lg:flex-row lg:items-center w-full border-b border-secondary/10 pb-4 gap-4"
						>
							<div class="size-12 rounded-full bg-primary lg:flex justify-center items-center">
								<i class="fa-solid fa-receipt text-xl text-white"></i>
							</div>
							<div class="flex-1">
								<div class="flex gap-4 justify-between items-center">
									<div>
										<h3 class="text-primary text-lg font-medium">
											{{ getCustomerName(sale.customer_id) }}
										</h3>
										<p class="text-xs text-gray-500">Venta #{{ sale.id }}</p>
									</div>
									<p class="text-xs text-gray-500">{{ formatDate(sale.created_at) }}</p>
								</div>
							</div>
							<div class="flex flex-col items-end">
								<p class="text-primary text-2xl font-bold">${{ Number(sale.total).toFixed(2) }}</p>
								<span
									:class="sale.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
									class="text-xs px-2 py-1 rounded"
								>
									{{ sale.status }}
								</span>
							</div>
							<div class="flex gap-2 justify-center items-center lg:ml-auto">
								<BaseButton
									:text="'Ver'"
									variant="outlined"
									class="w-full lg:w-auto"
									:to="'/sales/' + sale.id"
								/>
								<BaseButton
									text="Eliminar"
									class="w-full lg:w-auto"
									@click="confirmDelete(sale.id)"
								/>
							</div>
						</div>
					</div>
				</BaseCard>
			</div>
		</div>

		<BaseAlert
			:visible="showDeleteAlert"
			title="Confirmar eliminación"
			subtitle="Esta acción no se puede deshacer"
			description="¿Estás seguro de que deseas eliminar esta venta? Se eliminará permanentemente del registro."
			variant="delete"
			:cta="'Eliminar'"
			:cancel="true"
			@update="showDeleteAlert = false"
			@close="cancelDelete"
			@next="handleDelete"
		/>
	</section>
</template>