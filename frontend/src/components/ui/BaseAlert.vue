<script setup lang="ts">
import { ref, watch, nextTick, onUnmounted } from 'vue'

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

const alertRef = ref<HTMLElement | null>(null)
const previousFocus = ref<HTMLElement | null>(null)
const titleId = `alert-title-${Math.random().toString(36).slice(2, 9)}`
const descId = `alert-desc-${Math.random().toString(36).slice(2, 9)}`

const handleClose = () => {
	emit('update', false)
	emit('close')
}

const handleNext = () => {
	emit('next')
}

const handleKeydown = (e: KeyboardEvent) => {
	if (e.key === 'Escape') {
		handleClose()
		return
	}
	if (e.key === 'Tab' && alertRef.value) {
		const focusable = alertRef.value.querySelectorAll<HTMLElement>(
			'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
		)
		if (focusable.length === 0) return
		const first = focusable[0]
		const last = focusable[focusable.length - 1]
		if (!first || !last) return
		if (e.shiftKey) {
			if (document.activeElement === first) {
				e.preventDefault()
				last.focus()
			}
		} else {
			if (document.activeElement === last) {
				e.preventDefault()
				first.focus()
			}
		}
	}
}

watch(() => props.visible, async (val) => {
	if (val) {
		previousFocus.value = document.activeElement as HTMLElement
		await nextTick()
		const firstButton = alertRef.value?.querySelector<HTMLElement>('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')
		firstButton?.focus()
		document.addEventListener('keydown', handleKeydown)
	} else {
		document.removeEventListener('keydown', handleKeydown)
		previousFocus.value?.focus()
	}
})

onUnmounted(() => {
	document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
	<div
		v-if="$props.visible ?? false"
		class="w-full h-screen absolute top-0 left-0 flex justify-center items-center z-100"
	>
		<div
			ref="alertRef"
			role="alertdialog"
			aria-modal="true"
			:aria-labelledby="titleId"
			:aria-describedby="descId"
			class="w-md absolute flex flex-col justify-between items-start gap-4 rounded-xl px-8 py-4 bg-white border border-primary z-1"
		>
			<div class="border-b border-secondary pb-2 w-full">
				<h3 :id="titleId" class="text-xl text-primary font-bold">{{ $props.title }}</h3>
				<p v-if="$props.subtitle" class="text-sm">{{ $props.subtitle }}</p>
			</div>
			<div class="border-b border-secondary pb-2 w-full">
				<p :id="descId">{{ $props.description }}</p>
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
		<div class="absolute w-full h-full bg-dark/50" @click="handleClose" aria-hidden="true"></div>
	</div>
</template>
