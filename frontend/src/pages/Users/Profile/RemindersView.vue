<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { apiFetch } from '@/utils/helpers'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCheckbox from '@/components/ui/BaseCheckbox.vue'

const authStore = useAuthStore()
const userId = authStore.user?.id

// Form state for reminder settings
const reminderSettings = ref({
  whatsapp_enabled: false,
  email_enabled: false,
  sms_enabled: false,
  preventive_enabled: false,
  due_date_enabled: false,
  overdue_enabled: false,
  message_template: ''
})

// Original settings for reset
const originalSettings = ref({})

const loading = ref(false)
const error = ref<string | null>(null)
const success = ref<string | null>(null)

// Load current reminder settings from backend
const loadReminderSettings = async () => {
  if (!userId) return
  
  loading.value = true
  error.value = null
  success.value = null
  
  try {
    const response = await apiFetch(`/api/users/${userId}/reminder-settings/`)
    if (!response.ok) {
      // If endpoint doesn't exist, try to get from user profile
      const userResponse = await apiFetch(`/api/users/${userId}/`)
      if (!userResponse.ok) throw new Error('Failed to fetch user')
      const userData = await userResponse.json()
      // Assume reminder settings are stored in user object
      reminderSettings.value = {
        whatsapp_enabled: userData.whatsapp_enabled || false,
        email_enabled: userData.email_enabled || false,
        sms_enabled: userData.sms_enabled || false,
        preventive_enabled: userData.preventive_enabled || false,
        due_date_enabled: userData.due_date_enabled || false,
        overdue_enabled: userData.overdue_enabled || false,
        message_template: userData.message_template || ''
      }
    } else {
      const data = await response.json()
      reminderSettings.value = data
    }
    // Save original for reset
    originalSettings.value = { ...reminderSettings.value }
  } catch (e: any) {
    error.value = e.message || 'Failed to load reminder settings'
    console.error('Error loading reminder settings:', e)
  } finally {
    loading.value = false
  }
}

// Save reminder settings to backend
const saveReminderSettings = async () => {
  if (!userId) return
  
  loading.value = true
  error.value = null
  success.value = null
  
  try {
    const response = await apiFetch(`/api/users/${userId}/reminder-settings/`, {
      method: 'PUT',
      body: JSON.stringify(reminderSettings.value)
    })
    
    if (!response.ok) throw new Error('Failed to save reminder settings')
    
    success.value = 'Configuración guardada exitosamente'
    originalSettings.value = { ...reminderSettings.value }
    
    // Clear success message after 3 seconds
    setTimeout(() => {
      success.value = null
    }, 3000)
  } catch (e: any) {
    error.value = e.message || 'Failed to save reminder settings'
    console.error('Error saving reminder settings:', e)
  } finally {
    loading.value = false
  }
}

// Reset form to original settings
const resetReminderSettings = () => {
  reminderSettings.value = { ...originalSettings.value }
  error.value = null
  success.value = null
}

onMounted(() => {
  loadReminderSettings()
})
</script>

