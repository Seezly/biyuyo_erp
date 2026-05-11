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
	fetchSubscriptions()
})

const fetchSubscriptions = () => {
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

	billingStore.fetchSubscriptions(params)
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
		case 'active': return 'bg-green-500'
		case 'expired': return 'bg-red-500'
		case 'pending': return 'bg-yellow-500'
		default: return 'bg-gray-500'
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Suscripciones</h1>
			<p>Administra las suscripciones de tu negocio</p>
		</div>

		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseInput v-model="search" placeholder="Buscar suscripción..." class="col-span-12 lg:col-span-6" />
			<div class="flex lg:justify-end justify-between items-center gap-2 col-span-12 lg:col-span-6">
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Todas
					<input type="radio" v-model="statusFilter" value="" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Activas
					<input type="radio" v-model="statusFilter" value="active" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-white relative transition cursor-pointer">
					Expiradas
					<input type="radio" v-model="statusFilter" value="expired" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
			</div>
		</div>

		<div v-if="billingStore.loading" class="w-full text-center py-8">
			<p>Cargando suscripciones...</p>
		</div>

		<div v-else-if="billingStore.subscriptions.length === 0" class="w-full text-center py-8">
			<p class="text-gray-500">No hay suscripciones disponibles</p>
		</div>

		<div v-else class="grid grid-cols-12 gap-4 w-full">
			<BaseCard v-for="subscription in billingStore.subscriptions" :key="subscription.id" variant="outlined" class="col-span-full lg:col-span-4">
				<div class="flex flex-col gap-4 justify-start items-start">
					<div class="flex justify-between w-full items-center">
						<div class="flex justify-center items-center size-10 rounded-full bg-secondary">
							<i class="fa-solid fa-credit-card text-lg"></i>
						</div>
						<span :class="['rounded-full py-2 px-4 font-bold text-sm uppercase text-white', getStatusClass(subscription.status)]">
							{{ subscription.status }}
						</span>
					</div>
					<div class="flex flex-col gap-2">
						<h2 class="font-bold text-xl">Suscripción #{{ subscription.id }}</h2>
						<p class="text-sm">Plan: {{ subscription.plan_name || `Plan #${subscription.plan}` }}</p>
						<p class="text-sm text-gray-500">Desde: {{ formatDate(subscription.start_date) }}</p>
						<p class="text-sm text-gray-500">Hasta: {{ formatDate(subscription.end_date || '') }}</p>
					</div>
				</div>
			</BaseCard>
		</div>
	</section>
</template>