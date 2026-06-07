<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useBillingStore } from '@/stores/billing'
import { useBusinessesStore } from '@/stores/businesses'
import { useToastStore } from '@/stores/toast'
import { apiFetch } from '@/utils/helpers'

const router = useRouter()
const billingStore = useBillingStore()
const businessesStore = useBusinessesStore()
const toastStore = useToastStore()
const loading = ref(false)

onMounted(async () => {
  await Promise.all([
    billingStore.fetchPlans(),
    businessesStore.fetchBusinesses(),
  ])
})

const validationSchema = toTypedSchema(
  z.object({
    business_id: z.number().min(1, 'Selecciona un negocio'),
    plan_id: z.number().min(1, 'Selecciona un plan'),
    start_date: z.string().min(1, 'Fecha de inicio requerida'),
    end_date: z.string().optional(),
  })
)

const { handleSubmit, errors } = useForm({
  validationSchema,
  initialValues: {
    business_id: undefined as number | undefined,
    plan_id: undefined as number | undefined,
    start_date: '',
    end_date: undefined as string | undefined,
  },
})

const { value: business_id } = useField<number>('business_id')
const { value: plan_id } = useField<number>('plan_id')
const { value: start_date } = useField<string>('start_date')
const { value: end_date } = useField<string>('end_date')

const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  try {
    const response = await apiFetch('/api/subscriptions/', {
      method: 'POST',
      body: JSON.stringify({
        business_id: values.business_id,
        plan_id: values.plan_id,
        start_date: values.start_date,
        end_date: values.end_date || null,
        status: 'active',
      }),
    })
    if (!response.ok) {
      const errorData = await response.json()
      toastStore.error(errorData.detail || 'Error al crear suscripción')
      return
    }
    toastStore.success('Suscripción creada correctamente')
    router.push('/billing/subscriptions')
  } catch {
    toastStore.error('Error de conexión')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Crear suscripción</h1>
      <p>Asigna un plan de suscripción a un negocio</p>
    </div>

    <form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
      <label class="w-full flex flex-col text-dark">
        Negocio *
        <select v-model="business_id" class="py-2 px-4 rounded-xl border border-secondary text-primary">
          <option :value="undefined">Seleccionar negocio</option>
          <option v-for="b in businessesStore.businesses" :key="b.id" :value="b.id">
            {{ b.name }}
          </option>
        </select>
        <span v-if="errors.business_id" class="text-red-500 text-sm">{{ errors.business_id }}</span>
      </label>
      <label class="w-full flex flex-col text-dark">
        Plan *
        <select v-model="plan_id" class="py-2 px-4 rounded-xl border border-secondary text-primary">
          <option :value="undefined">Seleccionar plan</option>
          <option v-for="p in billingStore.plans" :key="p.id" :value="p.id">
            {{ p.name }} — ${{ p.price }}/mes
          </option>
        </select>
        <span v-if="errors.plan_id" class="text-red-500 text-sm">{{ errors.plan_id }}</span>
      </label>
      <label class="w-full flex flex-col text-dark">
        Fecha de inicio *
        <input v-model="start_date" type="date" class="py-2 px-4 rounded-xl border border-secondary text-primary" />
        <span v-if="errors.start_date" class="text-red-500 text-sm">{{ errors.start_date }}</span>
      </label>
      <label class="w-full flex flex-col text-dark">
        Fecha de fin (opcional)
        <input v-model="end_date" type="date" class="py-2 px-4 rounded-xl border border-secondary text-primary" />
      </label>
      <BaseButton :text="loading ? 'Creando...' : 'Crear suscripción'" :loading="loading" :disabled="loading" type="submit" />
    </form>
  </section>
</template>
