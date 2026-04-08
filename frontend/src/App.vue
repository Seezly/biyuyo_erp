<script setup lang="ts">
import TheHeader from './components/ui/TheHeader.vue'
</script>

<template>
	<TheHeader />
	<main class="max-w-7xl mt-8 flex-1 mx-auto w-full flex items-center justify-start">
		<RouterView />
	</main>
</template>

<style scoped></style>
