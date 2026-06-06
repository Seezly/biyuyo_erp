<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToastStore } from '@/stores/toast'
import BaseCard from '@/components/ui/BaseCard.vue'

const router = useRouter()
const authStore = useAuthStore()
const toastStore = useToastStore()
const loggedOut = ref(false)

onMounted(async () => {
  try {
    await authStore.logout()
    loggedOut.value = true
    toastStore.success('Sesión cerrada correctamente')
    setTimeout(() => router.push('/login'), 2000)
  } catch {
    router.push('/login')
  }
})
</script>

<template>
  <section class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <BaseCard variant="outlined" class="w-full max-w-md text-center">
      <div class="flex flex-col items-center gap-6 py-8">
        <div class="rounded-full bg-primary size-20 flex justify-center items-center">
          <i class="fa-solid fa-right-from-bracket text-3xl text-white"></i>
        </div>
        <div v-if="!loggedOut">
          <h1 class="text-2xl font-bold text-primary mb-2">Cerrando sesión...</h1>
          <p class="text-gray-500">Por favor espera un momento.</p>
        </div>
        <div v-else>
          <h1 class="text-2xl font-bold text-primary mb-2">Sesión cerrada</h1>
          <p class="text-gray-500 mb-4">Has cerrado sesión correctamente.</p>
          <p class="text-sm text-gray-400">Redirigiendo al inicio de sesión...</p>
        </div>
      </div>
    </BaseCard>
  </section>
</template>
