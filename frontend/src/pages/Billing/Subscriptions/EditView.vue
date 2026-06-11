<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import { useBillingStore } from '@/stores/billing'
import { useBusinessesStore } from '@/stores/businesses'
import { useToastStore } from '@/stores/toast'
import { apiFetch } from '@/utils/helpers'

const router = useRouter()
const route = useRoute()
const billingStore = useBillingStore()
const businessesStore = useBusinessesStore()
const toastStore = useToastStore()
const saving = ref(false)
const loading = ref(true)

const subscriptionId = Number(route.params.subscriptionId)
if (!subscriptionId) {
  router.back()
}

const validationSchema = toTypedSchema(
  z.object({
    business_id: z.number().min(1, 'Selecciona un negocio'),
    plan_id: z.number().min(1, 'Selecciona un plan'),
    status: z.string().min(1, 'Selecciona un estado'),
    start_date: z.string().min(1, 'Fecha de inicio requerida'),
    end_date: z.string().optional(),
  })
)

const { handleSubmit, errors, setValues } = useForm({
  validationSchema,
  initialValues: {
    business_id: undefined as number | undefined,
    plan_id: undefined as number | undefined,
    status: 'active',
    start_date: '',
    end_date: undefined as string | undefined,
  },
})

const { value: business_id } = useField<number>('business_id')
const { value: plan_id } = useField<number>('plan_id')
const { value: status } = useField<string>('status')
const { value: start_date } = useField<string>('start_date')
const { value: end_date } = useField<string>('end_date')

onMounted(async () => {
  await Promise.all([
    billingStore.fetchPlans(),
    businessesStore.fetchBusinesses(),
  ])
  try {
    const response = await apiFetch(`/api/subscriptions/${subscriptionId}/`)
    if (response.ok) {
      const data = await response.json()
      setValues({
        business_id: data.business_id || undefined,
        plan_id: data.plan_id || undefined,
        status: data.status || 'active',
        start_date: data.start_date || '',
        end_date: data.end_date || undefined,
      })
    }
  } catch {
    toastStore.error('Error al cargar la suscripción')
  } finally {
    loading.value = false
  }
})

const onSubmit = handleSubmit(async (values) => {
  saving.value = true
  try {
    const response = await apiFetch(`/api/subscriptions/${subscriptionId}/`, {
      method: 'PATCH',
      body: JSON.stringify(values),
    })

    if (!response.ok) {
      const errorData = await response.json()
      toastStore.error(errorData.detail || 'Error al actualizar suscripción')
      return
    }

    toastStore.success('Suscripción actualizada correctamente')
    router.push('/billing/subscriptions')
  } catch {
    toastStore.error('Error de conexión')
  } finally {
    saving.value = false
  }
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Editar suscripción</h1>
      <p>Actualiza la información de la suscripción</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando suscripción...</p>
    </div>

    <div v-else>
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
          Estado *
          <select v-model="status" class="py-2 px-4 rounded-xl border border-secondary text-primary">
            <option value="active">Activo</option>
            <option value="inactive">Inactivo</option>
            <option value="cancelled">Cancelado</option>
          </select>
          <span v-if="errors.status" class="text-red-500 text-sm">{{ errors.status }}</span>
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
        <BaseButton :text="saving ? 'Guardando...' : 'Guardar suscripción'" :loading="saving" :disabled="saving" type="submit" />
      </form>
    </div>
  </section>
</template>
