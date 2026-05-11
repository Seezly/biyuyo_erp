<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useBillingStore } from '@/stores/billing'
import { useToastStore } from '@/stores/toast'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const router = useRouter()
const route = useRoute()
const billingStore = useBillingStore()
const toastStore = useToastStore()

const search = ref('')
const statusFilter = ref('')

onMounted(() => {
	search.value = (route.query.search as string) || ''
	statusFilter.value = (route.query.status as string) || ''
	fetchInvoices()
})

const fetchInvoices = () => {
	const params: {
		search?: string
		status?: string
		ordering?: string
		page?: string
	} = {}

	if (search.value) params.search = search.value
	if (statusFilter.value) params.status = statusFilter.value
	if (route.query.ordering) params.ordering = route.query.ordering as string
	if (route.query.page) params.page = route.query.page as string

	billingStore.fetchInvoices(params)
}

watch([search, statusFilter], () => {
	const query: Record<string, string> = {}
	if (search.value) query.search = search.value
	if (statusFilter.value) query.status = statusFilter.value
	router.push({ query })
}, { deep: true })

const formatDate = (dateString: string) => {
	if (!dateString) return '-'
	const date = new Date(dateString)
	return date.toLocaleDateString('es-VE', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric',
	})
}

const getStatusClass = (status: string) => {
	switch (status) {
		case 'paid': return 'bg-green-500'
		case 'pending': return 'bg-yellow-500'
		case 'overdue': return 'bg-red-500'
		default: return 'bg-gray-500'
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Facturas</h1>
			<p>Historial de facturas y pagos</p>
		</div>

		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseInput v-model="search" placeholder="Buscar factura..." class="col-span-12 lg:col-span-6" />
			<div class="flex lg:justify-end justify-between items-center gap-2 col-span-12 lg:col-span-6">
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Todas
					<input type="radio" v-model="statusFilter" value="" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Pagadas
					<input type="radio" v-model="statusFilter" value="paid" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-white relative transition cursor-pointer">
					Pendientes
					<input type="radio" v-model="statusFilter" value="pending" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
			</div>
		</div>

		<div v-if="billingStore.loading" class="w-full text-center py-8">
			<p>Cargando facturas...</p>
		</div>

		<div v-else-if="billingStore.invoices.length === 0" class="w-full text-center py-8">
			<p class="text-gray-500">No hay facturas disponibles</p>
		</div>

		<div v-else class="w-full">
			<BaseCard variant="outlined" class="overflow-x-auto">
				<table class="min-w-full divide-y-2 divide-gray-200">
					<thead class="ltr:text-left rtl:text-right">
						<tr class="*:font-medium *:text-gray-900">
							<th class="px-4 py-2 whitespace-nowrap">ID</th>
							<th class="px-4 py-2 whitespace-nowrap">Monto</th>
							<th class="px-4 py-2 whitespace-nowrap">Método</th>
							<th class="px-4 py-2 whitespace-nowrap">Estado</th>
							<th class="px-4 py-2 whitespace-nowrap">Fecha</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200 *:even:bg-gray-50">
						<tr v-for="invoice in billingStore.invoices" :key="invoice.id" class="*:text-gray-900">
							<td class="px-4 py-2 whitespace-nowrap">#{{ invoice.id }}</td>
							<td class="px-4 py-2 whitespace-nowrap font-bold">${{ invoice.amount }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ invoice.method }}</td>
							<td class="px-4 py-2 whitespace-nowrap">
								<span :class="['rounded-full py-2 px-4 font-bold text-sm uppercase text-white', getStatusClass(invoice.status)]">
									{{ invoice.status }}
								</span>
							</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ formatDate(invoice.created_at) }}</td>
						</tr>
					</tbody>
				</table>
			</BaseCard>
		</div>
	</section>
</template>