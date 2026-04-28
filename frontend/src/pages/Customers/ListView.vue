<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Clientes</h1>
			<p>Administra a todos tus clientes desde un solo lugar</p>
		</div>
		<div class="w-full grid lg:grid-cols-12 gap-8">
			<BaseCard variant="outlined" class="col-span-12 lg:col-span-4 lg:row-col-1">
				<div class="flex flex-col gap-4">
					<div class="flex justify-between items-center">
						<div class="size-10 flex justify-center items-center bg-primary rounded-full">
							<i class="fa-solid fa-dollar-sign text-lg text-white"></i>
						</div>
						<h2 class="text-2xl font-bold text-primary">Clientes totales</h2>
					</div>
					<div>
						<h3 class="font-medium text-4xl text-primary">420</h3>
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined" class="col-span-12 lg:col-span-4 lg:row-col-1">
				<div class="flex flex-col gap-4">
					<div class="flex justify-between items-center">
						<div class="size-10 flex justify-center items-center bg-primary rounded-full">
							<i class="fa-solid fa-dollar-sign text-lg text-white"></i>
						</div>
						<h2 class="text-2xl font-bold text-primary">Clientes este mes</h2>
					</div>
					<div class="flex justify-between">
						<div>
							<h3 class="font-medium text-4xl text-primary">+420</h3>
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
								<span class="font-medium"> 7.81% </span>
								<span class="text-gray-500"> VS el mes anterior </span>
							</p>
						</div>
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined" class="col-span-12 lg:col-span-4 lg:row-col-1">
				<div class="flex flex-col gap-4">
					<div class="flex justify-between items-center">
						<div class="size-10 flex justify-center items-center bg-primary rounded-full">
							<i class="fa-solid fa-dollar-sign text-lg text-white"></i>
						</div>
						<h2 class="text-2xl font-bold text-primary">Clientes con deudas</h2>
					</div>
					<div class="flex justify-between">
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
								<span class="font-medium"> 6.81% </span>
								<span class="text-gray-500"> VS el mes anterior </span>
							</p>
						</div>
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined" class="col-span-12 lg:row-span-5 overflow-x-auto">
				<table class="min-w-full divide-y-2 divide-gray-200">
					<thead class="ltr:text-left rtl:text-right">
						<tr class="*:font-medium *:text-gray-900">
							<th class="px-4 py-2 whitespace-nowrap">Nombre</th>
							<th class="px-4 py-2 whitespace-nowrap">Desde</th>
							<th class="px-4 py-2 whitespace-nowrap">Deuda</th>
							<th class="px-4 py-2 whitespace-nowrap text-right">Acciones</th>
						</tr>
					</thead>

					<tbody class="divide-y divide-gray-200 *:even:bg-gray-50">
						<tr class="*:text-gray-900 *:first:font-medium">
							<td class="px-4 py-2 whitespace-nowrap">Sergio Gutierrez</td>
							<td class="px-4 py-2 whitespace-nowrap">22/04/2026</td>
							<td class="px-4 py-2 whitespace-nowrap">$0</td>
							<td class="px-4 py-2 whitespace-nowrap flex justify-end items-center gap-4">
								<BaseButton text="Pagar deuda" variant="outlined" width="auto" />
								<BaseButton text="Editar" variant="secondary" width="auto" />
								<BaseButton text="Eliminar" width="auto" />
							</td>
						</tr>
					</tbody>
				</table>
			</BaseCard>
		</div>
	</section>
</template>
