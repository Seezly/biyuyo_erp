<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
</script>

<template>
	<section class="w-full min-h-screen flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Historial de ventas</h1>
			<p>Consulta y gestiona el historial de ventas</p>
		</div>
		<div class="grid lg:grid-cols-4 lg:grid-rows-2 w-full gap-8">
			<BaseCard class="flex-1 hover:shadow-lg transition-shadow lg:col-span-3 lg:row-span-2">
				<div class="flex flex-col md:flex-row justify-between items-start gap-8">
					<div>
						<h2 class="text-white/50 font-semibold text-sm uppercase tracking-widest mb-4">
							Ventas totales de hoy
						</h2>
						<div class="flex flex-col gap-2 mb-4">
							<p class="text-6xl font-heading font-extrabold text-white tracking-tighter">$ 12.000,00</p>
							<small class="text-xl text-secondary">Bs 258.000,00</small>
						</div>
					</div>
				</div>
			</BaseCard>
			<BaseCard
				variant="secondary"
				class="flex-1 hover:shadow-lg transition-shadow lg:col-span-1 lg:row-span-2"
			>
				<div
					class="flex flex-col md:flex-row justify-center lg:justify-start lg:items-end gap-8 h-full"
				>
					<div class="flex flex-col gap-2">
						<p class="text-6xl font-heading font-extrabold text-white tracking-tighter">45</p>
						<small class="text-xl text-dark">Ventas</small>
					</div>
				</div>
			</BaseCard>
		</div>
		<div class="flex flex-col gap-4 w-full col-span-1 row-span-4">
			<div class="flex justify-between items-center">
				<h2 class="text-primary text-lg font-semibold">Actividad reciente</h2>
			</div>
			<BaseCard variant="outlined" class="hover:shadow-lg transition-shadow cursor-pointer">
				<div class="flex flex-row justify-start items-center gap-8 w-full">
					<div class="size-12 bg-primary rounded-full"></div>
					<div>
						<div>
							<h3 class="text-lg font-bold">Venta al detal</h3>
							<p>14/04/2026</p>
							<p>07:44 pm</p>
						</div>
					</div>
					<div class="ml-auto text-right">
						<p class="text-xl font-semibold">$450,00</p>
						<p class="text-sm">Bs. 16.000,00</p>
					</div>
				</div>
			</BaseCard>
		</div>
		<div
			class="fixed bottom-8 right-8 size-16 rounded-full shadow-lg hover:shadow-xl bg-primary flex justify-center items-center cursor-pointer hover:bg-secondary transition"
		>
			<span class="text-white">+</span>
		</div>
	</section>
</template>
