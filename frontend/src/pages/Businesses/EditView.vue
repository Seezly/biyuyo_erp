<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useBusinessesStore } from '@/stores/businesses'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const route = useRoute()
const businessesStore = useBusinessesStore()
const toastStore = useToastStore()
const loading = ref(false)

const businessId = Number(route.params.businessId)
if (!businessId) {
  router.back()
}

const validationSchema = toTypedSchema(
  z.object({
    name: z.string().min(1, 'El nombre es requerido'),
    description: z.string().min(1, 'La descripción es requerida'),
    rif: z.string().min(1, 'El RIF es requerido').regex(/^[VEJGvejg]\d{5,9}$/, 'Formato: V12345678 o E123456789'),
    address: z.string().min(1, 'La dirección es requerida'),
    state: z.string().min(1, 'El estado es requerido'),
    municipality: z.string().min(1, 'El municipio es requerido'),
    phone: z.string().min(1, 'El teléfono es requerido'),
    email: z.string().min(1, 'El email es requerido').email('Email inválido'),
    is_active: z.boolean().default(true),
  })
)

const { handleSubmit, errors, setValues } = useForm({
  validationSchema,
  initialValues: {
    name: '',
    description: '',
    rif: '',
    address: '',
    state: '',
    municipality: '',
    phone: '',
    email: '',
    is_active: true,
  },
})

const { value: name } = useField<string>('name')
const { value: description } = useField<string>('description')
const { value: rif } = useField<string>('rif')
const { value: address } = useField<string>('address')
const { value: state } = useField<string>('state')
const { value: municipality } = useField<string>('municipality')
const { value: phone } = useField<string>('phone')
const { value: email } = useField<string>('email')
const { value: is_active } = useField<boolean>('is_active')

const fetchBusiness = async () => {
  try {
    const business = await businessesStore.getBusiness(businessId)
    if (business) {
      setValues({
        name: business.name || '',
        description: business.description || '',
        rif: business.rif || '',
        address: business.address || '',
        state: business.state || '',
        municipality: business.municipality || '',
        phone: business.phone || '',
        email: business.email || '',
        is_active: business.is_active || true,
      })
    }
  } catch (error) {
    toastStore.error('Error al cargar el negocio')
  }
}

onMounted(() => {
  fetchBusiness()
})

const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  try {
    const business = await businessesStore.updateBusiness(businessId, values)
    if (business) {
      toastStore.success('Negocio actualizado correctamente')
      router.push('/admin/businesses')
    }
  } catch (error) {
    toastStore.error('Error de conexión')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Editar negocio</h1>
      <p>Actualiza los datos del negocio</p>
    </div>
    <form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
      <div class="grid grid-cols-2 grid-rows-1 gap-4">
        <label class="w-full flex flex-col text-dark">
          Nombre
          <BaseInput v-model="name" type="text" name="name" placeholder="Nombre del negocio" />
          <span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
        </label>
        <label class="w-full flex flex-col text-dark">
          RIF
          <BaseInput v-model="rif" type="text" name="rif" placeholder="V12345678" />
          <span v-if="errors.rif" class="text-red-500 text-sm">{{ errors.rif }}</span>
        </label>
      </div>
      <div class="grid grid-cols-2 grid-rows-1 gap-4">
        <label class="w-full flex flex-col text-dark">
          Teléfono
          <BaseInput v-model="phone" type="text" name="phone" placeholder="Teléfono" />
          <span v-if="errors.phone" class="text-red-500 text-sm">{{ errors.phone }}</span>
        </label>
        <label class="w-full flex flex-col text-dark">
          Email
          <BaseInput v-model="email" type="email" name="email" placeholder="Email" />
          <span v-if="errors.email" class="text-red-500 text-sm">{{ errors.email }}</span>
        </label>
      </div>
      <label class="w-full flex flex-col text-dark">
        Dirección
        <BaseInput v-model="address" type="text" name="address" placeholder="Dirección completa" />
        <span v-if="errors.address" class="text-red-500 text-sm">{{ errors.address }}</span>
      </label>
      <div class="grid grid-cols-2 grid-rows-1 gap-4">
        <label class="w-full flex flex-col text-dark">
          Estado
          <BaseInput v-model="state" type="text" name="state" placeholder="Estado" />
          <span v-if="errors.state" class="text-red-500 text-sm">{{ errors.state }}</span>
        </label>
        <label class="w-full flex flex-col text-dark">
          Municipio
          <BaseInput v-model="municipality" type="text" name="municipality" placeholder="Municipio" />
          <span v-if="errors.municipality" class="text-red-500 text-sm">{{ errors.municipality }}</span>
        </label>
      </div>
      <label class="w-full flex flex-col text-dark">
        Descripción
        <BaseInput v-model="description" type="text" name="description" placeholder="Descripción del negocio" />
        <span v-if="errors.description" class="text-red-500 text-sm">{{ errors.description }}</span>
      </label>
      <div class="grid grid-cols-2 grid-rows-1 gap-4 mb-6">
        <label class="w-full flex flex-col text-dark">
          Activo
          <input v-model="is_active" type="checkbox" class="rounded border-gray-300 text-primary" />
        </label>
      </div>
      <BaseButton :text="loading ? 'Guardando...' : 'Editar negocio'" :loading="loading" :disabled="loading" type="submit" />
    </form>
  </section>
</template>