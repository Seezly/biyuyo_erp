<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBillingStore } from '@/stores/billing'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const billingStore = useBillingStore()

const subscription = ref<any>(null)
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
  const id = Number(route.params.subscriptionId || route.params.id)
  if (!id) {
    router.push('/billing/subscriptions')
    return
  }
  subscription.value = await billingStore.fetchSubscriptionById(id)
  loading.value = false
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Detalle de suscripción</h1>
      <p>Información de la suscripción</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando suscripción...</p>
    </div>

    <div v-else-if="!subscription" class="w-full text-center py-8">
      <p class="text-gray-500">Suscripción no encontrada</p>
    </div>

    <template v-else>
      <BaseCard variant="outlined" class="w-full">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl text-primary font-bold">Suscripción #{{ subscription.id }}</h2>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Estado</p>
              <p class="text-dark">{{ subscription.status }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Plan</p>
              <p class="text-dark">{{ subscription.plan_name || `Plan #${subscription.plan}` }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Fecha de inicio</p>
              <p class="text-dark">{{ formatDate(subscription.start_date) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Fecha de fin</p>
              <p class="text-dark">{{ subscription.end_date ? formatDate(subscription.end_date) : 'Activa' }}</p>
            </div>
          </div>
        </div>
      </BaseCard>
      <div class="flex gap-4">
        <BaseButton variant="outlined" text="Volver" @click="router.push('/billing/subscriptions')" />
      </div>
    </template>
  </section>
</template>
