<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
const store = useAuthStore()
</script>

<template>
	<h1>Dashboard</h1>
	<p>User first name: {{ store.user?.first_name }}</p>
</template>
