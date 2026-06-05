<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBusinessesStore } from '@/stores/businesses'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const businessesStore = useBusinessesStore()

const business = ref<any>(null)
const loading = ref(true)

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('es-VE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

onMounted(async () => {
  const id = Number(route.params.businessId)
  if (!id) {
    router.push('/admin/businesses')
    return
  }
  business.value = await businessesStore.getBusiness(id)
  loading.value = false
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Detalle de negocio</h1>
      <p>Información del negocio</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando negocio...</p>
    </div>

    <div v-else-if="!business" class="w-full text-center py-8">
      <p class="text-gray-500">Negocio no encontrado</p>
    </div>

    <template v-else>
      <BaseCard variant="outlined" class="w-full">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl text-primary font-bold">{{ business.name }}</h2>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Descripción</p>
              <p class="text-dark">{{ business.description || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">RIF</p>
              <p class="text-dark">{{ business.rif || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Correo electrónico</p>
              <p class="text-dark">{{ business.email || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Teléfono</p>
              <p class="text-dark">{{ business.phone || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Dirección</p>
              <p class="text-dark">{{ business.address || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Estado</p>
              <p class="text-dark">{{ business.state || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Municipio</p>
              <p class="text-dark">{{ business.municipality || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Activo</p>
              <p class="text-dark">{{ business.is_active ? 'Sí' : 'No' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Fecha de inicio</p>
              <p class="text-dark">{{ formatDate(business.start_date) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Fecha de creación</p>
              <p class="text-dark">{{ formatDate(business.created_at) }}</p>
            </div>
          </div>
        </div>
      </BaseCard>
      <div class="flex gap-4">
        <BaseButton variant="outlined" text="Volver" @click="router.push('/admin/businesses')" />
        <BaseButton text="Editar" :to="'/admin/businesses/edit/' + business.id" />
      </div>
    </template>
  </section>
</template>
