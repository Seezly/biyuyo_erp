<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useBusinessesStore } from '@/stores/businesses'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const authStore = useAuthStore()
const businessesStore = useBusinessesStore()

const business = ref<any>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    if (authStore.user?.business_id) {
      await businessesStore.fetchBusinesses()
      business.value = businessesStore.businesses.find(
        (b: any) => b.id === authStore.user?.business_id
      )
    }
  } catch (error) {
    console.error('Error loading profile:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Mi perfil</h1>
			<p>Maneja tu información personal y preferencias</p>
		</div>
		<div v-if="loading" class="w-full text-center py-8">
			<p>Cargando perfil...</p>
		</div>
		<div v-else class="w-full h-screen grid grid-cols-12 grid-rows-12 gap-8">
			<BaseCard
				variant="outlined"
				class="col-span-full w-full row-span-full lg:col-span-8 lg:row-span-8"
			>
				<div class="flex flex-col gap-4">
					<form class="flex justify-start items-start flex-col gap-4 w-full">
						<h2 class="text-xl text-primary font-bold">Información del negocio</h2>
						<div class="flex justify-between items-center gap-4 w-full">
							<label class="w-full flex flex-col text-dark">
								Nombre del negocio
								<BaseInput :model-value="business?.name || ''" name="business_name" disabled />
							</label>
							<label class="w-full flex flex-col text-dark">
								Correo electrónico
								<BaseInput :model-value="authStore.user?.email || ''" name="email" type="email" disabled />
							</label>
						</div>
						<label class="w-full flex flex-col text-dark">
							Teléfono
							<BaseInput :model-value="business?.phone || ''" name="phone" disabled />
						</label>
						<div class="flex justify-between items-center gap-4 w-full">
							<label class="w-full flex flex-col text-dark">
								Estado
								<BaseInput :model-value="business?.state || ''" name="state" disabled />
							</label>
							<label class="w-full flex flex-col text-dark">
								Municipio
								<BaseInput :model-value="business?.municipality || ''" name="municipality" disabled />
							</label>
						</div>
						<label class="w-full flex flex-col text-dark">
							Dirección
							<BaseInput :model-value="business?.address || ''" name="business_address" disabled />
						</label>
					</form>
				</div>
			</BaseCard>
			<BaseCard
				variant="outlined"
				class="col-span-full w-full row-span-full lg:col-span-4 lg:row-span-6"
			>
				<div class="flex flex-col gap-4">
					<h2 class="text-xl text-primary font-bold">Seguridad de la cuenta</h2>
					<BaseButton to="/profile/change-password" text="Cambiar contraseña" />
					<BaseButton to="/profile/notifications" text="Notificaciones" />
					<BaseButton to="/profile/reminders" text="Recordatorios" />
				</div>
			</BaseCard>
			<BaseCard class="col-span-full w-full row-span-full lg:col-span-4 lg:row-span-4">
				<div class="flex flex-col gap-4 justify-between h-full w-full">
					<div>
						<h2 class="text-2xl font-bold text-white mb-2">¿Necesitas ayuda?</h2>
						<p class="text-sm text-white">
							Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos.
						</p>
					</div>
				</div>
			</BaseCard>
		</div>
	</section>
</template>
