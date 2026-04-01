<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
	text: string
	type?: 'primary' | 'secondary' | 'outlined' | 'inverted'
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
	colors[props.type || 'primary'],
	widths[props.width || 'full'],
	'py-2 px-4 rounded-lg cursor-pointer',
])
</script>

<template>
	<button :class="buttonClasses">
		{{ $props.text }}
	</button>
</template>
