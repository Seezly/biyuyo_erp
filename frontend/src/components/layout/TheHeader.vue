<script setup lang="ts">
import { ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

import BaseNav from '@/components/ui/BaseNav.vue'
import NavItem from '@/components/ui/NavItem.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import LogoutButton from '../Auth/LogoutButton.vue'
import StockAlerts from '@/components/ui/StockAlerts.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const route = useRoute()
const mobileMenuOpen = ref(false)

watch(() => route.path, () => {
  mobileMenuOpen.value = false
})
</script>

<template>
	<header
		class="w-full bg-white md:max-w-7xl mx-auto md:rounded-full sticky top-0 md:mt-8 md:top-8 shadow-sm md:shadow-md px-8 py-4 z-100"
	>
		<BaseNav aria-label="Menú principal">
			<NavItem>
				<button
					class="md:hidden! p-2 rounded-lg hover:bg-gray-100 transition-colors"
					@click="mobileMenuOpen = !mobileMenuOpen"
					:aria-expanded="mobileMenuOpen"
					aria-controls="mobile-menu"
					aria-label="Abrir menú de navegación"
				>
					<i class="fa-solid fa-bars text-2xl" aria-hidden="true"></i>
				</button>
				<h1>Biyuyo</h1>
			</NavItem>
			<NavItem v-if="!auth.isAuthenticated" class="hidden md:flex">
				<RouterLink class="rounded-full py-2 px-4" to="/">Inicio</RouterLink>
			</NavItem>
			<NavItem v-if="auth.isAuthenticated && auth.user?.role !== 'admin'" class="hidden md:flex">
				<RouterLink class="rounded-full py-2 px-4" to="/dashboard">Inicio</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/customers">Clientes</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/inventory">Inventario</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/sales">Ventas</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/sales/pos">POS</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/suppliers">Proveedores</RouterLink>
				<RouterLink class="rounded-full py-2 px-4" to="/reports">Reportes</RouterLink>
			</NavItem>
            <NavItem v-if="auth.isAuthenticated && auth.user?.role === 'admin'" class="hidden md:flex">
                <RouterLink class="rounded-full py-2 px-4" to="/admin">Administración</RouterLink>
                <RouterLink class="rounded-full py-2 px-4" to="/users">Usuarios</RouterLink>
                <RouterLink class="rounded-full py-2 px-4" to="/admin/businesses">Negocios</RouterLink>
                <RouterLink class="rounded-full py-2 px-4" to="/audit">Auditoría</RouterLink>
                <RouterLink class="rounded-full py-2 px-4" to="/billing">Facturación</RouterLink>
            </NavItem>
			<NavItem class="ml-auto">
				<div v-if="!auth.isAuthenticated" class="hidden md:flex justify-center items-center gap-4">
					<BaseButton to="/login" text="Iniciar sesión" width="auto" />
					<BaseButton to="/register" text="Registrarse" variant="ghost" width="auto" />
				</div>
				<div v-if="auth.isAuthenticated" class="hidden md:flex justify-center items-center gap-4">
					<StockAlerts />
					<i class="fa-regular fa-user text-2xl" aria-hidden="true"></i>
					<BaseButton to="/profile" text="Perfil" variant="outlined" width="auto" />
					<LogoutButton />
				</div>
			</NavItem>
		</BaseNav>

		<!-- Mobile menu -->
		<div
			v-if="mobileMenuOpen"
			id="mobile-menu"
			class="md:hidden mt-4 pb-4 border-t border-gray-100"
			role="menu"
		>
			<div v-if="!auth.isAuthenticated" class="flex flex-col gap-2 pt-4">
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/" role="menuitem">Inicio</RouterLink>
				<div class="flex gap-2 pt-2">
					<BaseButton to="/login" text="Iniciar sesión" width="auto" />
					<BaseButton to="/register" text="Registrarse" variant="ghost" width="auto" />
				</div>
			</div>
			<div v-if="auth.isAuthenticated && auth.user?.role !== 'admin'" class="flex flex-col gap-2 pt-4">
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/dashboard" role="menuitem">Inicio</RouterLink>
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/customers" role="menuitem">Clientes</RouterLink>
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/inventory" role="menuitem">Inventario</RouterLink>
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/sales" role="menuitem">Ventas</RouterLink>
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/sales/pos" role="menuitem">POS</RouterLink>
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/suppliers" role="menuitem">Proveedores</RouterLink>
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/reports" role="menuitem">Reportes</RouterLink>
				<div class="flex gap-2 pt-2">
					<StockAlerts />
					<BaseButton to="/profile" text="Perfil" variant="outlined" width="auto" />
					<LogoutButton />
				</div>
			</div>
			<div v-if="auth.isAuthenticated && auth.user?.role === 'admin'" class="flex flex-col gap-2 pt-4">
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/admin" role="menuitem">Administración</RouterLink>
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/users" role="menuitem">Usuarios</RouterLink>
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/admin/businesses" role="menuitem">Negocios</RouterLink>
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/audit" role="menuitem">Auditoría</RouterLink>
				<RouterLink class="rounded-lg py-2 px-4 hover:bg-gray-100" to="/billing" role="menuitem">Facturación</RouterLink>
				<div class="flex gap-2 pt-2">
					<StockAlerts />
					<BaseButton to="/profile" text="Perfil" variant="outlined" width="auto" />
					<LogoutButton />
				</div>
			</div>
		</div>
	</header>
</template>
