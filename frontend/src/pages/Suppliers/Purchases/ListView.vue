<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSuppliersStore } from '@/stores/suppliers'
import { useToastStore } from '@/stores/toast'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'

const router = useRouter()
const route = useRoute()
const suppliersStore = useSuppliersStore()
const toastStore = useToastStore()

const search = ref('')
const statusFilter = ref('')

onMounted(() => {
	search.value = (route.query.search as string) || ''
	statusFilter.value = (route.query.status as string) || ''
	fetchPurchases()
})

const fetchPurchases = () => {
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

	suppliersStore.fetchPurchases(params)
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
		hour: '2-digit',
		minute: '2-digit',
	})
}

const getStatusClass = (status: string) => {
	switch (status) {
		case 'completed': return 'bg-green-500'
		case 'pending': return 'bg-yellow-500'
		case 'cancelled': return 'bg-red-500'
		default: return 'bg-gray-500'
	}
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Compras</h1>
			<p>Administra las compras de tu negocio</p>
		</div>

		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseButton to="/suppliers/purchases/add" text="Nueva compra" class="col-span-12 lg:col-span-3" />
			<BaseInput v-model="search" placeholder="Buscar compra..." class="col-span-12 lg:col-span-5" />
			<div class="flex lg:justify-end justify-between items-center gap-2 col-span-12 lg:col-span-4">
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Todos
					<input type="radio" v-model="statusFilter" value="" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Completadas
					<input type="radio" v-model="statusFilter" value="completed" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-white relative transition cursor-pointer">
					Pendientes
					<input type="radio" v-model="statusFilter" value="pending" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
			</div>
		</div>

		<div v-if="suppliersStore.loading" class="w-full text-center py-8">
			<p>Cargando compras...</p>
		</div>

		<div v-else-if="suppliersStore.purchases.length === 0" class="w-full text-center py-8">
			<p class="text-gray-500">No hay compras disponibles</p>
		</div>

		<div v-else class="grid grid-cols-12 gap-4 w-full">
			<BaseCard v-for="purchase in suppliersStore.purchases" :key="purchase.id" variant="outlined" class="col-span-full lg:col-span-4">
				<div class="flex flex-col gap-4 justify-start items-start">
					<div class="flex justify-between w-full items-center">
						<div class="flex justify-center items-center size-10 rounded-full bg-secondary">
							<i class="fa-solid fa-shopping-cart text-lg"></i>
						</div>
						<span :class="['rounded-full py-2 px-4 font-bold text-sm uppercase text-white', getStatusClass(purchase.status)]">
							{{ purchase.status }}
						</span>
					</div>
					<div class="flex flex-col gap-2">
						<h2 class="font-bold text-xl">Compra #{{ purchase.id }}</h2>
						<p class="text-xl font-bold text-primary">${{ purchase.total }}</p>
						<p class="text-sm text-gray-500">{{ formatDate(purchase.created_at) }}</p>
					</div>
					<div class="flex gap-2 w-full">
						<BaseButton :to="'/suppliers/purchases/edit/' + purchase.id" text="Editar" variant="secondary" />
					</div>
				</div>
			</BaseCard>
		</div>
	</section>
</template>