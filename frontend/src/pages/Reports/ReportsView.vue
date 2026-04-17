<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Resumen financiero</h1>
			<p>La salud de tu negocio en una mirada</p>
		</div>
		<div class="grid grid-cols-12 gap-8 w-full">
			<BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="flex justify-between items-center">
						<div class="size-10 flex justify-center items-center bg-primary rounded-full">
							<i class="fa-solid fa-dollar-sign text-lg text-white"></i>
						</div>
						<h2 class="text-2xl font-bold text-primary">Total de efectivo (USD)</h2>
					</div>
					<div>
						<p class="text-2xl font-bold font-heading">$12.000,00</p>
						<p class="text-lg text-primary font-medium">Bs. 120.000,00</p>
					</div>
					<hr />
					<div>
						<p class="text-sm mb-2">Actualizado por última vez hace 12 minutos</p>
						<BaseButton text="Ver más" variant="outlined" />
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="flex justify-between items-center">
						<div class="size-10 flex justify-center items-center bg-primary rounded-full">
							<i class="fa-solid fa-money-bills text-lg text-white"></i>
						</div>
						<h2 class="text-2xl font-bold text-primary">Total de efectivo (Bs.)</h2>
					</div>
					<div>
						<p class="text-2xl font-bold font-heading">Bs. 120.000,00</p>
						<p class="text-lg text-primary font-medium">$12.000,00</p>
					</div>
					<hr />
					<div>
						<p class="text-sm mb-2">Actualizado por última vez hace 11 minutos</p>
						<BaseButton text="Ver más" variant="outlined" />
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined" class="col-span-12 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="flex justify-between items-center">
						<div class="size-10 flex justify-center items-center bg-primary rounded-full">
							<i class="fa-solid fa-building-columns text-lg text-white"></i>
						</div>
						<h2 class="text-2xl font-bold text-primary">Total en bancos</h2>
					</div>
					<div>
						<p class="text-2xl font-bold font-heading">$12.000,00</p>
						<p class="text-lg text-primary font-medium">Bs. 120.000,00</p>
					</div>
					<hr />
					<div>
						<p class="text-sm mb-2">Actualizado por última vez hace 25 minutos</p>
						<BaseButton text="Ver más" variant="outlined" />
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined" class="col-span-12 lg:col-span-8">
				<div class="flex flex-col gap-4">
					<div class="flex flex-col gap-2">
						<h2 class="text-2xl font-bold text-primary">Ventas / Gastos</h2>
						<p>Vista del rendimiento de la última semana</p>
					</div>
					<div>
						<p class="text-2xl font-bold font-heading">$12.000,00</p>
						<p class="text-lg text-primary font-medium">Bs. 120.000,00</p>
					</div>
					<hr />
					<div>
						<p class="text-sm mb-2">Actualizado por última vez hace 11 minutos</p>
						<BaseButton text="Ver más" variant="outlined" />
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="secondary" class="col-span-12 lg:col-span-4">
				<div class="flex flex-col gap-4 w-full h-full">
					<div class="flex flex-col gap-2">
						<h2 class="text-2xl font-bold text-white">Gastos recientes</h2>
					</div>
					<div class="flex flex-col justify-start items-start gap-2 w-full">
						<div
							class="flex justify-start items-center gap-2 w-full border border-primary bg-white py-2 px-4 rounded cursor-pointer"
						>
							<i class="fa-solid fa-receipt text-lg"></i>
							<div>
								<p class="font-medium">CORPOELEC</p>
								<p class="text-xs">Hace 2 horas</p>
							</div>
							<p class="font-bold text-lg ml-auto">-$200</p>
						</div>
					</div>
					<hr />
					<div class="mt-auto">
						<BaseButton text="Añadir nuevo gasto" />
					</div>
				</div>
			</BaseCard>
		</div>
	</section>
</template>
