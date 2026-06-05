<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCustomersStore } from '@/stores/customers'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const customersStore = useCustomersStore()

const customer = ref<any>(null)
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

onMounted(async () => {
  const id = Number(route.params.customerId)
  if (!id) {
    router.push('/customers')
    return
  }
  customer.value = await customersStore.fetchCustomer(id)
  loading.value = false
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Detalle de cliente</h1>
      <p>Información del cliente</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando cliente...</p>
    </div>

    <div v-else-if="!customer" class="w-full text-center py-8">
      <p class="text-gray-500">Cliente no encontrado</p>
    </div>

    <template v-else>
      <BaseCard variant="outlined" class="w-full">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl text-primary font-bold">{{ customer.name }}</h2>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Teléfono</p>
              <p class="text-dark">{{ customer.phone || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Cédula/RIF</p>
              <p class="text-dark">{{ customer.identification_number || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Fecha de creación</p>
              <p class="text-dark">{{ formatDate(customer.created_at) }}</p>
            </div>
          </div>
        </div>
      </BaseCard>
      <div class="flex gap-4">
        <BaseButton variant="outlined" text="Volver" @click="router.push('/customers')" />
        <BaseButton text="Editar" :to="'/customers/edit/' + customer.id" />
      </div>
    </template>
  </section>
</template>
