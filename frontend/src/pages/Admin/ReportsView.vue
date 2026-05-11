<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Reportes Administrativos</h1>
			<p>Reportes globales del sistema</p>
		</div>

		<div class="grid grid-cols-12 gap-8 w-full">
			<BaseCard variant="outlined" class="col-span-12 md:col-span-6 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="size-10 flex justify-center items-center bg-primary rounded-full">
						<i class="fa-solid fa-chart-line text-lg text-white"></i>
					</div>
					<h2 class="text-xl font-bold">Reporte de Negocios</h2>
					<p class="text-gray-500">Análisis de crecimiento de negocios.</p>
					<BaseButton text="Descargar" variant="outlined" />
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="size-10 flex justify-center items-center bg-secondary rounded-full">
						<i class="fa-solid fa-chart-pie text-lg text-white"></i>
					</div>
					<h2 class="text-xl font-bold">Reporte de Ingresos</h2>
					<p class="text-gray-500">Resumen de ingresos por suscripciones.</p>
					<BaseButton text="Descargar" variant="outlined" />
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6 lg:col-span-4">
				<div class="flex flex-col gap-4">
					<div class="size-10 flex justify-center items-center bg-green-500 rounded-full">
						<i class="fa-solid fa-users text-lg text-white"></i>
					</div>
					<h2 class="text-xl font-bold">Reporte de Usuarios</h2>
					<p class="text-gray-500">Estadísticas de usuarios registrados.</p>
					<BaseButton text="Descargar" variant="outlined" />
				</div>
			</BaseCard>
		</div>
	</section>
</template>