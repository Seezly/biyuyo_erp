<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import BaseCard from '@/components/ui/BaseCard.vue'

const router = useRouter()
const route = useRoute()
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Editar pago</h1>
			<p>Actualiza la información del pago</p>
		</div>
		<BaseCard variant="outlined" class="w-full">
			<p class="text-gray-500">Formulario de edición de pago en desarrollo.</p>
			<button class="text-primary underline mt-4" @click="router.push('/sales/payments')">Volver a pagos</button>
		</BaseCard>
	</section>
</template>
