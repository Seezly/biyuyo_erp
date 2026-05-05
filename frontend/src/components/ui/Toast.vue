<script setup lang="ts">
import { computed } from 'vue'
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()

const iconMap = {
	success: 'fa-check-circle',
	error: 'fa-circle-xmark',
	warning: 'fa-triangle-exclamation',
	info: 'fa-circle-info',
}

const colorMap = {
	success: 'bg-green-500',
	error: 'bg-red-500',
	warning: 'bg-yellow-500',
	info: 'bg-blue-500',
}
</script>

<template>
	<div class="fixed top-4 right-4 z-[9999] flex flex-col gap-2">
		<div
			v-for="toast in toastStore.toasts"
			:key="toast.id"
			class="flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg text-white min-w-[300px] max-w-md animate-slide-in"
			:class="colorMap[toast.type]"
		>
			<i :class="['fa-solid text-xl', iconMap[toast.type]]"></i>
			<p class="flex-1 text-sm font-medium">{{ toast.message }}</p>
			<button
				@click="toastStore.remove(toast.id)"
				class="opacity-70 hover:opacity-100 transition-opacity"
			>
				<i class="fa-solid fa-xmark"></i>
			</button>
		</div>
	</div>
</template>

<style scoped>
@keyframes slide-in {
	from {
		transform: translateX(100%);
		opacity: 0;
	}
	to {
		transform: translateX(0);
		opacity: 1;
	}
}

.animate-slide-in {
	animation: slide-in 0.3s ease-out;
}
</style>