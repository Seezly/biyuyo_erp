<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

interface ButtonProps {
  text?: string
  icon?: string
  variant?: 'primary' | 'secondary' | 'outlined' | 'inverted' | 'ghost' | 'danger'
  type?: 'button' | 'submit' | 'reset'
  width?: 'full' | 'auto'
  to?: string
  loading?: boolean
  disabled?: boolean
}

const props = defineProps<ButtonProps>()
const emit = defineEmits(['click'])

const colors = {
  primary: 'bg-primary text-white hover:bg-secondary transition duration-200',
  secondary: 'bg-secondary text-white hover:bg-primary transition duration-200',
  ghost:
    'text-primary hover:text-white hover:border hover:border-secondary hover:bg-secondary transition duration-200',
  outlined:
    'border border-secondary text-primary hover:bg-secondary hover:text-white transition duration-200',
  inverted: 'bg-dark text-white hover:bg-white hover:text-dark transition duration-200',
  danger: 'bg-red-500 text-white hover:bg-red-600 transition duration-200',
}

const widths = {
  full: 'w-full',
  auto: 'w-auto',
}

const isDisabled = computed(() => props.disabled || props.loading)

const buttonClasses = computed(() => [
  colors[props.variant || 'primary'],
  widths[props.width || 'full'],
  'py-2 px-4 rounded-full cursor-pointer',
  isDisabled.value ? 'opacity-60 cursor-not-allowed' : '',
])

const types = props.type || 'button'

function onClick() {
  if (!isDisabled.value) {
    emit('click')
  }
}
</script>

<template>
  <RouterLink v-if="to && !isDisabled" :to="to" :class="widths[props.width || 'full']">
    <button :type="types" :class="buttonClasses" :disabled="isDisabled" :aria-busy="loading || undefined">
      <svg v-if="loading" class="inline-block animate-spin mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
      </svg>
      {{ text }}
      <i v-if="!loading" :class="icon"></i>
    </button>
  </RouterLink>
  <button v-else :type="types" :class="buttonClasses" :disabled="isDisabled" :aria-busy="loading || undefined" @click="onClick">
    <svg v-if="loading" class="inline-block animate-spin mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
    </svg>
    {{ text }}
    <i v-if="!loading" :class="icon"></i>
  </button>
</template>