<template>
  <section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
    <div>
      <h1 class="text-primary text-2xl font-bold">Recordatorios</h1>
      <p>Personaliza cómo y cuándo tus clientes reciben recordatorios sobre sus pagos pendientes.</p>
    </div>
    
    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando configuración...</p>
    </div>
    
    <div v-else>
      <div class="text-sm text-dark mb-4" v-if="error">
        {{ error }}
      </div>
      <div class="text-sm text-green-600 mb-4" v-if="success">
        {{ success }}
      </div>

      <div class="flex flex-col gap-4 w-full">
        <div>
          <h2 class="text-primary text-lg font-semibold">Canales de envío</h2>
          <p class="text-sm text-dark">
            Selecciona los canales por los cuales deseas que tus clientes reciban recordatorios de pagos
            pendientes
          </p>
        </div>
        <div class="flex flex-col lg:flex-row gap-8 w-full">
          <BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
            <div class="flex justify-between items-center relative">
              <div>
                <h2 class="text-lg font-semibold text-dark">Recordatorios por WhatsApp</h2>
                <p class="text-sm text-dark">Mensajería instantánea directa.</p>
              </div>
              <div>
                <BaseCheckbox 
                  v-model="reminderSettings.whatsapp_enabled" 
                  text=""
                />
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
      <div class="flex flex-col gap-4 w-full">
        <div>
          <h2 class="text-primary text-lg font-semibold">Frecuencia de envío</h2>
          <p class="text-sm text-dark">
            Personaliza la frecuencia con la que tus clientes reciben recordatorios de pagos pendientes
            para mantenerlos informados y motivados a realizar sus pagos a tiempo.
          </p>
        </div>
        <div class="flex flex-col lg:flex-row gap-8 w-full">
          <BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
            <div class="flex relative justify-between items-center">
              <div>
                <h2 class="text-lg font-semibold text-dark">Recordatorio preventivo</h2>
                <p class="text-sm text-dark">Enviar 3 días antes de la fecha de vencimiento del pago.</p>
              </div>
              <div>
                <BaseCheckbox 
                  v-model="reminderSettings.preventive_enabled" 
                  text=""
                />
              </div>
            </div>
          </BaseCard>
          <BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
            <div class="flex relative justify-between items-center">
              <div>
                <h2 class="text-lg font-semibold text-dark">Recordatorio de vencimiento</h2>
                <p class="text-sm text-dark">Enviar el mismo día de la fecha de vencimiento del pago.</p>
              </div>
              <div>
                <BaseCheckbox 
                  v-model="reminderSettings.due_date_enabled" 
                  text=""
                />
              </div>
            </div>
          </BaseCard>
          <BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
            <div class="flex relative justify-between items-center">
              <div>
                <h2 class="text-lg font-semibold text-dark">Recordatorio de mora</h2>
                <p class="text-sm text-dark">
                  Enviar cada 7 días después de la fecha de vencimiento del pago.
                </p>
              </div>
              <div>
                <BaseCheckbox 
                  v-model="reminderSettings.overdue_enabled" 
                  text=""
                />
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
      <div class="flex flex-col gap-4 w-full">
        <div>
          <h2 class="text-primary text-lg font-semibold">Mensaje predefinido</h2>
          <p class="text-sm text-dark">
            Personaliza el mensaje que se enviará a tus clientes en cada recordatorio para mantener una
            comunicación clara
          </p>
        </div>
        <div class="flex flex-col lg:flex-row gap-8 w-full">
          <BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
            <div class="flex flex-col gap-4">
              <h2 class="text-lg font-semibold text-dark">Plantilla del mensaje</h2>
              <div class="flex flex-col lg:flex-row justify-between items-start gap-4">
                <textarea
                  v-model="reminderSettings.message_template"
                  name="messageTemplate"
                  class="w-full lg:w-2/3 h-48 lg:h-32 py-2 px-4 rounded border border-secondary text-dark"
                >
Hola [nombre], te recordamos que tienes un pago pendiente de [monto] con fecha próxima a vencer el día [fecha]. Por favor, puedes realizar el pago por cualquier medio que manejemos. ¡Gracias por tu atención!</textarea
                >
                <div class="flex-1 w-full flex flex-col items-center gap-4">
                  <p class="text-lg font-semibold">Variables utilizables</p>
                  <div class="flex gap-4">
                    <span
                      class="bg-secondary px-4 py-2 rounded-full hover:bg-primary text-white transition cursor-pointer"
                      >[nombre]</span
                    >
                    <span
                      class="bg-secondary px-4 py-2 rounded-full hover:bg-primary text-white transition cursor-pointer"
                      >[monto]</span
                    >
                    <span
                      class="bg-secondary px-4 py-2 rounded-full hover:bg-primary text-white transition cursor-pointer"
                      >[fecha]</span
                    >
                  </div>
                </div>
              </div>
              <p class="text-sm font-italic">
                Las etiquetas entre corchetes se reemplazarán automáticamente con los datos del cliente.
              </p>
            </div>
          </BaseCard>
        </div>
        <div class="flex flex-col lg:flex-row gap-8 w-full">
          <BaseCard variant="primary" class="flex-1 hover:shadow-lg transition-shadow">
            <div class="flex flex-col gap-4">
              <h2 class="text-lg font-semibold text-white">Vista previa del mensaje</h2>
              <div class="flex justify-between items-start bg-[#fff] rounded-lg p-8">
                <p>
                  Hola <span class="text-primary font-medium">José</span>, te recordamos que tienes un pago
                  pendiente de <span class="text-primary font-medium">$100</span> con fecha próxima a vencer
                  el día <span class="text-primary font-medium">15/04/2026</span>. Por favor, puedes realizar
                  el pago por cualquier medio que manejemos. ¡Gracias por tu atención!
                </p>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>
      <div class="flex gap-4 w-full">
        <BaseButton 
          text="Descartar cambios" 
          variant="outlined" 
          @click="resetReminderSettings"
        />
        <BaseButton 
          text="Guardar cambios" 
          @click="saveReminderSettings"
        />
      </div>
    </div>
  </section>
</template>
