<script setup lang="ts">
const props = defineProps<{
	type: 'text' | 'email' | 'password'
	placeholder?: string
	name: string
	value?: string | number
}>()
</script>

<template>
	<input
		:type="props.type"
		:name="props.name"
		:placeholder="props.placeholder"
		:value="props.value"
		class="py-2 px-4 rounded-lg border border-secondary text-primary"
	/>
</template>
