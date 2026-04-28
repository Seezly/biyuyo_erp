<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Compras y gastos</h1>
			<p>Administra las compras de tu negocios y los gastos del día a día</p>
		</div>
		<div class="w-full grid grid-cols-12 lg:grid-rows-6 gap-8">
			<div class="col-span-12 lg:col-span-3 lg:row-span-1">
				<BaseButton text="Añadir compra o gasto" to="/suppliers/purchases/add" />
			</div>
			<div class="col-span-12 lg:col-span-6 lg:row-span-1">
				<BaseInput type="search" placeholder="Buscar por nombre o RIF" class="w-full" />
			</div>
			<div class="col-span-12 lg:col-span-3 lg:row-span-1">
				<BaseInput type="date" name="" id="" class="w-full" />
			</div>
			<div class="col-span-12 lg:col-span-12 lg:row-span-5">
				<BaseCard variant="outlined">
					<h2 class="text-primary font-semibold text-xl mb-8">Últimas transacciones</h2>
					<div class="flex flex-col gap-4 w-full">
						<div
							class="flex flex-col lg:flex-row lg:items-center w-full border-b border-secondary/10 pb-4 gap-8"
						>
							<div class="size-12 rounded-full hidden bg-primary lg:flex justify-center items-center">
								<i class="fa-solid fa-boxes-packing text-xl text-white"></i>
							</div>
							<div>
								<div class="flex gap-4 justify-between items-center">
									<h3 class="text-primary text-lg font-medium">Lugar de compra</h3>
									<p class="text-xs">23/04/2026</p>
								</div>
								<p>Producto, servicio o deuda</p>
							</div>
							<p class="text-primary text-2xl font-bold">-$20,00</p>
							<div class="flex gap-4 justify-center items-center lg:ml-auto">
								<BaseButton text="Editar" variant="outlined" class="w-full lg:w-auto" />
								<BaseButton text="Eliminar" class="w-full lg:w-auto" />
							</div>
						</div>
					</div>
				</BaseCard>
			</div>
		</div>
		<div class="flex w-full flex-col lg:flex-row justify-center items-center gap-8">
			<BaseCard variant="outlined" class="flex-1">
				<h2 class="text-primary font-semibold text-xl mb-8">Gastos</h2>
				<div class="flex gap-4 justify-between items-center">
					<div>
						<h3 class="font-medium text-4xl text-primary">+$10.000,00</h3>
					</div>
					<div class="flex justify-center items-center gap-2 text-red-600">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="size-8"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"
							></path>
						</svg>

						<p class="flex gap-2 text-xs">
							<span class="font-medium"> 67.81% </span>
							<span class="text-gray-500"> VS el mes anterior </span>
						</p>
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined" class="flex-1">
				<h2 class="text-primary font-semibold text-xl mb-8"># de transacciones</h2>
				<div class="flex gap-4 justify-between items-center">
					<div>
						<h3 class="font-medium text-4xl text-primary">+420</h3>
					</div>
					<div class="flex justify-center items-center gap-2 text-green-600">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="size-8"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
							></path>
						</svg>

						<p class="flex gap-2 text-xs">
							<span class="font-medium"> 67.81% </span>
							<span class="text-gray-500"> VS el mes anterior </span>
						</p>
					</div>
				</div>
			</BaseCard>
		</div>
	</section>
</template>
