<script setup lang="ts">
import { RouterLink } from 'vue-router'

import BaseNav from '@/components/ui/BaseNav.vue'
import NavItem from '@/components/ui/NavItem.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<template>
	<header
		class="w-full bg-[#fff] md:max-w-7xl mx-auto md:rounded-full sticky top-0 md:mt-8 md:top-8 shadow-sm md:shadow-md px-8 py-4 z-100"
	>
		<BaseNav>
			<NavItem>
				<i class="md:hidden! fa-solid fa-bars text-2xl"></i>
				<h1>Biyuyo</h1>
			</NavItem>
			<NavItem v-if="!auth.isAuthenticated" class="hidden md:flex">
				<RouterLink to="/">Inicio</RouterLink>
				<RouterLink to="/about">Nosotros</RouterLink>
				<RouterLink to="/benefits">Beneficios</RouterLink>
				<RouterLink to="/plans">Planes</RouterLink>
				<RouterLink to="/contact">Contáctanos</RouterLink>
			</NavItem>
			<NavItem class="ml-auto">
				<div v-if="!auth.isAuthenticated" class="hidden md:flex justify-center items-center gap-4">
					<BaseButton to="/login" text="Iniciar sesión" width="auto" />
					<BaseButton to="/register" text="Registrarse" variant="outlined" width="auto" />
				</div>
				<i v-else class="fa-regular fa-user text-2xl"></i>
			</NavItem>
		</BaseNav>
	</header>
</template>
