<script setup lang="ts">
import { RouterLink } from 'vue-router'

import BaseNav from '@/components/ui/BaseNav.vue'
import NavItem from '@/components/ui/NavItem.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import LogoutButton from '../Auth/LogoutButton.vue'
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
				<RouterLink class="rounded-full py-2 px-4" to="/">Inicio</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/about">Nosotros</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/benefits">Beneficios</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/plans">Planes</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/contact">Contáctanos</RouterLink>
			</NavItem>
			<NavItem v-if="auth.isAuthenticated" class="hidden md:flex">
				<RouterLink class="rounded-full py-2 px-4" to="/dashboard">Inicio</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/customers">Clientes</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/inventory">Inventario</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/sales">Ventas</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/sales/pos">POS</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/suppliers">Proveedores</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/reports">Reportes</RouterLink>
			</NavItem>
			<NavItem class="ml-auto">
				<div v-if="!auth.isAuthenticated" class="hidden md:flex justify-center items-center gap-4">
					<BaseButton to="/login" text="Iniciar sesión" width="auto" />
					<BaseButton to="/register" text="Registrarse" variant="ghost" width="auto" />
				</div>
				<div v-if="auth.isAuthenticated" class="hidden md:flex justify-center items-center gap-4">
					<i class="fa-regular fa-user text-2xl"></i>
					<BaseButton to="/profile" text="Perfil" variant="outlined" width="auto" />
					<LogoutButton />
				</div>
			</NavItem>
		</BaseNav>
	</header>
</template>
