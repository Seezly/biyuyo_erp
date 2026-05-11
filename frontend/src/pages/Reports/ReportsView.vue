<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useReportsStore } from '@/stores/reports'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const reportsStore = useReportsStore()
const loading = ref(true)

onMounted(async () => {
	await Promise.all([
		reportsStore.fetchSales(),
		reportsStore.fetchInventory(),
	])
	loading.value = false
})

const formatCurrency = (value: number) => {
	return new Intl.NumberFormat('es-VE', {
		style: 'currency',
		currency: 'USD',
	}).format(value)
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Resumen financiero</h1>
			<p>La salud de tu negocio en una mirada</p>
		</div>

		<div v-if="loading" class="w-full text-center py-8">
			<p>Cargando reportes...</p>
		</div>

		<div v-else class="grid grid-cols-12 gap-8 w-full">
			<BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="flex justify-between items-center">
						<div class="size-10 flex justify-center items-center bg-primary rounded-full">
							<i class="fa-solid fa-dollar-sign text-lg text-white"></i>
						</div>
						<h2 class="text-2xl font-bold text-primary">Total de ventas</h2>
					</div>
					<div>
						<p class="text-2xl font-bold font-heading">
							{{ reportsStore.sales ? formatCurrency(reportsStore.sales.total_sales) : '$0.00' }}
						</p>
					</div>
					<hr />
					<div>
						<p class="text-sm mb-2">
							{{ reportsStore.sales?.count || 0 }} transacciones
						</p>
						<BaseButton text="Ver más" variant="outlined" to="/reports/sales" />
					</div>
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="flex justify-between items-center">
						<div class="size-10 flex justify-center items-center bg-secondary rounded-full">
							<i class="fa-solid fa-box text-lg text-white"></i>
						</div>
						<h2 class="text-2xl font-bold text-primary">Inventario</h2>
					</div>
					<div>
						<p class="text-2xl font-bold font-heading">
							{{ reportsStore.inventory?.total_products || 0 }} productos
						</p>
						<p class="text-lg text-primary font-medium">
							Valor: {{ reportsStore.inventory ? formatCurrency(reportsStore.inventory.total_value) : '$0.00' }}
						</p>
					</div>
					<hr />
					<div>
						<p class="text-sm mb-2">
							{{ reportsStore.inventory?.low_stock_count || 0 }} bajo stock
						</p>
						<BaseButton text="Ver más" variant="outlined" to="/reports/inventory" />
					</div>
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="flex justify-between items-center">
						<div class="size-10 flex justify-center items-center bg-green-500 rounded-full">
							<i class="fa-solid fa-chart-line text-lg text-white"></i>
						</div>
						<h2 class="text-2xl font-bold text-primary">Ticket promedio</h2>
					</div>
<div>
                        <p class="text-2xl font-bold font-heading">
                            {{ reportsStore.sales ? formatCurrency(reportsStore.sales.average_sale) : '$0.00' }}
                        </p>
                    </div>
                    <hr />
                    <div>
                        <p class="text-sm mb-2">Por venta</p>
                        <BaseButton text="Ver más" variant="outlined" to="/reports/sales" />
                    </div>
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 lg:col-span-8">
				<div class="flex flex-col gap-4">
					<div class="flex flex-col gap-2">
						<h2 class="text-2xl font-bold text-primary">Ventas / Gastos</h2>
						<p>Vista del rendimiento de la última semana</p>
					</div>
					<div>
						<p class="text-2xl font-bold font-heading">
							{{ reportsStore.sales ? formatCurrency(reportsStore.sales.total_sales) : '$0.00' }}
						</p>
					</div>
					<hr />
					<div>
						<p class="text-sm mb-2">Total de ingresos</p>
						<BaseButton text="Ver más" variant="outlined" to="/reports/sales" />
					</div>
				</div>
			</BaseCard>

			<BaseCard variant="secondary" class="col-span-12 lg:col-span-4">
				<div class="flex flex-col gap-4 w-full h-full">
					<div class="flex flex-col gap-2">
						<h2 class="text-2xl font-bold text-white">Alertas</h2>
					</div>
					<div class="flex flex-col justify-start items-start gap-2 w-full">
						<div
							v-if="reportsStore.inventory && reportsStore.inventory.low_stock_count > 0"
							class="flex justify-start items-center gap-2 w-full border border-primary bg-white py-2 px-4 rounded cursor-pointer"
						>
							<i class="fa-solid fa-triangle-exclamation text-lg text-yellow-500"></i>
							<div>
								<p class="font-medium">Stock bajo</p>
								<p class="text-xs">{{ reportsStore.inventory.low_stock_count }} productos</p>
							</div>
						</div>
						<div v-else class="flex items-center gap-2">
							<i class="fa-solid fa-check-circle text-green-500 text-lg"></i>
							<p class="text-white">Inventario OK</p>
						</div>
					</div>
					<div class="mt-auto">
						<BaseButton to="/inventory/products?filter=low" text="Ver productos" variant="outlined" />
					</div>
				</div>
			</BaseCard>
		</div>
	</section>
</template>