<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

interface Stats {
	totalBusinesses: number
	totalUsers: number
	totalSales: number
	activeSubscriptions: number
}

const stats = ref<Stats>({
	totalBusinesses: 0,
	totalUsers: 0,
	totalSales: 0,
	activeSubscriptions: 0,
})

const loading = ref(true)

const fetchStats = async () => {
  try {
    const response = await fetch('/api/reports/global_stats/')
    if (response.ok) {
      const data = await response.json()
      stats.value.totalBusinesses = data.totalBusinesses
      stats.value.totalUsers = data.totalUsers
      stats.value.totalSales = data.totalSales
      stats.value.activeSubscriptions = data.activeSubscriptions
    }
  } catch (error) {
    console.error('Error fetching stats:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
	fetchStats()
})
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Panel de Administración</h1>
			<p>Estadísticas globales del sistema</p>
		</div>

		<div v-if="loading" class="w-full text-center py-8">
			<p>Cargando estadísticas...</p>
		</div>

		<div v-else class="grid grid-cols-12 gap-8 w-full">
			<BaseCard variant="outlined" class="col-span-12 md:col-span-6 lg:col-span-3">
				<div class="flex flex-col gap-2">
					<div class="size-10 flex justify-center items-center bg-primary rounded-full">
						<i class="fa-solid fa-building text-lg text-white"></i>
					</div>
					<p class="text-sm text-gray-500">Negocios registrados</p>
					<p class="text-2xl font-bold">{{ stats.totalBusinesses }}</p>
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6 lg:col-span-3">
				<div class="flex flex-col gap-2">
					<div class="size-10 flex justify-center items-center bg-secondary rounded-full">
						<i class="fa-solid fa-users text-lg text-white"></i>
					</div>
					<p class="text-sm text-gray-500">Usuarios totales</p>
					<p class="text-2xl font-bold">{{ stats.totalUsers }}</p>
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6 lg:col-span-3">
				<div class="flex flex-col gap-2">
					<div class="size-10 flex justify-center items-center bg-green-500 rounded-full">
						<i class="fa-solid fa-dollar-sign text-lg text-white"></i>
					</div>
					<p class="text-sm text-gray-500">Ventas totales</p>
					<p class="text-2xl font-bold">{{ stats.totalSales }}</p>
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6 lg:col-span-3">
				<div class="flex flex-col gap-2">
					<div class="size-10 flex justify-center items-center bg-yellow-500 rounded-full">
						<i class="fa-solid fa-credit-card text-lg text-white"></i>
					</div>
					<p class="text-sm text-gray-500">Suscripciones activas</p>
					<p class="text-2xl font-bold">{{ stats.activeSubscriptions }}</p>
				</div>
			</BaseCard>

			<div class="col-span-12 flex gap-4">
				<BaseButton to="/admin/statistics" text="Ver estadísticas detalladas" />
				<BaseButton to="/admin/reports" text="Ver reportes" variant="outlined" />
				<BaseButton to="/admin/settings" text="Configuración" variant="secondary" />
			</div>
		</div>
	</section>
</template>