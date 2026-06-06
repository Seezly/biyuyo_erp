<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useBillingStore } from '@/stores/billing'
import { useToastStore } from '@/stores/toast'
import { apiFetch } from '@/utils/helpers'

const router = useRouter()
const route = useRoute()
const billingStore = useBillingStore()
const toastStore = useToastStore()
const loading = ref(false)
const saving = ref(false)

const subscriptionId = Number(route.params.subscriptionId)
if (!subscriptionId) {
  router.back()
}

const validationSchema = toTypedSchema(
  z.object({
    user_id: z.number().min(1, 'Selecciona un usuario'),
    plan_id: z.number().min(1, 'Selecciona un plan'),
    start_date: z.string().min(1, 'Fecha de inicio requerida'),
    end_date: z.string().optional(),
    is_active: z.boolean().default(true),
  })
)

const { handleSubmit, errors, setValues } = useForm({
  validationSchema,
  initialValues: {
    user_id: undefined as number | undefined,
    plan_id: undefined as number | undefined,
    start_date: '',
    end_date: undefined as string | undefined,
    is_active: true,
  },
})

const { value: user_id } = useField<number>('user_id')
const { value: plan_id } = useField<number>('plan_id')
const { value: start_date } = useField<string>('start_date')
const { value: end_date } = useField<string>('end_date')
const { value: is_active } = useField<boolean>('is_active')

const fetchSubscription = async () => {
  loading.value = true
  try {
    const response = await apiFetch(`/api/subscriptions/${subscriptionId}/`)
    if (response.ok) {
      const data = await response.json()
      setValues({
        user_id: data.user_id || '',
        plan_id: data.plan_id || '',
        start_date: data.start_date || '',
        end_date: data.end_date || '',
        is_active: data.is_active || true,
      })
    }
  } catch (error) {
    toastStore.error('Error al cargar la suscripción')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSubscription()
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
  } catch (error) {
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
          Usuario *
          <select v-model="user_id" class="py-2 px-4 rounded-xl border border-secondary text-primary">
            <option value="">Seleccionar usuario</option>
            <!-- Options would be populated from auth store -->
          </select>
          <span v-if="errors.user_id" class="text-red-500 text-sm">{{ errors.user_id }}</span>
        </label>
        <label class="w-full flex flex-col text-dark">
          Plan *
          <select v-model="plan_id" class="py-2 px-4 rounded-xl border border-secondary text-primary">
            <option value="">Seleccionar plan</option>
            <!-- Options would be populated from billing store -->
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
          <span v-if="errors.end_date" class="text-red-500 text-sm">{{ errors.end_date }}</span>
        </label>
        <div class="grid grid-cols-2 grid-rows-1 gap-4 mb-6">
          <label class="w-full flex flex-col text-dark">
            Activo
            <input v-model="is_active" type="checkbox" class="rounded border-gray-300 text-primary" />
          </label>
        </div>
        <BaseButton :text="saving ? 'Guardando...' : 'Guardar suscripción'" :loading="saving" :disabled="saving" type="submit" />
      </form>
    </div>
  </section>
</template>