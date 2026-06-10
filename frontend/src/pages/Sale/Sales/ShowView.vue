<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useSalesStore } from '@/stores/sales'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const salesStore = useSalesStore()

onMounted(async () => {
  await salesStore.fetchSales()
})

const todaySales = computed(() => salesStore.todaySales)
const todayTotal = computed(() => salesStore.todayTotal)

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('es-VE', {
    style: 'currency',
    currency: 'USD',
  }).format(value)
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

const formatTime = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleTimeString('es-VE', {
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Historial de ventas</h1>
			<p>Consulta y gestiona el historial de ventas</p>
		</div>
		<div class="grid lg:grid-cols-4 lg:grid-rows-2 w-full gap-8">
			<BaseCard class="flex-1 hover:shadow-lg transition-shadow lg:col-span-3 lg:row-span-2">
				<div class="flex flex-col md:flex-row justify-between items-start gap-8">
					<div>
						<h2 class="text-white/50 font-semibold text-sm uppercase tracking-widest mb-4">
							Ventas totales de hoy
						</h2>
						<div class="flex flex-col gap-2 mb-4">
							<p class="text-6xl font-heading font-extrabold text-white tracking-tighter">
								{{ formatCurrency(todayTotal) }}
							</p>
							<small class="text-xl text-secondary">
								{{ todaySales.length }} ventas
							</small>
						</div>
					</div>
				</div>
			</BaseCard>
			<BaseCard
				variant="secondary"
				class="flex-1 hover:shadow-lg transition-shadow lg:col-span-1 lg:row-span-2"
			>
				<div
					class="flex flex-col md:flex-row justify-center lg:justify-start lg:items-end gap-8 h-full"
				>
					<div class="flex flex-col gap-2">
						<p class="text-6xl font-heading font-extrabold text-white tracking-tighter">
							{{ salesStore.sales.length }}
						</p>
						<small class="text-xl text-dark">Total ventas</small>
					</div>
				</div>
			</BaseCard>
		</div>
		<div class="flex flex-col gap-4 w-full col-span-1 row-span-4">
			<div class="flex justify-between items-center">
				<h2 class="text-primary text-lg font-semibold">Actividad reciente</h2>
			</div>
			<template v-if="salesStore.sales.length > 0">
				<BaseCard
					v-for="sale in salesStore.sales.slice(0, 5)"
					:key="sale.id"
					variant="outlined"
					class="hover:shadow-lg transition-shadow cursor-pointer"
				>
					<div class="flex flex-row justify-start items-center gap-8 w-full">
						<div class="size-12 bg-primary rounded-full flex items-center justify-center">
							<i class="fa-solid fa-receipt text-white" aria-hidden="true"></i>
						</div>
						<div>
							<div>
								<h3 class="text-lg font-bold">Venta #{{ sale.id }}</h3>
								<p>{{ formatDate(sale.created_at) }}</p>
							</div>
						</div>
						<div class="ml-auto text-right">
							<p class="text-xl font-semibold">{{ formatCurrency(Number(sale.total)) }}</p>
						</div>
					</div>
				</BaseCard>
			</template>
			<BaseCard v-else variant="outlined">
				<p class="text-gray-500 text-center py-4">No hay ventas registradas</p>
			</BaseCard>
		</div>
		<div class="flex justify-between items-center w-full gap-8">
			<BaseButton to="/sales/all" text="Ver todas las ventas" />
			<BaseButton to="/sales/pos" text="Nueva venta" />
		</div>
	</section>
</template>
