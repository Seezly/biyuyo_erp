<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import LogoutButton from '@/components/Auth/LogoutButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'

const store = useAuthStore()
</script>

<template>
	<section class="flex flex-col gap-4 justify-center items-center">
		<div class="bg-white p-10 rounded-[3rem] relative overflow-hidden">
			<div class="flex justify-between items-start mb-8">
				<div>
					<h2
						class="text-on-surface-variant font-headline font-semibold text-sm uppercase tracking-widest mb-2"
					>
						Today's Sales
					</h2>
					<div class="flex flex-col gap-1">
						<span class="text-6xl font-headline font-extrabold text-on-surface tracking-tighter"
							>$1,284.50</span
						>
						<div class="flex items-center gap-2 text-tertiary font-headline font-bold text-2xl mt-2">
							<span class="material-symbols-outlined text-lg" data-icon="currency_exchange"
								>currency_exchange</span
							>
							<span>46,242.00 VES</span>
						</div>
					</div>
				</div>
				<div class="bg-primary-fixed text-on-primary-fixed px-6 py-3 rounded-xl">
					<p class="text-[10px] font-bold uppercase tracking-wider mb-1 opacity-70">Exchange Rate</p>
					<p class="font-headline font-black text-xl">1 USD = 36 VES</p>
				</div>
			</div>
			<div class="grid grid-cols-3 gap-6 pt-8 border-t-2 border-surface-container">
				<div class="flex flex-col">
					<span class="text-on-surface-variant text-sm font-medium mb-1">Orders</span>
					<span class="text-2xl font-headline font-bold">42</span>
				</div>
				<div class="flex flex-col">
					<span class="text-on-surface-variant text-sm font-medium mb-1">Items Sold</span>
					<span class="text-2xl font-headline font-bold">156</span>
				</div>
				<div class="flex flex-col">
					<span class="text-on-surface-variant text-sm font-medium mb-1">Avg. Ticket</span>
					<span class="text-2xl font-headline font-bold">$30.58</span>
				</div>
			</div>
			<!-- Decorative Background element -->
			<div
				class="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 bg-secondary-fixed/20 rounded-full blur-3xl -z-10"
			></div>
		</div>

		<BaseCard>
			<h2 class="text-xl text-white/50 font-thin mb-4">Ventas de hoy</h2>
			<div class="mb-4">
				<p class="text-3xl font-bold text-white">$ 12.000,00</p>
				<small class="text-xl text-secondary">Bs 258.000,00</small>
			</div>
			<div class="w-1/2 bg-secondary rounded-xl p-4 text-sm">
				<h3 class="text-white">Tasa de cambio:</h3>
				<p class="text-white">1 USD = 500 Bs</p>
			</div>
		</BaseCard>
		<h1>Dashboard</h1>
		<p>User first name: {{ store.user?.first_name }}</p>
		<section>
			<BaseCard> </BaseCard>
		</section>
		<LogoutButton />
	</section>
</template>
