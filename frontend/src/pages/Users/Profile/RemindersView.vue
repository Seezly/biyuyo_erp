<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToastStore } from '@/stores/toast'
import { apiFetch } from '@/utils/helpers'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCheckbox from '@/components/ui/BaseCheckbox.vue'

const toastStore = useToastStore()
const loading = ref(true)
const saving = ref(false)

const reminderSettings = ref({
  whatsapp_enabled: false,
  preventive_enabled: false,
  due_date_enabled: false,
  overdue_enabled: false,
  message_template: 'Hola [nombre], te recordamos que tienes un pago pendiente de [monto] con fecha próxima a vencer el día [fecha]. Por favor, puedes realizar el pago por cualquier medio que manejemos. ¡Gracias por tu atención!',
})

onMounted(async () => {
  try {
    const response = await apiFetch('/api/reminder-settings/current/')
    if (response.ok) {
      const data = await response.json()
      reminderSettings.value = {
        whatsapp_enabled: data.whatsapp_enabled ?? false,
        preventive_enabled: data.preventive_enabled ?? false,
        due_date_enabled: data.due_date_enabled ?? false,
        overdue_enabled: data.overdue_enabled ?? false,
        message_template: data.message_template ?? reminderSettings.value.message_template,
      }
    }
  } catch (error) {
    console.error('Error loading reminder settings:', error)
  } finally {
    loading.value = false
  }
})

const saveReminderSettings = async () => {
  saving.value = true
  try {
    const response = await apiFetch('/api/reminder-settings/current/', {
      method: 'PATCH',
      body: JSON.stringify(reminderSettings.value),
    })
    if (response.ok) {
      toastStore.success('Configuración guardada correctamente')
    } else {
      toastStore.error('Error al guardar configuración')
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
      <h1 class="text-primary text-2xl font-bold">Recordatorios</h1>
      <p>Personaliza cómo y cuándo tus clientes reciben recordatorios sobre sus pagos pendientes.</p>
    </div>

    <div v-if="loading" class="w-full text-center py-8">
      <p>Cargando configuración...</p>
    </div>
    <template v-else>
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
          <BaseCard variant="outlined" class="flex-1">
            <div class="flex flex-col gap-4">
              <h2 class="text-lg font-semibold text-dark">Plantilla del mensaje</h2>
              <div class="flex flex-col lg:flex-row justify-between items-start gap-4">
                <textarea
                  v-model="reminderSettings.message_template"
                  name="messageTemplate"
                  class="w-full lg:w-2/3 h-48 lg:h-32 py-2 px-4 rounded border border-secondary text-dark"
                ></textarea>
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
      </div>
      <div class="flex gap-4 w-full">
        <BaseButton 
          :text="saving ? 'Guardando...' : 'Guardar cambios'" 
          :loading="saving"
          :disabled="saving"
          @click="saveReminderSettings"
        />
      </div>
    </template>
  </section>
</template>
