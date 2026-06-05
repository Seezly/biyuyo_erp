<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBillingStore } from '@/stores/billing'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const billingStore = useBillingStore()

const plan = ref<any>(null)
const loading = ref(true)

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('es-VE', {
    style: 'currency',
    currency: 'USD',
  }).format(value)
}

onMounted(async () => {
  const id = Number(route.params.planId || route.params.id)
  if (!id) {
    router.push('/billing/plans')
    return
  }
  plan.value = await billingStore.fetchPlan(id)
  loading.value = false
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Detalle de plan</h1>
      <p>Información del plan</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando plan...</p>
    </div>

    <div v-else-if="!plan" class="w-full text-center py-8">
      <p class="text-gray-500">Plan no encontrado</p>
    </div>

    <template v-else>
      <BaseCard variant="outlined" class="w-full">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl text-primary font-bold">{{ plan.name }}</h2>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Precio</p>
              <p class="text-dark">{{ formatCurrency(plan.price) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Máximo de usuarios</p>
              <p class="text-dark">{{ plan.max_users }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Máximo de productos</p>
              <p class="text-dark">{{ plan.max_products }}</p>
            </div>
          </div>
        </div>
      </BaseCard>
      <div class="flex gap-4">
        <BaseButton variant="outlined" text="Volver" @click="router.push('/billing/plans')" />
        <BaseButton text="Editar" :to="'/billing/plans/edit/' + plan.id" />
      </div>
    </template>
  </section>
</template>
