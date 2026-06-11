<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useBusinessesStore } from '@/stores/businesses'
import BaseButton from '@/components/ui/BaseButton.vue'

const auth = useAuthStore()
const businessesStore = useBusinessesStore()

const isAdmin = auth.user?.role === 'admin' || auth.user?.is_superuser

onMounted(async () => {
  if (isAdmin && businessesStore.businesses.length === 0) {
    await businessesStore.fetchBusinesses()
  }
})

function selectBusiness(id: number, name: string) {
  auth.startImpersonation(id, name)
}

function backToAdmin() {
  auth.stopImpersonation()
}
</script>

<template>
  <div
    v-if="isAdmin"
    class="w-full bg-gray-50 border-b border-gray-200"
  >
    <div class="max-w-7xl mx-auto px-4 py-2 flex items-center gap-4">
      <!-- Impersonating: show current business + back button -->
      <template v-if="auth.isImpersonating">
        <span class="text-sm text-gray-500">Negocio actual:</span>
        <span class="text-sm font-semibold text-primary">{{ auth.impersonatedBusinessName }}</span>
        <BaseButton
          text="Volver a administración"
          variant="outlined"
          width="auto"
          @click="backToAdmin"
        />
      </template>

      <!-- Not impersonating: show business list -->
      <template v-else>
        <span class="text-sm text-gray-500">Seleccionar negocio:</span>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="business in businessesStore.businesses"
            :key="business.id"
            class="text-sm px-3 py-1 rounded-full border border-gray-300 hover:border-primary hover:text-primary transition-colors cursor-pointer"
            @click="selectBusiness(business.id, business.name)"
          >
            {{ business.name }}
          </button>
          <span v-if="businessesStore.businesses.length === 0" class="text-sm text-gray-400">
            No hay negocios disponibles
          </span>
        </div>
      </template>
    </div>
  </div>
</template>
