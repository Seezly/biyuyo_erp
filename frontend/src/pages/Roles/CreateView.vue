<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useRolesStore } from '@/stores/roles'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const rolesStore = useRolesStore()
const toastStore = useToastStore()
const loading = ref(false)

const validationSchema = toTypedSchema(
  z.object({
    name: z.string().min(1, 'El nombre es requerido'),
    description: z.string().min(1, 'La descripción es requerida'),
    is_active: z.boolean().default(true),
  })
)

const { handleSubmit, errors } = useForm({
  validationSchema,
  initialValues: {
    name: '',
    description: '',
    is_active: true,
  },
})

const { value: name } = useField<string>('name')
const { value: description } = useField<string>('description')
const { value: is_active } = useField<boolean>('is_active')

const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  try {
    const role = await rolesStore.createRole(values)
    if (role) {
      toastStore.success('Rol creado correctamente')
      router.push('/admin/roles')
    } else {
      // Error will be handled by the store
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
      <h1 class="text-primary text-2xl font-bold">Añadir rol</h1>
      <p>Completa los datos del nuevo rol</p>
    </div>
    <form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
      <div class="grid grid-cols-2 grid-rows-1 gap-4">
        <label class="w-full flex flex-col text-dark">
          Nombre
          <BaseInput v-model="name" type="text" name="name" placeholder="Nombre del rol" />
          <span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
        </label>
        <label class="w-full flex flex-col text-dark">
          Descripción
          <BaseInput v-model="description" type="text" name="description" placeholder="Descripción del rol" />
          <span v-if="errors.description" class="text-red-500 text-sm">{{ errors.description }}</span>
        </label>
      </div>
      <div class="grid grid-cols-2 grid-rows-1 gap-4 mb-6">
        <label class="w-full flex flex-col text-dark">
          Activo
          <input v-model="is_active" type="checkbox" class="rounded border-gray-300 text-primary" />
        </label>
      </div>
      <BaseButton :text="loading ? 'Creando...' : 'Agregar rol'" :disabled="loading" type="submit" />
    </form>
  </section>
</template>