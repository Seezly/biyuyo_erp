<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuditStore } from '@/stores/audit'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
const route = useRoute()
const auditStore = useAuditStore()

const logId = Number(route.params.id)
if (isNaN(logId)) router.back()
const loading = ref(true)
const error = ref<string | null>(null)
const log = ref<any>(null)

const fetchAuditLog = async () => {
  loading.value = true
  error.value = null
  try {
    const logData = await auditStore.fetchAuditLog(logId)
    if (logData) {
      log.value = logData
    } else {
      error.value = 'Registro de auditoría no encontrado'
    }
  } catch (e: any) {
    error.value = e.message || 'Error al cargar el registro de auditoría'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAuditLog()
})

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
    second: '2-digit',
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

const formatChanges = (changes: any) => {
  if (!changes) return []
  return Object.entries(changes).map(([key, value]: [string, any]) => ({
    key,
    value
  }))
}
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Detalle de Auditoría</h1>
      <p>Información detallada del registro de auditoría</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando registro de auditoría...</p>
    </div>

    <div v-else-if="error" class="w-full text-center py-8">
      <p class="text-red-500">{{ error }}</p>
    </div>

    <div v-else-if="log" class="w-full">
      <BaseCard variant="outlined">
        <div class="flex flex-col gap-4">
          <div class="flex justify-between items-start">
            <div>
              <h2 class="text-primary text-xl font-bold">
                {{ log.action }}
              </h2>
              <p class="text-sm text-gray-500">
                {{ log.model_name }} • {{ formatDate(log.timestamp) }} {{ formatTime(log.timestamp) }}
              </p>
            </div>
            <div class="flex items-center gap-2">
              <BaseButton
                :to="'/audit'"
                text="Volver al listado"
                variant="outlined"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div class="space-y-4">
              <div class="border-b pb-2">
                <h3 class="font-semibold text-sm uppercase tracking-wider text-gray-500">
                  Información del usuario
                </h3>
                <p class="text-lg font-medium">
                  {{ log.user?.email || 'Sistema' }}
                </p>
              </div>

              <div class="border-b pb-2">
                <h3 class="font-semibold text-sm uppercase tracking-wider text-gray-500">
                  Información del objeto
                </h3>
                <div class="space-y-2">
                  <p><strong>Modelo:</strong> {{ log.model_name }}</p>
                  <p><strong>ID del objeto:</strong> {{ log.object_id || 'N/A' }}</p>
                  <p><strong>Representación:</strong> {{ log.object_repr || 'N/A' }}</p>
                </div>
              </div>

              <div class="border-b pb-2">
                <h3 class="font-semibold text-sm uppercase tracking-wider text-gray-500">
                  Detalles de la acción
                </h3>
                <div class="space-y-2">
                  <p><strong>Acción:</strong>
                    <span :class="['rounded-full py-1 px-2 text-xs font-bold', getActionClass(log.action)]">
                      {{ log.action }}
                    </span>
                  </p>
                  <p><strong>Descripción:</strong> {{ log.description || 'N/A' }}</p>
                  <p><strong>Dirección IP:</strong> {{ log.ip_address || 'N/A' }}</p>
                  <p><strong>User Agent:</strong> {{ log.user_agent || 'N/A' }}</p>
                </div>
              </div>
            </div>

            <div v-if="log.changes && Object.keys(log.changes).length > 0">
              <div class="border-b pb-2">
                <h3 class="font-semibold text-sm uppercase tracking-wider text-gray-500">
                  Cambios detectados
                </h3>
                <div v-if="formatChanges(log.changes).length > 0" class="space-y-2">
                  <div v-for="(change, index) in formatChanges(log.changes)" :key="index"
                       class="border p-3 rounded">
                    <div class="flex justify-between items-start">
                      <span class="font-medium">{{ change.key }}</span>
                      <span class="text-gray-500 text-sm">→</span>
                    </div>
                    <p class="mt-1">{{ change.value }}</p>
                  </div>
                </div>
                <p v-else class="text-gray-500 text-sm">
                  No se detectaron cambios específicos en este registro.
                </p>
              </div>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>
  </section>
</template>