<template>
  <div class="text-center py-12">
    <div class="flex flex-col items-center gap-4">
      <i :class="`text-6xl text-gray-300 ${icon}`" aria-hidden="true"></i>
      <h3 class="text-xl font-semibold text-gray-600">{{ title }}</h3>
      <p class="text-gray-500 max-w-md">{{ description }}</p>
      <slot name="actions">
        <BaseButton
          v-if="actionText && actionLink"
          :to="actionLink"
          variant="primary"
          width="auto"
        >
          {{ actionText }}
        </BaseButton>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue'

defineProps<{
  icon: string
  title: string
  description: string
  actionText?: string
  actionLink?: string
}>()
</script>
