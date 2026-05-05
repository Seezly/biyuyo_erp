<script setup lang="ts">
import { ref } from 'vue'

import BaseButton from './BaseButton.vue'

const props = defineProps<{
	title: string
	subtitle?: string
	description: string
	variant: 'edit' | 'delete' | 'info'
	cancel?: boolean
	cta?: string
	visible: boolean
}>()

const emit = defineEmits(['update', 'close', 'next'])

const handleClose = () => {
	emit('update', false)
	emit('close')
}

const handleNext = () => {
	emit('next')
}
</script>

<template>
	<div
		v-if="$props.visible ?? false"
		class="w-full h-screen absolute top-0 left-0 flex justify-center items-center z-100"
	>
		<div
			class="w-md absolute flex flex-col justify-between items-start gap-4 rounded-xl px-8 py-4 bg-white border border-primary z-1"
		>
			<div class="border-b border-secondary pb-2 w-full">
				<h3 class="text-xl text-primary font-bold">{{ $props.title }}</h3>
				<p v-if="$props.subtitle" class="text-sm">{{ $props.subtitle }}</p>
			</div>
			<div class="border-b border-secondary pb-2 w-full">
				<p>{{ $props.description }}</p>
			</div>
			<div class="flex gap-4 justify-end items-center w-full">
				<BaseButton
					v-if="cancel"
					@click="handleClose"
					width="auto"
					text="Cancelar"
					variant="outlined"
				/>
				<BaseButton :text="cta ?? 'Ok'" @click="handleNext" width="auto" />
			</div>
		</div>
		<div class="absolute w-full h-full bg-dark/50" @click="handleClose"></div>
	</div>
</template>
