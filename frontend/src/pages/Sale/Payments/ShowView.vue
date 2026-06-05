<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSalesStore } from '@/stores/sales'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const salesStore = useSalesStore()

const payment = ref<any>(null)
const loading = ref(true)

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-VE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('es-VE', {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}

onMounted(async () => {
  const id = Number(route.params.paymentId || route.params.id)
  if (!id) {
    router.push('/sales/all')
    return
  }
  payment.value = await salesStore.fetchPaymentById(id)
  loading.value = false
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Detalle de pago</h1>
      <p>Información del pago</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando pago...</p>
    </div>

    <div v-else-if="!payment" class="w-full text-center py-8">
      <p class="text-gray-500">Pago no encontrado</p>
    </div>

    <template v-else>
      <BaseCard variant="outlined" class="w-full">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl text-primary font-bold">Pago #{{ payment.id }}</h2>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Método de pago</p>
              <p class="text-dark">{{ payment.method }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Monto</p>
              <p class="text-dark">{{ formatCurrency(payment.amount) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Referencia</p>
              <p class="text-dark">{{ payment.reference || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Estado</p>
              <p class="text-dark">{{ payment.status }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Venta asociada</p>
              <p class="text-dark">#{{ payment.sale }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Fecha de creación</p>
              <p class="text-dark">{{ formatDate(payment.created_at) }}</p>
            </div>
          </div>
        </div>
      </BaseCard>
      <div class="flex gap-4">
        <BaseButton variant="outlined" text="Volver" @click="router.push('/sales/all')" />
      </div>
    </template>
  </section>
</template>
