<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { apiFetch } from '@/utils/helpers'
import { useToastStore } from '@/stores/toast'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseCheckbox from '@/components/ui/BaseCheckbox.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const authStore = useAuthStore()
const toastStore = useToastStore()

const emailEnabled = ref(false)
const pushEnabled = ref(false)
const lowStockAlert = ref(false)
const outOfStockAlert = ref(false)
const loading = ref(true)
const saving = ref(false)

onMounted(async () => {
  try {
    const response = await apiFetch(`/api/users/${authStore.user?.id}/`)
    if (response.ok) {
      const data = await response.json()
      emailEnabled.value = data.email_notifications ?? false
      pushEnabled.value = data.push_notifications ?? false
      lowStockAlert.value = data.low_stock_alerts ?? false
      outOfStockAlert.value = data.out_of_stock_alerts ?? false
    }
  } catch (error) {
    console.error('Error loading notification preferences:', error)
  } finally {
    loading.value = false
  }
})

const savePreferences = async () => {
  saving.value = true
  try {
    const response = await apiFetch(`/api/users/${authStore.user?.id}/`, {
      method: 'PATCH',
      body: JSON.stringify({
        email_notifications: emailEnabled.value,
        push_notifications: pushEnabled.value,
        low_stock_alerts: lowStockAlert.value,
        out_of_stock_alerts: outOfStockAlert.value,
      }),
    })
    if (response.ok) {
      toastStore.success('Preferencias guardadas correctamente')
    } else {
      toastStore.error('Error al guardar preferencias')
    }
  } catch (error) {
    toastStore.error('Error de conexión')
  } finally {
    saving.value = false
  }
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Alertas y Notificaciones</h1>
			<p>Administra tus preferencias de notificaciones y alertas</p>
		</div>
		<div v-if="loading" class="w-full text-center py-8">
			<p>Cargando preferencias...</p>
		</div>
		<template v-else>
			<div class="flex flex-col gap-4 w-full">
				<div>
					<h2 class="text-primary text-lg font-semibold">Canales de notificación</h2>
					<p class="text-sm text-dark">
						Selecciona los canales por los cuales deseas recibir notificaciones y alertas importantes
					</p>
				</div>
				<div class="flex flex-col lg:flex-row gap-8 w-full">
					<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
						<div class="flex justify-between items-center relative">
							<div>
								<h2 class="text-lg font-semibold text-dark">Notificaciones por correo electrónico</h2>
								<p class="text-sm text-dark">
									Recibe actualizaciones y alertas importantes en tu correo electrónico.
								</p>
							</div>
							<div>
								<BaseCheckbox v-model="emailEnabled" text="" />
							</div>
						</div>
					</BaseCard>
					<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
						<div class="flex justify-between items-center relative">
							<div>
								<h2 class="text-lg font-semibold text-dark">Notificaciones Push</h2>
								<p class="text-sm text-dark">Recibe actualizaciones y alertas importantes en tu teléfono.</p>
							</div>
							<div>
								<BaseCheckbox v-model="pushEnabled" text="" />
							</div>
						</div>
					</BaseCard>
				</div>
			</div>
			<div class="flex flex-col gap-4 w-full">
				<div>
					<h2 class="text-primary text-lg font-semibold">Alertas de inventario</h2>
					<p class="text-sm text-dark">Seleccione cómo y cuándo desea recibir alertas de sus productos</p>
				</div>
				<div class="flex flex-col lg:flex-row gap-8 w-full">
					<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
						<div class="flex justify-between items-center relative">
							<div>
								<h2 class="text-lg font-semibold text-dark">Alertas de inventario bajo</h2>
								<p class="text-sm text-dark">
									Recibir alertas cuando el inventario esté por debajo del nivel mínimo.
								</p>
							</div>
							<div>
								<BaseCheckbox v-model="lowStockAlert" text="" />
							</div>
						</div>
					</BaseCard>
					<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
						<div class="flex justify-between items-center relative">
							<div>
								<h2 class="text-lg font-semibold text-dark">Alertas de producto agotado</h2>
								<p class="text-sm text-dark">Recibir alertas cuando un producto esté agotado.</p>
							</div>
							<div>
								<BaseCheckbox v-model="outOfStockAlert" text="" />
							</div>
						</div>
					</BaseCard>
				</div>
			</div>
			<div class="flex gap-4 w-full">
				<BaseButton
					:text="saving ? 'Guardando...' : 'Guardar preferencias'"
					:loading="saving"
					:disabled="saving"
					@click="savePreferences"
				/>
			</div>
		</template>
	</section>
</template>
