<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import LogoutButton from '@/components/Auth/LogoutButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'

const store = useAuthStore()
</script>

<template>
	<section class="w-full min-h-screen flex flex-col gap-8 justify-start m-8 md:m-0 items-start">
		<article class="w-full">
			<p class="text-2xl font-semibold mb-8">
				Bienvenido,
				<span class="font-bold text-primary font-heading">{{ store.user?.first_name }}</span>
			</p>
			<div class="grid grid-cols-4 md:grid-cols-3 grid-rows-4 md:grid-rows-4 gap-4 md:gap-4">
				<BaseCard
					class="col-start-1 row-start-1 col-span-4 row-span-2 md:col-start-1 md:row-start-1 md:col-span-2 md:row-span-3"
				>
					<div class="flex flex-col md:flex-row justify-between items-start gap-8">
						<div>
							<h2 class="text-white/50 font-semibold text-sm uppercase tracking-widest mb-4">
								Ventas de hoy
							</h2>
							<div class="flex flex-col gap-2 mb-4">
								<p class="text-6xl font-heading font-extrabold text-white tracking-tighter">$ 12.000,00</p>
								<small class="text-xl text-secondary">Bs 258.000,00</small>
							</div>
						</div>
						<div class="bg-secondary text-white px-8 py-4 rounded-xl">
							<h3 class="text-[10px] font-bold uppercase tracking-wider mb-1 opacity-70">
								Tasa de cambio:
							</h3>
							<p class="font-heading font-black text-xl">1 USD = 500 Bs</p>
						</div>
					</div>
				</BaseCard>
				<BaseCard
					variant="outlined"
					class="col-start-1 row-start-3 col-span-4 md:col-start-3 md:row-start-1 md:col-span-1 md:row-span-2"
				>
					1
				</BaseCard>
				<BaseCard
					variant="outlined"
					class="col-start-1 row-start-5 col-span-2 md:col-start-3 md:row-start-3 md:col-span-1 md:row-span-2"
				>
					2
				</BaseCard>
				<BaseCard
					variant="secondary"
					class="col-start-1 row-start-4 col-span-4 md:col-start-2 md:row-start-4 md:col-span-1 md:row-span-1"
				>
					3
				</BaseCard>
				<BaseCard
					variant="secondary"
					class="col-start-3 row-start-5 col-span-2 md:col-start-1 md:row-start-4 md:col-span-1 md:row-span-1"
				>
					4
				</BaseCard>
			</div>
			<LogoutButton />
		</article>
		<article class="grid grid-cols-2 lg:grid-cols-4 w-full gap-8">
			<BaseCard variant="outlined">
				<div class="flex flex-col justify-start items-start">
					<div class="mb-4">
						<i class="fa-solid fa-calculator text-[3rem]"></i>
					</div>
					<div class="">
						<h2 class="font-semibold text-md uppercase tracking-widest mb-2">POS</h2>
						<p class="">Vende y cobra rápido</p>
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined">
				<div class="flex flex-col justify-start items-start">
					<div class="mb-4">
						<i class="fa-solid fa-boxes-stacked text-[3rem]"></i>
					</div>
					<div class="">
						<h2 class="font-semibold text-md uppercase tracking-widest mb-2">Inventario</h2>
						<p class="">Maneja tu inventario</p>
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined">
				<div class="flex flex-col justify-start items-start">
					<div class="mb-4">
						<i class="fa-solid fa-tags text-[3rem]"></i>
					</div>
					<div class="">
						<h2 class="font-semibold text-md uppercase tracking-widest mb-2">Ventas</h2>
						<p class="">Ventas e historial de ventas</p>
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined">
				<div class="flex flex-col justify-start items-start">
					<div class="mb-4">
						<i class="fa-solid fa-users text-[3rem]"></i>
					</div>
					<div class="">
						<h2 class="font-semibold text-md uppercase tracking-widest mb-2">Clientes</h2>
						<p class="">Maneja a todos tus clientes</p>
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined">
				<div class="flex flex-col justify-start items-start">
					<div class="mb-4">
						<i class="fa-solid fa-wallet text-[3rem]"></i>
					</div>
					<div class="">
						<h2 class="font-semibold text-md uppercase tracking-widest mb-2">Finanzas</h2>
						<p class="">Gastos y flujo de caja</p>
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined">
				<div class="flex flex-col justify-start items-start">
					<div class="mb-4">
						<i class="fa-regular fa-file text-[3rem]"></i>
					</div>
					<div class="">
						<h2 class="font-semibold text-md uppercase tracking-widest mb-2">Reportes</h2>
						<p class="">Reportes de analíticas, y gráficos del negocio</p>
					</div>
				</div>
			</BaseCard>
		</article>
	</section>
</template>
