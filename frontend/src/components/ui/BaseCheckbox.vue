<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
	text: string
	variant?: 'outlined' | 'filled'
	type?: 'checkbox' | 'button'
	name?: string
	modelValue?: boolean
}>()

const baseClasses = {
	checkbox: {
		input: 'p-2 border border-secondary text-primary rounded-full cursor-pointer',
		label: 'w-full flex gap-4 items-center text-dark',
	},
	button: {
		input: 'absolute opacity-0 cursor-pointer h-full w-full',
		label:
			'size-24 text-xs w-full has-checked:bg-primary has-checked:text-white has-checked:hover:bg-primary/90 rounded flex flex-col justify-center items-center text-center hover:bg-secondary/90 text-dark relative transition',
	},
}

const classes = computed(() => {
	const variant = props.variant || 'outlined'
	const type = props.type || 'checkbox'
	return {
		input: baseClasses[type].input,
		label:
			baseClasses[type].label +
			(variant === 'outlined' && type === 'button'
				? ' border border-secondary'
				: variant === 'outlined' && type === 'button'
					? ' bg-secondary'
					: ''),
	}
})

const emit = defineEmits<{
	(e: 'update:modelValue', value: boolean): void
}>()

const onCheck = (e: Event) => {
	const t = e.target as HTMLInputElement
	emit('update:modelValue', t.checked)
}
</script>

<template>
	<label :for="props.name" :class="classes.label">
		<input
			type="checkbox"
			:name="props.name"
			:checked="props.modelValue"
			@input="onCheck"
			:class="classes.input"
		/>
		{{ props.text }}
	</label>
</template>
