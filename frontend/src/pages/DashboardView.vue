<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import LogoutButton from '@/components/Auth/LogoutButton.vue'

const store = useAuthStore()
</script>

<template>
	<section class="flex flex-col gap-4 justify-center items-center">
		<h1>Dashboard</h1>
		<p>User first name: {{ store.user?.first_name }}</p>
		<LogoutButton />
	</section>
</template>
