<script setup lang="ts">
import { ref } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Estadísticas Detalladas</h1>
      <p>Análisis profundo del rendimiento del sistema</p>
    </div>

    <div class="grid grid-cols-12 gap-8 w-full">
      <BaseCard variant="outlined" class="col-span-12">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl font-bold text-primary">Usuarios por Negocio</h2>
          <p class="text-gray-500">Distribución de usuarios en los diferentes negocios registrados.</p>
          <BaseButton text="Exportar datos" variant="outlined" to="/reports?reportType=business" />
        </div>
      </BaseCard>

      <BaseCard variant="outlined" class="col-span-12">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl font-bold text-primary">Suscripciones por Plan</h2>
          <p class="text-gray-500">Análisis de planes activos y su distribución.</p>
          <BaseButton text="Ver detalles" variant="outlined" to="/billing/plans" />
        </div>
      </BaseCard>

      <BaseCard variant="outlined" class="col-span-12">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl font-bold text-primary">Ingresos Mensuales</h2>
          <p class="text-gray-500">Reporte de ingresos por suscripciones.</p>
          <BaseButton text="Descargar reporte" variant="outlined" to="/billing/invoices" />
        </div>
      </BaseCard>
    </div>
  </section>
</template>