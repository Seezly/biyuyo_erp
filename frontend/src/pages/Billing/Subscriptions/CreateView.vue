<script setup lang="ts">
import { useRouter } from 'vue-router'
import BaseCard from '@/components/ui/BaseCard.vue'

const router = useRouter()
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Crear suscripción</h1>
			<p>Asigna un plan de suscripción a un negocio</p>
		</div>
		<BaseCard variant="outlined" class="w-full">
			<p class="text-gray-500">Formulario de creación de suscripción en desarrollo.</p>
			<button class="text-primary underline mt-4" @click="router.push('/billing/subscriptions')">Volver a suscripciones</button>
		</BaseCard>
	</section>
</template>
