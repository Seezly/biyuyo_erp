<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Total de ventas</h1>
			<p>Consulta y gestiona las ventas de tu negocio</p>
		</div>
		<div class="w-full grid grid-cols-12 lg:grid-rows-6 gap-8">
			<div class="col-span-12 lg:col-span-3 lg:row-span-1">
				<BaseButton text="Añadir venta" to="/sales/pos" />
			</div>
			<div class="col-span-12 lg:col-span-6 lg:row-span-1">
				<BaseInput type="search" placeholder="Buscar por nombre" class="w-full" />
			</div>
			<div class="col-span-12 lg:col-span-3 lg:row-span-1">
				<BaseInput type="date" name="" class="w-full" />
			</div>
			<div class="col-span-12 lg:col-span-12 lg:row-span-5">
				<BaseCard variant="outlined">
					<h2 class="text-primary font-semibold text-xl mb-8">Últimas ventas</h2>
					<div class="flex flex-col gap-4 w-full">
						<div
							class="flex flex-col lg:flex-row lg:items-center w-full border-b border-secondary/10 pb-4 gap-8"
						>
							<div class="size-12 rounded-full hidden bg-primary lg:flex justify-center items-center">
								<i class="fa-solid fa-boxes-packing text-xl text-white"></i>
							</div>
							<div>
								<div class="flex gap-4 justify-between items-center">
									<h3 class="text-primary text-lg font-medium">Nombre del cliente</h3>
									<p class="text-xs">23/04/2026 09:35 AM</p>
								</div>
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
	</section>
</template>
