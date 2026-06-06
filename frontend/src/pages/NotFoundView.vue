<script setup lang="ts">
import { useRouter } from 'vue-router'
import BaseButton from '@/components/ui/BaseButton.vue'

const router = useRouter()
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-center items-center min-h-[60vh]">
		<div class="text-center">
			<h1 class="text-primary text-6xl font-bold mb-4">404</h1>
			<p class="text-xl text-gray-600 mb-2">Página no encontrada</p>
			<p class="text-gray-500">La página que buscas no existe o fue movida.</p>
		</div>
		<BaseButton text="Volver al inicio" @click="router.push('/')" />
	</section>
</template>
