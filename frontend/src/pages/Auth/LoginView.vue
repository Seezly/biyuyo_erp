<script setup lang="ts">
import ButtonItem from '@/components/ui/ButtonItem.vue'
import InputItem from '@/components/ui/InputItem.vue'
</script>

<template>
	<section class="h-screen w-full flex flex-col items-center justify-center">
		<div class="mb-8">
			<h1 class="text-3xl text-center font-bold text-primary mb-4">Iniciar sesión</h1>
			<p class="text-dark text-center">Rellena tus datos para iniciar sesión</p>
		</div>
		<form action="" class="flex justify-start items-center flex-col gap-4 w-md">
			<label class="w-full flex flex-col text-dark">
				Correo electrónico
				<InputItem type="email" name="email" placeholder="Correo electrónico" />
			</label>
			<label class="w-full flex flex-col text-dark mb-8">
				<div class="flex justify-between items-center">
					Contraseña
					<a href="#" class="text-primary underline text-xs font-light">¿Olvidaste tu contraseña?</a>
				</div>
				<InputItem type="password" name="password" placeholder="Contraseña" />
			</label>
			<ButtonItem text="Iniciar sesión" />
			<ButtonItem text="Regístrate" type="outlined" />
		</form>
	</section>
</template>
