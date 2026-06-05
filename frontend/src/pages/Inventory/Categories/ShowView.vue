<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInventoryStore } from '@/stores/inventory'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const route = useRoute()
const router = useRouter()
const inventoryStore = useInventoryStore()

const category = ref<any>(null)
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
  const id = Number(route.params.categoryId)
  if (!id) {
    router.push('/inventory/categories')
    return
  }
  category.value = await inventoryStore.fetchCategoryById(id)
  loading.value = false
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Detalle de categoría</h1>
      <p>Información de la categoría</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando categoría...</p>
    </div>

    <div v-else-if="!category" class="w-full text-center py-8">
      <p class="text-gray-500">Categoría no encontrada</p>
    </div>

    <template v-else>
      <BaseCard variant="outlined" class="w-full">
        <div class="flex flex-col gap-4">
          <h2 class="text-xl text-primary font-bold">{{ category.name }}</h2>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">ID</p>
              <p class="text-dark">{{ category.id }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Fecha de creación</p>
              <p class="text-dark">{{ formatDate(category.created_at) }}</p>
            </div>
          </div>
        </div>
      </BaseCard>
      <div class="flex gap-4">
        <BaseButton variant="outlined" text="Volver" @click="router.push('/inventory/categories')" />
        <BaseButton text="Editar" :to="'/inventory/categories/edit/' + category.id" />
      </div>
    </template>
  </section>
</template>
