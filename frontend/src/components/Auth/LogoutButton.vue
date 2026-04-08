<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue'

import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const auth = useAuthStore()

const handleLogout = async () => {
	await auth.logout()
	router.push('/logout')
}
</script>

<template>
	<BaseButton @click="handleLogout" text="Cerrar sesión" />
</template>
