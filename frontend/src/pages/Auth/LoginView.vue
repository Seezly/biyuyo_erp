<script setup lang="ts">
import LoginForm from '@/components/Auth/LoginForm.vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import { type User } from '@/types/Auth'

const auth = useAuthStore()
const router = useRouter()

function handleLogin(data: User) {
	auth.setUser(data)
	router.push({ path: '/dashboard' })
}
</script>

<template>
	<section class="w-full flex flex-col items-center justify-center">
		<div class="mb-8">
			<h1 class="text-3xl text-center font-bold text-primary mb-4">Iniciar sesión</h1>
			<p class="text-dark text-center">Rellena tus datos para iniciar sesión</p>
		</div>
		<LoginForm @submit="handleLogin" />
	</section>
</template>
