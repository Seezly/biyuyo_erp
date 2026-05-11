<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useBusinessesStore } from '@/stores/businesses'
import { useAuthStore } from '@/stores/auth'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
const route = useRoute()
const businessesStore = useBusinessesStore()
const authStore = useAuthStore()

const search = ref('')
const statusFilter = ref('')

onMounted(() => {
	search.value = (route.query.search as string) || ''
	statusFilter.value = (route.query.is_active as string) || ''
	fetchBusinesses()
})

const fetchBusinesses = () => {
	const params: {
		search?: string
		is_active?: string
		ordering?: string
		page?: string
	} = {}

	if (search.value) params.search = search.value
	if (statusFilter.value) params.is_active = statusFilter.value
	if (route.query.ordering) params.ordering = route.query.ordering as string
	if (route.query.page) params.page = route.query.page as string

	businessesStore.fetchBusinesses(params)
}

watch([search, statusFilter], () => {
	const query: Record<string, string> = {}
	if (search.value) query.search = search.value
	if (statusFilter.value) query.is_active = statusFilter.value
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

const getStatusClass = (isActive: boolean) => {
	return isActive ? 'bg-green-500' : 'bg-red-500'
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Negocios</h1>
			<p>Lista de negocios registrados en el sistema</p>
		</div>

		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseInput v-model="search" placeholder="Buscar negocio..." class="col-span-12 lg:col-span-6" />
			<div class="flex lg:justify-end justify-between items-center gap-2 col-span-12 lg:col-span-6">
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Todos
					<input type="radio" v-model="statusFilter" value="" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition cursor-pointer">
					Activos
					<input type="radio" v-model="statusFilter" value="true" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
				<label class="px-4 py-2 bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-white relative transition cursor-pointer">
					Inactivos
					<input type="radio" v-model="statusFilter" value="false" class="absolute opacity-0 cursor-pointer h-full w-full" />
				</label>
			</div>
		</div>

		<div v-if="businessesStore.loading" class="w-full text-center py-8">
			<p>Cargando negocios...</p>
		</div>

		<div v-else-if="businessesStore.businesses.length === 0" class="w-full text-center py-8">
			<p class="text-gray-500">No hay negocios disponibles</p>
		</div>

		<div v-else class="w-full">
			<BaseCard variant="outlined" class="overflow-x-auto">
				<table class="min-w-full divide-y-2 divide-gray-200">
					<thead class="ltr:text-left rtl:text-right">
						<tr class="*:font-medium *:text-gray-900">
							<th class="px-4 py-2 whitespace-nowrap">Nombre</th>
							<th class="px-4 py-2 whitespace-nowrap">RIF</th>
							<th class="px-4 py-2 whitespace-nowrap">Email</th>
							<th class="px-4 py-2 whitespace-nowrap">Teléfono</th>
							<th class="px-4 py-2 whitespace-nowrap">Estado</th>
							<th class="px-4 py-2 whitespace-nowrap">Estado</th>
							<th class="px-4 py-2 whitespace-nowrap">Fecha de inicio</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200 *:even:bg-gray-50">
						<tr v-for="business in businessesStore.businesses" :key="business.id" class="*:text-gray-900">
							<td class="px-4 py-2 whitespace-nowrap font-bold">{{ business.name }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ business.rif }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ business.email }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ business.phone }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ business.state }}</td>
							<td class="px-4 py-2 whitespace-nowrap">
								<span :class="['rounded-full py-2 px-4 font-bold text-sm uppercase text-white', getStatusClass(business.is_active)]">
									{{ business.is_active ? 'Activo' : 'Inactivo' }}
								</span>
							</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ formatDate(business.start_date) }}</td>
						</tr>
					</tbody>
				</table>
			</BaseCard>
		</div>
	</section>
</template>