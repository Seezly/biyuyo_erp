<script setup lang="ts">
defineProps<{
	ariaLabel?: string
}>()
</script>

<template>
	<nav class="w-full flex justify-start items-center gap-8" :aria-label="ariaLabel">
		<slot />
	</nav>
</template>
