<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TheHeader from './components/layout/TheHeader.vue'
import TheBusinessBar from './components/layout/TheBusinessBar.vue'
import TheFooter from './components/layout/TheFooter.vue'
import Toast from './components/ui/Toast.vue'
import Breadcrumb from './components/Breadcrumb.vue'

const route = useRoute()
const isLanding = computed(() => route.name === 'Landing')
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
		:class="[
			'flex-1 w-full flex flex-col items-start justify-start gap-4',
			isLanding ? '' : 'max-w-7xl mx-auto',
		]"
	>
		<Breadcrumb v-if="!isLanding" />
		<RouterView />
	</main>
	<TheFooter />
</template>
