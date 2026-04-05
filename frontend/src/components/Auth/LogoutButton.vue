<script setup lang="ts">
import ButtonItem from '@/components/ui/ButtonItem.vue'

import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const auth = useAuthStore()

const handleLogout = async () => {
	await auth.logout()
	router.push('/logout')
}
</script>

<template>
	<ButtonItem @click="handleLogout" text="Cerrar sesión" />
</template>
