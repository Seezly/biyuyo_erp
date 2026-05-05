<script setup lang="ts">
import BaseButton from './BaseButton.vue'

defineProps<{
	visible: boolean
	title: string
	message?: string
	confirmText?: string
	cancelText?: string
	variant?: 'default' | 'danger'
	size?: 'sm' | 'md' | 'lg'
}>()

const emit = defineEmits(['close', 'confirm'])

const handleClose = () => {
	emit('close')
}

const handleConfirm = () => {
	emit('confirm')
}

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
			<div class="absolute inset-0 bg-black/50" @click="handleClose"></div>

			<div
				:class="['relative bg-white rounded-xl shadow-xl w-full p-6', sizeClasses[size || 'md']]"
			>
				<button
					class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
					@click="handleClose"
				>
					<i class="fa-solid fa-xmark text-xl"></i>
				</button>

				<h3 class="text-xl font-bold text-gray-800 mb-2">{{ title }}</h3>

				<p v-if="message" class="text-gray-600 mb-6">{{ message }}</p>

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