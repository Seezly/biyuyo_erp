<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
	text: string
	variant?: 'primary' | 'secondary' | 'outlined' | 'inverted'
	type?: 'button' | 'submit' | 'reset'
	width?: 'full' | 'auto'
}>()

const colors = {
	primary: 'bg-primary text-white',
	secondary: 'bg-secondary text-primary',
	outlined: 'border border-secondary text-primary',
	inverted: 'bg-dark text-white',
}

const widths = {
	full: 'w-full',
	auto: 'w-auto',
}

const buttonClasses = computed(() => [
	colors[props.variant || 'primary'],
	widths[props.width || 'full'],
	'py-2 px-4 rounded-lg cursor-pointer',
])

const types = props.type || 'button'
</script>

<template>
	<button :type="types" :class="buttonClasses">
		{{ $props.text }}
	</button>
</template>
