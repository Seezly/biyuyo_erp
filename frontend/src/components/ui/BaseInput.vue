<script setup lang="ts">
const props = defineProps<{
	type?: 'text' | 'email' | 'password' | 'number' | 'search' | 'tel' | 'month' | 'date'
	placeholder?: string
	name?: string
	modelValue?: string | number
}>()

const emit = defineEmits<{
	(e: 'update:modelValue', value: string | number): void
}>()

const onInput = (e: Event) => {
	const t = e.target as HTMLInputElement
	emit('update:modelValue', t.value)
}
</script>

<template>
	<input
		:type="props.type || 'text'"
		:name="props.name"
		:placeholder="props.placeholder"
		:value="props.modelValue"
		@input="onInput"
		class="py-2 px-4 rounded-xl border border-secondary text-primary"
	/>
</template>
