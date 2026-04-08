<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
	variant?: 'primary' | 'secondary' | 'outlined' | 'inverted'
}>()

const colors = {
	primary: 'bg-primary',
	secondary: 'bg-secondary',
	outlined: 'border border-secondary',
	inverted: 'bg-dark text-white',
}

const cardClasses = computed(() => [
	colors[props.variant || 'primary'],
	'rounded-2xl bg-primary w-sm px-6 py-4 shadow-sm',
])
</script>

<template>
	<div :class="cardClasses">
		<slot />
	</div>
</template>
