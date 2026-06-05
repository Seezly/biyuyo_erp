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

const groupId = Number(route.params.roleId)

const validationSchema = toTypedSchema(
  z.object({
    name: z.string().min(1, 'El nombre es requerido'),
  })
)

const { handleSubmit, errors, setValues } = useForm({
  validationSchema,
  initialValues: {
    name: '',
  },
})

const { value: name } = useField<string>('name')

const fetchRole = async () => {
  try {
    const role = await rolesStore.getRole(groupId)
    if (role) {
      setValues({ name: role.name || '' })
    }
  } catch {
    toastStore.error('Error al cargar el rol')
  }
}

onMounted(() => {
  fetchRole()
})

const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  try {
    const updated = await rolesStore.updateRole(groupId, values)
    if (updated) {
      toastStore.success('Rol actualizado correctamente')
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
      <h1 class="text-primary text-2xl font-bold">Editar rol</h1>
      <p>Actualiza los datos del rol</p>
    </div>
    <form @submit="onSubmit" class="flex justify-start mx-auto items-center flex-col gap-4 w-full lg:w-md">
      <label class="w-full flex flex-col text-dark">
        Nombre
        <BaseInput v-model="name" type="text" name="name" placeholder="Nombre del rol" />
        <span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
      </label>
      <BaseButton :text="loading ? 'Guardando...' : 'Guardar cambios'" :disabled="loading" type="submit" />
    </form>
  </section>
</template>
