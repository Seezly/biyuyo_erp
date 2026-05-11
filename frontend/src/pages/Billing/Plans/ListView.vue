<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useBillingStore } from '@/stores/billing'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const router = useRouter()
const route = useRoute()
const billingStore = useBillingStore()

const search = ref('')

onMounted(() => {
	search.value = (route.query.search as string) || ''
	fetchPlans()
})

const fetchPlans = () => {
	const params: { search?: string; ordering?: string } = {}
	if (search.value) params.search = search.value
	if (route.query.ordering) params.ordering = route.query.ordering as string

	billingStore.fetchPlans(params)
}

watch(search, () => {
	const query: Record<string, string> = {}
	if (search.value) query.search = search.value
	router.push({ query })
})

const formatPrice = (price: number) => {
	return new Intl.NumberFormat('es-VE', {
		style: 'currency',
		currency: 'USD',
	}).format(price)
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Planes</h1>
			<p>Planes disponibles para tu negocio</p>
		</div>

		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseInput v-model="search" placeholder="Buscar plan..." class="col-span-12 lg:col-span-6" />
		</div>

		<div v-if="billingStore.loading" class="w-full text-center py-8">
			<p>Cargando planes...</p>
		</div>

		<div v-else-if="billingStore.plans.length === 0" class="w-full text-center py-8">
			<p class="text-gray-500">No hay planes disponibles</p>
		</div>

		<div v-else class="grid grid-cols-12 gap-4 w-full">
			<BaseCard v-for="plan in billingStore.plans" :key="plan.id" variant="outlined" class="col-span-full lg:col-span-4">
				<div class="flex flex-col gap-4 justify-start items-start">
					<div class="flex justify-between w-full items-center">
						<div class="flex justify-center items-center size-10 rounded-full bg-secondary">
							<i class="fa-solid fa-layer-group text-lg"></i>
						</div>
					</div>
					<div class="flex flex-col gap-2">
						<h2 class="font-bold text-xl">{{ plan.name }}</h2>
						<p class="text-3xl font-bold text-primary">{{ formatPrice(plan.price) }}/mes</p>
						<div class="flex flex-col gap-1 text-sm text-gray-500">
							<p>Usuarios: {{ plan.max_users }}</p>
							<p>Productos: {{ plan.max_products }}</p>
						</div>
					</div>
				</div>
			</BaseCard>
		</div>
	</section>
</template>