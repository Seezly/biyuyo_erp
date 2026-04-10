<script setup lang="ts">
import { ref } from 'vue'

import StepsItem from '@/components/StepsItem.vue'
import RegisterForm from '@/components/Auth/RegisterForm.vue'

const step = ref<number>(1)
</script>

<template>
	<section class="min-h-screen w-full flex flex-col items-center justify-center">
		<div class="mb-8">
			<h1 class="text-3xl text-center font-bold text-primary mb-4">Crear cuenta</h1>
			<p class="text-dark text-center">
				Rellena tus datos para crear una cuenta y empezar a utilizar Biyuyo ERP
			</p>
		</div>
		<StepsItem
			:step="step"
			:steps="[
				{ step: 1, label: 'Datos personales' },
				{ step: 2, label: 'Datos del negocio' },
			]"
		/>
		<RegisterForm :step="step" @incrementStep="step++" />
	</section>
</template>
