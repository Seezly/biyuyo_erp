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

const router = useRouter()
const route = useRoute()
const salesStore = useSalesStore()
const toastStore = useToastStore()
const loading = ref(false)
const saving = ref(false)

const saleId = Number(route.params.id)

const validationSchema = toTypedSchema(
  z.object({
    customer_id: z.number().min(1, 'Selecciona un cliente'),
    total: z.number().min(0, 'El total debe ser positivo').optional(),
    status: z.string().default('pending'),
    payment_status: z.string().default('pending'),
  })
)

const { handleSubmit, errors, setValues } = useForm({
  validationSchema,
  initialValues: {
    customer_id: undefined as number | undefined,
    total: undefined as number | undefined,
    status: 'pending',
    payment_status: 'pending',
  },
})

const { value: customer_id } = useField<number>('customer_id')
const { value: total } = useField<number | undefined>('total')
const { value: status } = useField<string>('status')
const { value: payment_status } = useField<string>('payment_status')

const fetchSale = async () => {
  loading.value = true
  try {
    await salesStore.fetchSale(saleId)
    const sale = salesStore.currentSale
    if (sale) {
      setValues({
        customer_id: sale.customer ? Number(sale.customer) : undefined,
        total: sale.total ? Number(sale.total) : undefined,
        status: sale.status || 'pending',
        payment_status: sale.payment_status || 'pending',
      })
    }
  } catch (error) {
    toastStore.error('Error al cargar la venta')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSale()
})

const onSubmit = handleSubmit(async (values) => {
  saving.value = true
  try {
    const updatedSale = await salesStore.updateSale(saleId, values)
    if (updatedSale) {
      // Success toast will be handled by the store
      router.push('/sales')
    }
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
      <h1 class="text-primary text-2xl font-bold">Editar venta</h1>
      <p>Actualiza la información de la venta</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando venta...</p>
    </div>

    <div v-else>
      <form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
        <label class="w-full flex flex-col text-dark">
          Cliente *
           <select v-model="customer_id" class="py-2 px-4 rounded-xl border border-secondary text-primary">
             <option value="">Seleccionar cliente</option>
             <!-- Options would be populated from customers store -->
           </select>
          <span v-if="errors.customer_id" class="text-red-500 text-sm">{{ errors.customer_id }}</span>
        </label>
        <label class="w-full flex flex-col text-dark">
          Total
          <BaseInput v-model="total" type="number" step="0.01" name="total" placeholder="0.00" />
          <span v-if="errors.total" class="text-red-500 text-sm">{{ errors.total }}</span>
        </label>
        <label class="w-full flex flex-col text-dark">
          Estado
          <select v-model="status" class="py-2 px-4 rounded-xl border border-secondary text-primary">
            <option value="pending">Pendiente</option>
            <option value="completed">Completada</option>
            <option value="cancelled">Cancelada</option>
          </select>
          <span v-if="errors.status" class="text-red-500 text-sm">{{ errors.status }}</span>
        </label>
        <label class="w-full flex flex-col text-dark">
          Estado de pago
          <select v-model="payment_status" class="py-2 px-4 rounded-xl border border-secondary text-primary">
            <option value="pending">Pendiente</option>
            <option value="paid">Pagada</option>
            <option value="partial">Parcial</option>
            <option value="failed">Fallida</option>
          </select>
          <span v-if="errors.payment_status" class="text-red-500 text-sm">{{ errors.payment_status }}</span>
        </label>
        <BaseButton :text="saving ? 'Guardando...' : 'Guardar venta'" :disabled="saving" type="submit" />
      </form>
    </div>
  </section>
</template>