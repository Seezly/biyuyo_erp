<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReportsStore } from '@/stores/reports'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const reportsStore = useReportsStore()

const reportType = ref(route.params.reportType as string)

const reportTypes: Record<string, { title: string; description: string }> = {
  sales: { title: 'Reporte de Ventas', description: 'Análisis detallado de ventas' },
  inventory: { title: 'Reporte de Inventario', description: 'Estado del inventario' },
  customers: { title: 'Reporte de Clientes', description: 'Estadísticas de clientes' },
}

const currentReport = reportTypes[reportType.value] || { title: 'Reporte personalizado', description: '' }

const downloadReport = () => {
  let data: any[] = []
  let filename = `${reportType.value}_reporte.csv`

  if (reportType.value === 'sales' && reportsStore.sales) {
    data = [{ 'Ventas Totales': reportsStore.sales.total_sales, 'Cantidad': reportsStore.sales.count, 'Promedio': reportsStore.sales.average_sale }]
  } else if (reportType.value === 'inventory' && reportsStore.inventory) {
    data = [{ 'Productos': reportsStore.inventory.total_products, 'Valor': reportsStore.inventory.total_value, 'Stock Bajo': reportsStore.inventory.low_stock_count, 'Sin Stock': reportsStore.inventory.out_of_stock_count }]
  }

  if (data.length === 0) return

  const headers = Object.keys(data[0])
  const csv = [headers.join(','), ...data.map(row => headers.map(h => `"${(row as any)[h]}"`).join(','))].join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
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
      <h1 class="text-primary text-2xl font-bold">{{ currentReport.title }}</h1>
      <p>{{ currentReport.description }}</p>
    </div>

    <BaseCard variant="outlined" class="w-full">
      <div class="flex flex-col gap-4">
        <p class="text-gray-500">Selecciona un tipo de reporte para generar.</p>
        <div class="flex gap-4">
          <BaseButton text="Ventas" @click="router.push('/reports/sales')" />
          <BaseButton text="Inventario" variant="outlined" @click="router.push('/reports/inventory')" />
        </div>
      </div>
    </BaseCard>

    <div class="flex gap-4">
      <BaseButton text="Descargar CSV" @click="downloadReport" />
      <BaseButton text="Volver" variant="outlined" @click="router.push('/reports')" />
    </div>
  </section>
</template>
