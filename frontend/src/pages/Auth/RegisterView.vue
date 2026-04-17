<script setup lang="ts">
import RegisterForm from '@/components/Auth/RegisterForm.vue'
</script>

<template>
	<section class="px-8 w-full flex flex-col items-center justify-center">
		<div class="mb-8">
			<h1 class="text-3xl text-center font-bold text-primary mb-4">Crear cuenta</h1>
			<p class="text-dark text-center">
				Rellena tus datos para crear una cuenta y empezar a utilizar Biyuyo ERP
			</p>
		</div>

		<RegisterForm />
	</section>
</template>
