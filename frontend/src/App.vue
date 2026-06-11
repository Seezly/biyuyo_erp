<script setup lang="ts">
import TheHeader from './components/layout/TheHeader.vue'
import TheBusinessBar from './components/layout/TheBusinessBar.vue'
import TheFooter from './components/layout/TheFooter.vue'
import Toast from './components/ui/Toast.vue'
import Breadcrumb from './components/Breadcrumb.vue'
</script>

<template>
	<a
		href="#main-content"
		class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[10000] focus:bg-primary focus:text-white focus:px-4 focus:py-2 focus:rounded-lg focus:outline-none focus:ring-2 focus:ring-white"
	>
		Saltar al contenido principal
	</a>
	<Toast />
	<TheHeader />
	<TheBusinessBar />
	<main
		id="main-content"
		tabindex="-1"
		class="max-w-7xl flex-1 mx-auto w-full flex flex-col items-start justify-start gap-4"
	>
		<Breadcrumb />
		<RouterView />
	</main>
	<TheFooter />
</template>

<style scoped></style>
