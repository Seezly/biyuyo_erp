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

const buttonClasses = computed(() => [
  colors[props.variant || 'primary'],
  widths[props.width || 'full'],
  'py-2 px-4 rounded-full cursor-pointer',
])

const types = props.type || 'button'

function onClick() {
  emit('click')
}
</script>

<template>
  <RouterLink v-if="to" :to="to" :class="widths[props.width || 'full']">
    <button :type="types" :class="buttonClasses" @click="onClick">
      {{ text }}
      <i :class="icon"></i>
    </button>
  </RouterLink>
  <button v-else :type="types" :class="buttonClasses" @click="onClick">
    {{ text }}
    <i :class="icon"></i>
  </button>
</template>
