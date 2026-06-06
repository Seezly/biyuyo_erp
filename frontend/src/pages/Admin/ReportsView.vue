<script setup lang="ts">
import { useReportsStore } from '@/stores/reports'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const reportsStore = useReportsStore()

const downloadCSV = async (type: 'businesses' | 'revenue' | 'users') => {
  let data: any[] = []
  let filename = ''

  if (type === 'businesses') {
    await reportsStore.fetchSummary()
    data = reportsStore.summary.map((s: any) => ({
      Negocio: s.business_name,
      Ventas: s.total_sales,
      Compras: s.total_purchases,
      Productos: s.total_products,
      'Stock Bajo': s.low_stock_count,
    }))
    filename = 'reporte_negocios.csv'
  } else if (type === 'revenue') {
    await reportsStore.fetchSales()
    data = [
      {
        'Ventas Totales': reportsStore.sales?.total_sales ?? 0,
        'Cantidad': reportsStore.sales?.count ?? 0,
        'Venta Promedio': reportsStore.sales?.average_sale ?? 0,
      }
    ]
    filename = 'reporte_ingresos.csv'
  } else if (type === 'users') {
    await reportsStore.fetchSummary()
    data = reportsStore.summary.map((s: any) => ({
      Negocio: s.business_name,
      Productos: s.total_products,
    }))
    filename = 'reporte_usuarios.csv'
  }

  if (data.length === 0) return

  const headers = Object.keys(data[0])
  const csvContent = [
    headers.join(','),
    ...data.map(row => headers.map(h => `"${(row as any)[h]}"`).join(','))
  ].join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Reportes Administrativos</h1>
			<p>Reportes globales del sistema</p>
		</div>

		<div class="grid grid-cols-12 gap-8 w-full">
			<BaseCard variant="outlined" class="col-span-12 md:col-span-6 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="size-10 flex justify-center items-center bg-primary rounded-full">
						<i class="fa-solid fa-chart-line text-lg text-white" aria-hidden="true"></i>
					</div>
					<h2 class="text-xl font-bold">Reporte de Negocios</h2>
					<p class="text-gray-500">Análisis de crecimiento de negocios.</p>
					<BaseButton text="Descargar CSV" variant="outlined" @click="downloadCSV('businesses')" />
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="size-10 flex justify-center items-center bg-secondary rounded-full">
						<i class="fa-solid fa-chart-pie text-lg text-white" aria-hidden="true"></i>
					</div>
					<h2 class="text-xl font-bold">Reporte de Ingresos</h2>
					<p class="text-gray-500">Resumen de ingresos por suscripciones.</p>
					<BaseButton text="Descargar CSV" variant="outlined" @click="downloadCSV('revenue')" />
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="size-10 flex justify-center items-center bg-green-500 rounded-full">
						<i class="fa-solid fa-users text-lg text-white" aria-hidden="true"></i>
					</div>
					<h2 class="text-xl font-bold">Reporte de Usuarios</h2>
					<p class="text-gray-500">Estadísticas de usuarios registrados.</p>
					<BaseButton text="Descargar CSV" variant="outlined" @click="downloadCSV('users')" />
				</div>
			</BaseCard>
		</div>
	</section>
</template>