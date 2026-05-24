<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuditStore } from '@/stores/audit'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import Pagination from '@/components/Pagination.vue'

const router = useRouter()
const route = useRoute()
const auditStore = useAuditStore()

const search = ref('')
const actionFilter = ref('')
const modelFilter = ref('')

// Helper function to safely extract page number from query params
const getPageFromQuery = (pageParam: string | string[] | undefined): number => {
  if (Array.isArray(pageParam)) {
    return parseInt(String(pageParam[0])) || 1
  }
  return parseInt(String(pageParam ?? '1')) || 1
}

// Initialize filters from URL query params
onMounted(() => {
  search.value = (route.query.search as string) ?? ''
  actionFilter.value = (route.query.action as string) ?? ''
  modelFilter.value = (route.query.model as string) ?? ''
  fetchAuditLogs()
})

// Fetch audit logs with current filter params
const fetchAuditLogs = () => {
  const params: {
    user_id?: number
    action?: string
    model_name?: string
    start_date?: string
    end_date?: string
    ordering?: string
    page?: string
  } = {}

  if (search.value) {
    // Search across multiple fields
    params.model_name = search.value
  }
  if (actionFilter.value) params.action = actionFilter.value
  if (modelFilter.value) params.model_name = modelFilter.value
  if (route.query.ordering) params.ordering = route.query.ordering as string
  if (route.query.page) params.page = route.query.page as string

  auditStore.fetchAuditLogs(params)
}

// Watch for filter changes and update URL
watch([search, actionFilter, modelFilter], () => {
  const query: Record<string, string> = {}
  if (search.value) query.search = search.value
  if (actionFilter.value) query.action = actionFilter.value
  if (modelFilter.value) query.model = modelFilter.value
  router.push({ query })
}, { deep: true })

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-VE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

const formatTime = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleTimeString('es-VE', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getActionClass = (action: string) => {
  switch (action) {
    case 'create': return 'bg-green-100 text-green-800'
    case 'update': return 'bg-blue-100 text-blue-800'
    case 'delete': return 'bg-red-100 text-red-800'
    case 'login': return 'bg-indigo-100 text-indigo-800'
    case 'logout': return 'bg-gray-100 text-gray-800'
    case 'view': return 'bg-yellow-100 text-yellow-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Registro de Auditoría</h1>
      <p>Historial de actividades y cambios en el sistema</p>
    </div>

    <div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
      <BaseInput v-model="search" placeholder="Buscar por modelo..." class="col-span-12 lg:col-span-4" />
      <BaseInput v-model="actionFilter" placeholder="Filtrar por acción..." class="col-span-12 lg:col-span-4" />
      <BaseInput v-model="modelFilter" placeholder="Filtrar por modelo..." class="col-span-12 lg:col-span-4" />
    </div>

    <div v-if="auditStore.loading" class="w-full text-center py-8">
      <p>Cargando registro de auditoría...</p>
    </div>

    <div v-else-if="auditStore.logs.length === 0" class="w-full text-center py-8">
      <p class="text-gray-500">No hay registros de auditoría disponibles</p>
    </div>

    <div v-else class="w-full">
      <BaseCard variant="outlined" class="overflow-x-auto">
        <table class="min-w-full divide-y-2 divide-gray-200">
          <thead class="ltr:text-left rtl:text-right">
            <tr class="*:font-medium *:text-gray-900">
              <th class="px-4 py-2 whitespace-nowrap">Fecha</th>
              <th class="px-4 py-2 whitespace-nowrap">Usuario</th>
              <th class="px-4 py-2 whitespace-nowrap">Acción</th>
              <th class="px-4 py-2 whitespace-nowrap">Modelo</th>
              <th class="px-4 py-2 whitespace-nowrap">Objeto ID</th>
              <th class="px-4 py-2 whitespace-nowrap">Descripción</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-200 *:even:bg-gray-50">
            <tr v-for="log in auditStore.logs" :key="log.id" class="*:text-gray-900">
              <td class="px-4 py-2 whitespace-nowrap">
                <div class="flex flex-col gap-1">
                  <span class="text-sm">{{ formatDate(log.timestamp) }}</span>
                  <span class="text-xs text-gray-500">{{ formatTime(log.timestamp) }}</span>
                </div>
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                {{ log.user?.email || 'Sistema' }}
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <span :class="['rounded-full py-1 px-2 text-xs font-bold', getActionClass(log.action)]">
                  {{ log.action }}
                </span>
              </td>
              <td class="px-4 py-2 whitespace-nowrap">{{ log.model_name }}</td>
              <td class="px-4 py-2 whitespace-nowrap">{{ log.object_id || '-' }}</td>
              <td class="px-4 py-2 whitespace-nowrap">{{ log.description || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </BaseCard>
      
      <!-- Pagination -->
      <div v-if="auditStore.pagination.count > 0" class="flex justify-center mt-4">
           <Pagination
             :total="auditStore.pagination.count"
             :page="getPageFromQuery(route.query.page as string | string[] | undefined)"
             :pageCount="Math.ceil(auditStore.pagination.count / 10)"
             @update="page => { 
               const query = { ...route.query };
               // Remove any null or undefined values from query
               Object.keys(query).forEach(key => {
                 if (query[key] === null || query[key] === undefined) {
                   delete query[key];
                 }
               });
               // Ensure page is a string
               router.push({ query: { ...query, page: String(page) } });
             }"
           />
      </div>
    </div>
  </section>
</template>