<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSalesStore } from '@/stores/sales'
import { useCustomersStore } from '@/stores/customers'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const salesStore = useSalesStore()
const customersStore = useCustomersStore()

const saleId = Number(route.params.saleId)
if (!saleId) router.back()

const loading = ref(true)

onMounted(async () => {
  await customersStore.fetchCustomers()
  await salesStore.fetchSale(saleId)
  loading.value = false
})

const sale = computed(() => salesStore.currentSale)

const getCustomerName = (customerId: number) => {
  const customer = customersStore.customers.find(c => c.id === customerId)
  return customer?.name || `Cliente #${customerId}`
}

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
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Detalle de Venta</h1>
      <p>Información completa de la venta #{{ saleId }}</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando venta...</p>
    </div>

    <div v-else-if="sale" class="w-full grid grid-cols-12 gap-8">
      <BaseCard variant="outlined" class="col-span-full lg:col-span-8">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl text-primary font-bold">Información de la venta</h2>
          <div class="grid grid-cols-2 gap-4 w-full">
            <label class="w-full flex flex-col text-dark">
              Venta #
              <span class="font-semibold">{{ sale.id }}</span>
            </label>
            <label class="w-full flex flex-col text-dark">
              Cliente
              <span class="font-semibold">{{ getCustomerName(sale.customer_id) }}</span>
            </label>
          </div>
          <div class="grid grid-cols-2 gap-4 w-full">
            <label class="w-full flex flex-col text-dark">
              Subtotal
              <span class="font-semibold">{{ formatCurrency(Number(sale.subtotal)) }}</span>
            </label>
            <label class="w-full flex flex-col text-dark">
              Descuento
              <span class="font-semibold">{{ formatCurrency(Number(sale.discount)) }}</span>
            </label>
          </div>
          <div class="grid grid-cols-2 gap-4 w-full">
            <label class="w-full flex flex-col text-dark">
              Impuesto
              <span class="font-semibold">{{ formatCurrency(Number(sale.tax)) }}</span>
            </label>
            <label class="w-full flex flex-col text-dark">
              Total
              <span class="font-bold text-primary text-lg">{{ formatCurrency(Number(sale.total)) }}</span>
            </label>
          </div>
          <label class="w-full flex flex-col text-dark">
            Estado
            <span
              :class="sale.status === 'completed' ? 'text-green-600' : sale.status === 'cancelled' ? 'text-red-600' : 'text-yellow-600'"
              class="font-semibold"
            >
              {{ sale.status }}
            </span>
          </label>
          <label class="w-full flex flex-col text-dark">
            Fecha
            <span class="font-semibold">{{ formatDate(sale.created_at) }}</span>
          </label>
        </div>
      </BaseCard>

      <BaseCard variant="outlined" class="col-span-full lg:col-span-4">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl text-primary font-bold">Acciones</h2>
          <BaseButton :to="'/sales/edit/' + sale.id" text="Editar venta" />
          <BaseButton to="/sales/all" text="Ver todas las ventas" variant="outlined" />
        </div>
      </BaseCard>
    </div>

    <div v-else class="w-full text-center py-8">
      <p class="text-gray-500">Venta no encontrada</p>
      <BaseButton to="/sales/all" text="Volver a la lista" class="mt-4" />
    </div>
  </section>
</template>
