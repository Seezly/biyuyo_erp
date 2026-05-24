<script setup lang="ts">
import TheHeader from './components/layout/TheHeader.vue'
import TheFooter from './components/layout/TheFooter.vue'
import Toast from './components/ui/Toast.vue'
import Breadcrumb from './components/Breadcrumb.vue'
</script>

<template>
	<Toast />
	<TheHeader />
	<main class="max-w-7xl flex-1 mx-auto w-full flex flex-col items-start justify-start gap-4">
		<Breadcrumb />
		<RouterView />
	</main>
	<TheFooter />
</template>

<style scoped></style>
