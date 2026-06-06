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
  })
)

const { handleSubmit, errors } = useForm({
  validationSchema,
  initialValues: {
    name: '',
  },
})

const { value: name } = useField<string>('name')

const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  try {
    const role = await rolesStore.createRole(values)
    if (role) {
      toastStore.success('Rol creado correctamente')
      router.push('/admin/roles')
    }
  } catch {
    toastStore.error('Error de conexion')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Agregar rol</h1>
      <p>Completa los datos del nuevo rol</p>
    </div>
    <form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
      <label class="w-full flex flex-col text-dark">
        Nombre
        <BaseInput v-model="name" type="text" name="name" placeholder="Nombre del rol" />
        <span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
      </label>
      <BaseButton :text="loading ? 'Creando...' : 'Agregar rol'" :loading="loading" :disabled="loading" type="submit" />
    </form>
  </section>
</template>
