<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Alertas y Notificaciones</h1>
			<p>Administra tus preferencias de notificaciones y alertas</p>
		</div>
		<div class="flex flex-col gap-4 w-full">
			<div>
				<h2 class="text-primary text-lg font-semibold">Canales de notificación</h2>
				<p class="text-sm text-dark">
					Selecciona los canales por los cuales deseas recibir notificaciones y alertas importantes
				</p>
			</div>
			<div class="flex flex-col lg:flex-row gap-8 w-full">
				<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
					<div class="flex relative">
						<div class="w-11/12">
							<h2 class="text-lg font-semibold text-dark">Notificaciones por correo electrónico</h2>
							<p class="text-sm text-dark mb-4">
								Recibe actualizaciones y alertas importantes en tu correo electrónico.
							</p>
						</div>
						<label class="flex items-center gap-4">
							<input type="checkbox" class="absolute top-1/2 right-4 transform -translate-y-1/2" />
						</label>
					</div>
				</BaseCard>
				<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
					<div class="flex relative">
						<div class="w-11/12">
							<h2 class="text-lg font-semibold text-dark">Notificaciones Push</h2>
							<p class="text-sm text-dark mb-4">
								Recibe actualizaciones y alertas importantes en tu teléfono.
							</p>
						</div>
						<label class="flex items-center gap-4">
							<input type="checkbox" class="absolute top-1/2 right-4 transform -translate-y-1/2" />
						</label>
					</div>
				</BaseCard>
			</div>
		</div>
		<div class="flex flex-col gap-4 w-full">
			<div>
				<h2 class="text-primary text-lg font-semibold">Alertas de inventario</h2>
				<p class="text-sm text-dark">Seleccione cómo y cuándo desea recibir alertas de sus productos</p>
			</div>
			<div class="flex flex-col lg:flex-row gap-8 w-full">
				<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
					<div class="flex relative">
						<div class="w-11/12">
							<h2 class="text-lg font-semibold text-dark">Alertas de inventario bajo</h2>
							<p class="text-sm text-dark mb-4">
								Recibir alertas cuando el inventario esté por debajo del nivel mínimo.
							</p>
						</div>
						<label class="flex items-center gap-4">
							<input type="checkbox" class="absolute top-1/2 right-4 transform -translate-y-1/2" />
						</label>
					</div>
				</BaseCard>
				<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
					<div class="flex relative">
						<div class="w-11/12">
							<h2 class="text-lg font-semibold text-dark">Alertas de producto agotado</h2>
							<p class="text-sm text-dark mb-4">Recibir alertas cuando un producto esté agotado.</p>
						</div>
						<label class="flex items-center gap-4">
							<input type="checkbox" class="absolute top-1/2 right-4 transform -translate-y-1/2" />
						</label>
					</div>
				</BaseCard>
			</div>
		</div>
	</section>
</template>
