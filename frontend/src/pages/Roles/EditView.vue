<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useForm, useField } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import { useRolesStore } from '@/stores/roles'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const route = useRoute()
const rolesStore = useRolesStore()
const toastStore = useToastStore()
const loading = ref(false)

const roleId = Number(route.params.roleId)

const validationSchema = toTypedSchema(
  z.object({
    name: z.string().min(1, 'El nombre es requerido'),
    description: z.string().min(1, 'La descripción es requerida'),
    is_active: z.boolean().default(true),
  })
)

const { handleSubmit, errors, setValues } = useForm({
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

const fetchRole = async () => {
  try {
    const role = await rolesStore.getRole(roleId)
    if (role) {
      setValues({
        name: role.name || '',
        description: role.description || '',
        is_active: role.is_active || true,
      })
    }
  } catch (error) {
    toastStore.error('Error al cargar el rol')
  }
}

onMounted(() => {
  fetchRole()
})

const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  try {
    const role = await rolesStore.updateRole(roleId, values)
    if (role) {
      toastStore.success('Rol actualizado correctamente')
      router.push('/admin/roles')
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
      <h1 class="text-primary text-2xl font-bold">Editar rol</h1>
      <p>Actualiza los datos del rol</p>
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
      <BaseButton :text="loading ? 'Guardando...' : 'Editar rol'" :disabled="loading" type="submit" />
    </form>
  </section>
</template>