<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import LogoutButton from '@/components/Auth/LogoutButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'

const store = useAuthStore()
</script>

<template>
	<section class="w-full min-h-screen flex flex-col gap-8 justify-start items-start">
		<p class="text-2xl font-semibold">
			Bienvenido, <span class="font-bold text-primary font-heading">{{ store.user?.first_name }}</span>
		</p>
		<BaseCard>
			<div class="flex justify-between items-start gap-8">
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
					<h3 class="text-[10px] font-bold uppercase tracking-wider mb-1 opacity-70">Tasa de cambio:</h3>
					<p class="font-heading font-black text-xl">1 USD = 500 Bs</p>
				</div>
			</div>
		</BaseCard>
		<LogoutButton />
	</section>
</template>
