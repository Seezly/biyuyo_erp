<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Configuración del Sistema</h1>
			<p>Administración global de la plataforma</p>
		</div>

		<div class="grid grid-cols-12 gap-8 w-full">
			<BaseCard variant="outlined" class="col-span-12 md:col-span-6">
				<div class="flex flex-col gap-4">
					<h2 class="text-xl font-bold text-primary">Planes de Suscripción</h2>
					<p class="text-gray-500">Gestionar planes disponibles para los negocios.</p>
					<BaseButton to="/billing/plans" text="Administrar planes" />
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6">
				<div class="flex flex-col gap-4">
					<h2 class="text-xl font-bold text-primary">Configuración de Facturación</h2>
					<p class="text-gray-500">Parámetros de facturación y pagos.</p>
					<BaseButton to="/billing/invoices" text="Ver facturas" variant="outlined" />
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6">
				<div class="flex flex-col gap-4">
					<h2 class="text-xl font-bold text-primary">Usuarios y Roles</h2>
					<p class="text-gray-500">Gestionar usuarios del sistema y permisos por rol.</p>
					<BaseButton to="/users" text="Administrar usuarios" variant="outlined" />
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6">
				<div class="flex flex-col gap-4">
					<h2 class="text-xl font-bold text-primary">Negocios Registrados</h2>
					<p class="text-gray-500">Ver y administrar los negocios activos en la plataforma.</p>
					<BaseButton to="/businesses" text="Ver negocios" variant="outlined" />
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6">
				<div class="flex flex-col gap-4">
					<h2 class="text-xl font-bold text-primary">Reportes Globales</h2>
					<p class="text-gray-500">Estadísticas agregadas de todos los negocios.</p>
					<BaseButton to="/reports" text="Ver reportes" variant="outlined" />
				</div>
			</BaseCard>

			<BaseCard variant="outlined" class="col-span-12 md:col-span-6">
				<div class="flex flex-col gap-4">
					<h2 class="text-xl font-bold text-primary">Auditoría del Sistema</h2>
					<p class="text-gray-500">Registro de actividades y cambios en el sistema.</p>
					<BaseButton to="/audit" text="Ver auditoría" variant="outlined" />
				</div>
			</BaseCard>
		</div>
	</section>
</template>
