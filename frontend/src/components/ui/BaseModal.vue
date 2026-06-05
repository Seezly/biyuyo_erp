<script setup lang="ts">
import { ref, watch, nextTick, onUnmounted } from 'vue'
import BaseButton from './BaseButton.vue'

const props = defineProps<{
	visible: boolean
	title: string
	message?: string
	confirmText?: string
	cancelText?: string
	variant?: 'default' | 'danger'
	size?: 'sm' | 'md' | 'lg'
}>()

const emit = defineEmits(['close', 'confirm'])

const modalRef = ref<HTMLElement | null>(null)
const previousFocus = ref<HTMLElement | null>(null)
const titleId = `modal-title-${Math.random().toString(36).slice(2, 9)}`
const messageId = `modal-message-${Math.random().toString(36).slice(2, 9)}`

const handleClose = () => {
	emit('close')
}

const handleConfirm = () => {
	emit('confirm')
}

const handleKeydown = (e: KeyboardEvent) => {
	if (e.key === 'Escape') {
		handleClose()
		return
	}
	if (e.key === 'Tab' && modalRef.value) {
		const focusable = modalRef.value.querySelectorAll<HTMLElement>(
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
		const firstButton = modalRef.value?.querySelector<HTMLElement>('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')
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

const sizeClasses = {
	sm: 'max-w-sm',
	md: 'max-w-md',
	lg: 'max-w-lg',
}
</script>

<template>
	<Teleport to="body">
		<div
			v-if="visible"
			class="fixed inset-0 z-[9999] flex items-center justify-center p-4"
		>
			<div class="absolute inset-0 bg-black/50" @click="handleClose" aria-hidden="true"></div>

			<div
				ref="modalRef"
				role="dialog"
				aria-modal="true"
				:aria-labelledby="titleId"
				:aria-describedby="message ? messageId : undefined"
				:class="['relative bg-white rounded-xl shadow-xl w-full p-6', sizeClasses[size || 'md']]"
			>
				<button
					class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
					aria-label="Cerrar"
					@click="handleClose"
				>
					<i class="fa-solid fa-xmark text-xl" aria-hidden="true"></i>
				</button>

				<h3 :id="titleId" class="text-xl font-bold text-gray-800 mb-2">{{ title }}</h3>

				<p v-if="message" :id="messageId" class="text-gray-600 mb-6">{{ message }}</p>

				<div class="flex justify-end gap-3">
					<BaseButton
						:text="cancelText || 'Cancelar'"
						variant="outlined"
						@click="handleClose"
						width="auto"
					/>
					<BaseButton
						:text="confirmText || 'Confirmar'"
						:variant="variant === 'danger' ? 'danger' : 'primary'"
						@click="handleConfirm"
						width="auto"
					/>
				</div>
			</div>
		</div>
	</Teleport>
</template>