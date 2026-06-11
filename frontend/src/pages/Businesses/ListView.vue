<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useBusinessesStore } from '@/stores/businesses'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseAlert from '@/components/ui/BaseAlert.vue'

const router = useRouter()
const route = useRoute()
const businessesStore = useBusinessesStore()

const search = ref('')
const showDeleteAlert = ref(false)
const businessToDelete = ref<number | null>(null)

onMounted(() => {
  search.value = (route.query.search as string) || ''
  fetchBusinesses()
})

const fetchBusinesses = () => {
  const params: {
    search?: string
    ordering?: string
    page?: string
  } = {}

  if (search.value) params.search = search.value
  if (route.query.ordering) params.ordering = route.query.ordering as string
  if (route.query.page) params.page = route.query.page as string

  businessesStore.fetchBusinesses(params)
}

watch(search, () => {
  const query: Record<string, string> = {}
  if (search.value) query.search = search.value
  router.push({ query })
})

const confirmDelete = (id: number) => {
  businessToDelete.value = id
  showDeleteAlert.value = true
}

const handleDelete = async () => {
  if (businessToDelete.value) {
    await businessesStore.deleteBusiness(businessToDelete.value)
    showDeleteAlert.value = false
    businessToDelete.value = null
  }
}

const cancelDelete = () => {
  showDeleteAlert.value = false
  businessToDelete.value = null
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-VE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Negocios</h1>
      <p>Administra y controla los negocios registrados en el sistema</p>
    </div>

    <div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
      <BaseButton to="/admin/businesses/add" text="Añadir negocio" class="col-span-12 lg:col-span-3" />
      <BaseInput v-model="search" placeholder="Buscar negocio por nombre o RIF" class="col-span-12 lg:col-span-9" />
    </div>

    <div v-if="businessesStore.loading" class="w-full text-center py-8">
      <p>Cargando negocios...</p>
    </div>

    <div v-else-if="businessesStore.businesses.length === 0" class="w-full text-center py-8">
      <p class="text-gray-500">No hay negocios disponibles</p>
    </div>

    <div v-else class="w-full">
      <BaseCard variant="outlined" class="col-span-12">
        <h2 class="text-primary font-semibold text-xl mb-8">Negocios registrados</h2>
        <table class="min-w-full divide-y-2 divide-gray-200">
          <thead class="ltr:text-left rtl:text-right">
            <tr class="*:font-medium *:text-gray-900">
              <th class="px-4 py-2 whitespace-nowrap">Nombre</th>
              <th class="px-4 py-2 whitespace-nowrap">RIF</th>
              <th class="px-4 py-2 whitespace-nowrap">Email</th>
              <th class="px-4 py-2 whitespace-nowrap">Teléfono</th>
              <th class="px-4 py-2 whitespace-nowrap">Dirección</th>
              <th class="px-4 py-2 whitespace-nowrap">Estado</th>
              <th class="px-4 py-2 whitespace-nowrap">Municipio</th>
              <th class="px-4 py-2 whitespace-nowrap text-right">Acciones</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-200 *:even:bg-gray-50">
            <tr v-for="business in businessesStore.businesses" :key="business.id" class="*:text-gray-900 *:first:font-medium">
              <td class="px-4 py-2 whitespace-nowrap">{{ business.name }}</td>
              <td class="px-4 py-2 whitespace-nowrap">{{ business.rif }}</td>
              <td class="px-4 py-2 whitespace-nowrap">{{ business.email }}</td>
              <td class="px-4 py-2 whitespace-nowrap">{{ business.phone }}</td>
              <td class="px-4 py-2 whitespace-nowrap">{{ business.address }}</td>
              <td class="px-4 py-2 whitespace-nowrap">{{ business.state }}</td>
              <td class="px-4 py-2 whitespace-nowrap">{{ business.municipality }}</td>
              <td class="px-4 py-2 whitespace-nowrap flex justify-end items-center gap-2">
                <BaseButton :to="'/admin/businesses/edit/' + business.id" text="Editar" variant="secondary" width="auto" />
                <BaseButton text="Eliminar" width="auto" @click="confirmDelete(business.id)" />
              </td>
            </tr>
          </tbody>
        </table>
      </BaseCard>
    </div>
  </section>

  <BaseAlert
    :visible="showDeleteAlert"
    title="Eliminar negocio"
    subtitle="Esta acción no se puede deshacer"
    description="¿Estás seguro de que deseas eliminar este negocio?"
    variant="delete"
    :cta="'Eliminar'"
    :cancel="true"
    @update="showDeleteAlert = false"
    @close="cancelDelete"
    @next="handleDelete"
  />
</template>