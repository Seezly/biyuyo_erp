<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'

const features = [
	{
		icon: 'fa-solid fa-cash-register',
		title: 'Punto de Venta',
		description: 'Sistema POS rápido e intuitivo para gestionar ventas en tiempo real con control de stock automático.',
	},
	{
		icon: 'fa-solid fa-boxes-stacked',
		title: 'Inventario',
		description: 'Control completo de productos, categorías y movimientos de inventario con alertas de stock bajo.',
	},
	{
		icon: 'fa-solid fa-users',
		title: 'Clientes',
		description: 'Base de datos de clientes con historial de compras, búsqueda rápida y gestión de contactos.',
	},
	{
		icon: 'fa-solid fa-chart-line',
		title: 'Reportes',
		description: 'Reportes de ventas, inventario y finanzas con estadísticas detalladas para tomar mejores decisiones.',
	},
	{
		icon: 'fa-solid fa-truck',
		title: 'Proveedores',
		description: 'Gestión de proveedores y órdenes de compra con seguimiento de entregas y pagos.',
	},
	{
		icon: 'fa-solid fa-building',
		title: 'Multi-negocio',
		description: 'Administra múltiples negocios desde una sola cuenta con datos completamente aislados.',
	},
]
</script>

<template>
	<div>
		<!-- Hero Section -->
		<section class="bg-primary text-white py-20 px-4">
			<div class="max-w-4xl mx-auto text-center">
				<h1 class="font-heading text-4xl md:text-6xl font-extrabold mb-6 leading-tight">
					Gestiona tu negocio<br />de forma simple
				</h1>
				<p class="text-lg md:text-xl text-gray-200 mb-10 max-w-2xl mx-auto">
					Biyuyo ERP es la plataforma multi-tenant diseñada para pequeñas empresas
					venezolanas. Inventario, ventas, clientes y reportes en un solo lugar.
				</p>
				<div class="flex flex-col sm:flex-row gap-4 justify-center">
					<BaseButton to="/register" text="Comenzar gratis" variant="inverted" width="auto" />
					<BaseButton to="/login" text="Iniciar sesión" variant="ghost" width="auto" />
				</div>
			</div>
		</section>

		<!-- Features Section -->
		<section id="features" class="py-20 px-4">
			<div class="max-w-6xl mx-auto">
				<div class="text-center mb-14">
					<h2 class="font-heading text-3xl md:text-4xl font-bold text-dark mb-4">
						Todo lo que necesitas para tu negocio
					</h2>
					<p class="text-gray-500 text-lg max-w-2xl mx-auto">
						Herramientas poderosas pero fáciles de usar, diseñadas para que te enfoques en lo importante.
					</p>
				</div>
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
					<BaseCard v-for="feature in features" :key="feature.title">
						<div class="flex flex-col items-start gap-4">
							<div class="flex justify-center items-center size-12 rounded-full bg-secondary/10 text-secondary">
								<i :class="feature.icon + ' text-xl'" aria-hidden="true"></i>
							</div>
							<h3 class="font-heading text-xl font-bold text-dark">{{ feature.title }}</h3>
							<p class="text-gray-500 leading-relaxed">{{ feature.description }}</p>
						</div>
					</BaseCard>
				</div>
			</div>
		</section>

		<!-- CTA Section -->
		<section class="bg-secondary text-white py-20 px-4">
			<div class="max-w-3xl mx-auto text-center">
				<h2 class="font-heading text-3xl md:text-4xl font-bold mb-6">
					¿Listo para crecer?
				</h2>
				<p class="text-lg text-white/80 mb-10 max-w-xl mx-auto">
					Registra tu negocio hoy y comienza a gestionar todo desde una sola plataforma.
					Es gratis para empezar.
				</p>
				<BaseButton to="/register" text="Crear mi cuenta gratis" variant="inverted" width="auto" />
			</div>
		</section>
	</div>
</template>
