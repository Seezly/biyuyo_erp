<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useSalesStore } from '@/stores/sales'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const salesStore = useSalesStore()
const toastStore = useToastStore()
const loading = ref(false)

onMounted(async () => {
  await salesStore.fetchSales()
})

const validationSchema = toTypedSchema(
  z.object({
    sale: z.number().min(1, 'Selecciona una venta'),
    method: z.string().min(1, 'Selecciona un método de pago'),
    amount: z.number().min(0.01, 'El monto debe ser mayor a 0'),
    reference: z.string().optional(),
  })
)

const { handleSubmit, errors } = useForm({
  validationSchema,
  initialValues: {
    sale: undefined as number | undefined,
    method: 'cash',
    amount: 0,
    reference: '',
  },
})

const { value: sale } = useField<number>('sale')
const { value: method } = useField<string>('method')
const { value: amount } = useField<number>('amount')
const { value: reference } = useField<string>('reference')

const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  try {
    const result = await salesStore.createPayment({
      sale: values.sale!,
      method: values.method,
      amount: values.amount,
      reference: values.reference || '',
      status: 'pending',
    })
    if (result) {
      router.push('/sales/payments')
    }
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
      <h1 class="text-primary text-2xl font-bold">Registrar pago</h1>
      <p>Registra un nuevo pago recibido</p>
    </div>

    <form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
      <label class="w-full flex flex-col text-dark">
        Venta *
        <select v-model="sale" class="py-2 px-4 rounded-xl border border-secondary text-primary">
          <option :value="undefined">Seleccionar venta</option>
          <option v-for="s in salesStore.sales" :key="s.id" :value="s.id">
            Venta #{{ s.id }} — ${{ s.total }}
          </option>
        </select>
        <span v-if="errors.sale" class="text-red-500 text-sm">{{ errors.sale }}</span>
      </label>
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
      <BaseButton :text="loading ? 'Registrando...' : 'Registrar pago'" :loading="loading" :disabled="loading" type="submit" />
    </form>
  </section>
</template>
