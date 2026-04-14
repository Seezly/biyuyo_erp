<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
	variant?: 'primary' | 'secondary' | 'outlined' | 'inverted'
}>()

const colors = {
	primary: 'bg-primary',
	secondary: 'bg-secondary',
	outlined: 'border border-secondary bg-[#fff]',
	inverted: 'bg-dark text-white',
}

const cardClasses = computed(() => [colors[props.variant || 'primary'], 'rounded-xl p-8 shadow-sm'])
</script>

<template>
	<div :class="cardClasses">
		<slot />
	</div>
</template>
