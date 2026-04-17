<script setup lang="ts">
import { ref, watch } from 'vue'

interface Step {
	step: number
	label: string
}

const props = defineProps<{
	step: number
	steps: Step[]
}>()

const step = ref<number>(props.step)

watch(
	() => props.step,
	(newStep) => {
		step.value = newStep
	},
)
</script>

<template>
	<div class="w-full">
		<h2 class="sr-only">Pasos</h2>

		<div
			class="relative after:absolute after:inset-x-0 after:top-1/2 after:block after:h-px after:-translate-y-1/2 after:rounded-lg after:bg-secondary"
		>
			<ol class="relative z-10 flex justify-between text-sm font-medium">
				<li
					v-for="stepItem in props.steps"
					:key="stepItem.step"
					class="flex items-center gap-2 p-2 bg-[#FFFFFF]"
				>
					<span
						:class="step >= stepItem.step ? 'bg-primary text-white' : 'bg-white text-primary'"
						class="size-6 rounded-full text-center text-[10px]/6 font-bold transition-colors duration-200"
					>
						{{ stepItem.step }}
					</span>

					<span class="hidden sm:block text-dark"> {{ stepItem.label }} </span>
				</li>
			</ol>
		</div>
	</div>
</template>
