<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useSalesStore } from '@/stores/sales'
import { useToastStore } from '@/stores/toast'
import { apiFetch } from '@/utils/helpers'

const router = useRouter()
const route = useRoute()
const salesStore = useSalesStore()
const toastStore = useToastStore()
const loading = ref(false)
const saving = ref(false)

const paymentId = Number(route.params.paymentId)
if (!paymentId) {
  router.back()
}

const validationSchema = toTypedSchema(
  z.object({
    method: z.string().min(1, 'Selecciona un método de pago'),
    amount: z.number().min(0.01, 'El monto debe ser mayor a 0'),
    reference: z.string().optional(),
    status: z.string().default('completed'),
  })
)

const { handleSubmit, errors, setValues } = useForm({
  validationSchema,
  initialValues: {
    method: 'cash',
    amount: 0,
    reference: '',
    status: 'completed',
  },
})

const { value: method } = useField<string>('method')
const { value: amount } = useField<number>('amount')
const { value: reference } = useField<string>('reference')
const { value: status } = useField<string>('status')

const fetchPayment = async () => {
  loading.value = true
  try {
    const response = await apiFetch(`/api/payments/${paymentId}/`)
    if (response.ok) {
      const data = await response.json()
      setValues({
        method: data.method || 'cash',
        amount: data.amount || 0,
        reference: data.reference || '',
        status: data.status || 'completed',
      })
    }
  } catch {
    toastStore.error('Error al cargar el pago')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPayment()
})

const onSubmit = handleSubmit(async (values) => {
  saving.value = true
  try {
    const response = await apiFetch(`/api/payments/${paymentId}/`, {
      method: 'PATCH',
      body: JSON.stringify(values),
    })
    if (!response.ok) {
      const errorData = await response.json()
      toastStore.error(errorData.detail || 'Error al actualizar pago')
      return
    }
    toastStore.success('Pago actualizado correctamente')
    router.push('/sales/payments')
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
      <h1 class="text-primary text-2xl font-bold">Editar pago</h1>
      <p>Actualiza la información del pago</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando pago...</p>
    </div>

    <div v-else>
      <form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
        <label class="w-full flex flex-col text-dark">
          Método de pago *
          <select v-model="method" class="py-2 px-4 rounded-xl border border-secondary text-primary">
            <option value="cash">Efectivo</option>
            <option value="card">Tarjeta</option>
            <option value="transfer">Transferencia</option>
          </select>
          <span v-if="errors.method" class="text-red-500 text-sm">{{ errors.method }}</span>
        </label>
        <label class="w-full flex flex-col text-dark">
          Monto (USD) *
          <BaseInput v-model="amount" type="number" step="0.01" name="amount" placeholder="0.00" min="0.01" />
          <span v-if="errors.amount" class="text-red-500 text-sm">{{ errors.amount }}</span>
        </label>
        <label class="w-full flex flex-col text-dark">
          Referencia (opcional)
          <BaseInput v-model="reference" type="text" name="reference" placeholder="Número de referencia" />
        </label>
        <label class="w-full flex flex-col text-dark">
          Estado
          <select v-model="status" class="py-2 px-4 rounded-xl border border-secondary text-primary">
            <option value="completed">Completado</option>
            <option value="pending">Pendiente</option>
            <option value="cancelled">Cancelado</option>
          </select>
        </label>
        <BaseButton :text="saving ? 'Guardando...' : 'Guardar pago'" :loading="saving" :disabled="saving" type="submit" />
      </form>
    </div>
  </section>
</template>
