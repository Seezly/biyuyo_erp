<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Usuarios</h1>
			<p>Administra y controla los usuarios de tu negocio</p>
		</div>
		<div class="grid w-full lg:grid-cols-12 gap-8">
			<BaseCard variant="outlined" class="col-span-12">
				<h2 class="text-primary font-semibold text-xl mb-8">Usuarios del negocio</h2>
				<div class="flex flex-col gap-4 w-full">
					<div
						class="flex flex-col lg:flex-row lg:items-center w-full border-b border-secondary/10 pb-4 gap-8"
					>
						<div class="size-12 rounded-full hidden bg-primary lg:flex justify-center items-center">
							<i class="fa-solid fa-boxes-packing text-xl text-white"></i>
						</div>
						<div>
							<div class="flex gap-4 justify-between items-center">
								<h3 class="text-primary text-lg font-medium">Nombre del usuario</h3>
								<p class="text-xs">V-28273564</p>
							</div>
							<p>Empleado</p>
						</div>
						<div class="flex gap-4 justify-center items-center lg:ml-auto">
							<BaseButton text="Editar" variant="outlined" class="w-full lg:w-auto" />
							<BaseButton text="Eliminar" class="w-full lg:w-auto" />
						</div>
					</div>
				</div>
			</BaseCard>
			<BaseCard variant="outlined" class="col-span-12">
				<h2 class="text-primary font-semibold text-xl mb-8">Registro de actividades de los usuarios</h2>
				<table class="min-w-full divide-y-2 divide-gray-200">
					<thead class="ltr:text-left rtl:text-right">
						<tr class="*:font-medium *:text-gray-900">
							<th class="px-4 py-2 whitespace-nowrap">Nombre</th>
							<th class="px-4 py-2 whitespace-nowrap">Cédula</th>
							<th class="px-4 py-2 whitespace-nowrap">Fecha</th>
							<th class="px-4 py-2 whitespace-nowrap">Acción</th>
							<th class="px-4 py-2 whitespace-nowrap">URL</th>
							<th class="px-4 py-2 whitespace-nowrap">Afectado</th>
						</tr>
					</thead>

					<tbody class="divide-y divide-gray-200 *:even:bg-gray-50">
						<tr class="*:text-gray-900 *:first:font-medium">
							<td class="px-4 py-2 whitespace-nowrap">Sergio Gutierrez</td>
							<td class="px-4 py-2 whitespace-nowrap">V28273564</td>
							<td class="px-4 py-2 whitespace-nowrap">27/04/2026</td>
							<td class="px-4 py-2 whitespace-nowrap">ELIMINAR</td>
							<td class="px-4 py-2 whitespace-nowrap">/categories</td>
							<td class="px-4 py-2 whitespace-nowrap">Categoría 1</td>
						</tr>
					</tbody>
				</table>
			</BaseCard>
		</div>
	</section>
</template>
