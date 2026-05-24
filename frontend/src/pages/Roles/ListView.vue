<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useRolesStore } from '@/stores/roles'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()
const route = useRoute()
const rolesStore = useRolesStore()

const search = ref('')
const showDeleteAlert = ref(false)
const roleToDelete = ref<number | null>(null)

onMounted(() => {
  search.value = (route.query.search as string) || ''
  fetchRoles()
})

const fetchRoles = () => {
  const params: {
    search?: string
    ordering?: string
    page?: string
  } = {}

  if (search.value) params.search = search.value
  if (route.query.ordering) params.ordering = route.query.ordering as string
  if (route.query.page) params.page = route.query.page as string

  rolesStore.fetchRoles(params)
}

watch(search, () => {
  const query: Record<string, string> = {}
  if (search.value) query.search = search.value
  router.push({ query })
})

const confirmDelete = (id: number) => {
  roleToDelete.value = id
  showDeleteAlert.value = true
}

const handleDelete = async () => {
  if (roleToDelete.value) {
    await rolesStore.deleteRole(roleToDelete.value)
    showDeleteAlert.value = false
    roleToDelete.value = null
  }
}

const cancelDelete = () => {
  showDeleteAlert.value = false
  roleToDelete.value = null
}
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Roles</h1>
      <p>Administra y controla los roles del sistema</p>
    </div>

    <div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
      <BaseButton to="/admin/roles/add" text="Añadir rol" class="col-span-12 lg:col-span-3" />
      <BaseInput v-model="search" placeholder="Buscar rol por nombre o descripción" class="col-span-12 lg:col-span-9" />
    </div>

    <div v-if="rolesStore.loading" class="w-full text-center py-8">
      <p>Cargando roles...</p>
    </div>

    <div v-else-if="rolesStore.roles.length === 0" class="w-full text-center py-8">
      <p class="text-gray-500">No hay roles disponibles</p>
    </div>

    <div v-else class="w-full">
      <BaseCard variant="outlined" class="col-span-12">
        <h2 class="text-primary font-semibold text-xl mb-8">Roles del sistema</h2>
        <table class="min-w-full divide-y-2 divide-gray-200">
          <thead class="ltr:text-left rtl:text-right">
            <tr class="*:font-medium *:text-gray-900">
              <th class="px-4 py-2 whitespace-nowrap">Nombre</th>
              <th class="px-4 py-2 whitespace-nowrap">Descripción</th>
              <th class="px-4 py-2 whitespace-nowrap">Estado</th>
              <th class="px-4 py-2 whitespace-nowrap text-right">Acciones</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-200 *:even:bg-gray-50">
            <tr v-for="role in rolesStore.roles" :key="role.id" class="*:text-gray-900 *:first:font-medium">
              <td class="px-4 py-2 whitespace-nowrap">{{ role.name }}</td>
              <td class="px-4 py-2 whitespace-nowrap">{{ role.description }}</td>
              <td class="px-4 py-2 whitespace-nowrap">
                <span v-if="role.is_active" class="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded">
                  Activo
                </span>
                <span v-else class="bg-red-100 text-red-800 text-xs font-bold px-2 py-1 rounded">
                  Inactivo
                </span>
              </td>
              <td class="px-4 py-2 whitespace-nowrap flex justify-end items-center gap-2">
                <BaseButton :to="'/admin/roles/edit/' + role.id" text="Editar" variant="secondary" width="auto" />
                <BaseButton text="Eliminar" width="auto" @click="confirmDelete(role.id)" />
              </td>
            </tr>
          </tbody>
        </table>
      </BaseCard>
    </div>
  </section>
</template>