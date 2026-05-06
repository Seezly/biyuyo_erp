<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSalesStore } from '@/stores/sales'
import { useToastStore } from '@/stores/toast'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const router = useRouter()
const route = useRoute()
const salesStore = useSalesStore()
const toastStore = useToastStore()

const search = ref('')
const methodFilter = ref('')
const statusFilter = ref('')

onMounted(() => {
	search.value = (route.query.search as string) || ''
	methodFilter.value = (route.query.method as string) || ''
	statusFilter.value = (route.query.status as string) || ''
	fetchPayments()
})

const fetchPayments = () => {
	const params: {
		search?: string
		method?: string
		status?: string
		ordering?: string
		page?: string
	} = {}

	if (search.value) params.search = search.value
	if (methodFilter.value) params.method = methodFilter.value
	if (statusFilter.value) params.status = statusFilter.value
	if (route.query.ordering) params.ordering = route.query.ordering as string
	if (route.query.page) params.page = route.query.page as string

	salesStore.fetchPayments(params)
}

watch([search, methodFilter, statusFilter], () => {
	const query: Record<string, string> = {}
	if (search.value) query.search = search.value
	if (methodFilter.value) query.method = methodFilter.value
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

const getStatusClass = (status: string) => {
	switch (status) {
		case 'completed': return 'bg-green-500'
		case 'pending': return 'bg-yellow-500'
		case 'failed': return 'bg-red-500'
		default: return 'bg-gray-500'
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Lista de pagos</h1>
			<p>Administra los pagos de tu negocio</p>
		</div>

		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseInput v-model="search" placeholder="Buscar por referencia..." class="col-span-12 lg:col-span-4" />
			<div class="flex lg:justify-end justify-between items-center gap-2 col-span-12 lg:col-span-8">
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Todos
					<input type="radio" v-model="methodFilter" value="" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Efectivo
					<input type="radio" v-model="methodFilter" value="cash" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-white relative transition cursor-pointer">
					Transferencia
					<input type="radio" v-model="methodFilter" value="transfer" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
			</div>
		</div>

		<div v-if="salesStore.loading" class="w-full text-center py-8">
			<p>Cargando pagos...</p>
		</div>

		<div v-else-if="salesStore.payments.length === 0" class="w-full text-center py-8">
			<p class="text-gray-500">No hay pagos disponibles</p>
		</div>

		<div v-else class="grid grid-cols-12 gap-4 w-full">
			<BaseCard v-for="payment in salesStore.payments" :key="payment.id" variant="outlined" class="col-span-full lg:col-span-4">
				<div class="flex flex-col gap-4 justify-start items-start">
					<div class="flex justify-between w-full items-center">
						<div class="flex justify-center items-center size-10 rounded-full bg-secondary">
							<i class="fa-solid fa-credit-card text-lg"></i>
						</div>
						<span :class="['rounded-full py-2 px-4 font-bold text-sm uppercase text-white', getStatusClass(payment.status)]">
							{{ payment.status }}
						</span>
					</div>
					<div class="flex flex-col gap-2">
						<h2 class="font-bold text-xl">Pago #{{ payment.id }}</h2>
						<p class="text-sm">Método: {{ payment.method }}</p>
						<p class="text-xl font-bold text-primary">${{ payment.amount }}</p>
						<p class="text-sm text-gray-500">Referencia: {{ payment.reference || 'N/A' }}</p>
						<p class="text-sm text-gray-500">{{ formatDate(payment.created_at) }}</p>
					</div>
				</div>
			</BaseCard>
		</div>
	</section>
</template>