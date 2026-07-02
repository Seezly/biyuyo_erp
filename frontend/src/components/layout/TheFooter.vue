<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<template>
	<footer class="bg-primary text-white">
		<div class="max-w-6xl mx-auto px-8 py-12">
			<div class="grid grid-cols-1 md:grid-cols-4 gap-10">
				<!-- Brand -->
				<div class="md:col-span-1">
					<h2 class="font-heading text-2xl font-bold mb-3">Biyuyo</h2>
					<p class="text-white/70 text-sm leading-relaxed">
						Plataforma ERP multi-tenant para pequeñas empresas venezolanas.
					</p>
				</div>

				<!-- Producto -->
				<div>
					<h3 class="font-heading font-bold mb-4">Producto</h3>
					<ul class="flex flex-col gap-2 text-sm text-white/70">
						<li>
							<RouterLink to="/login" class="hover:text-white transition-colors"
								>Iniciar sesión</RouterLink
							>
						</li>
						<li>
							<RouterLink to="/register" class="hover:text-white transition-colors"
								>Registrarse</RouterLink
							>
						</li>
					</ul>
				</div>

				<!-- Empresa -->
				<div>
					<h3 class="font-heading font-bold mb-4">Empresa</h3>
					<ul class="flex flex-col gap-2 text-sm text-white/70">
						<li><a href="#" class="hover:text-white transition-colors">Acerca de</a></li>
						<li><a href="#" class="hover:text-white transition-colors">Contacto</a></li>
						<li><a href="#" class="hover:text-white transition-colors">Soporte</a></li>
					</ul>
				</div>

				<!-- Legal -->
				<div>
					<h3 class="font-heading font-bold mb-4">Legal</h3>
					<ul class="flex flex-col gap-2 text-sm text-white/70">
						<li><a href="#" class="hover:text-white transition-colors">Política de Privacidad</a></li>
						<li><a href="#" class="hover:text-white transition-colors">Términos de Uso</a></li>
					</ul>
				</div>
			</div>

			<!-- Bottom bar -->
			<div
				class="border-t border-white/20 mt-10 pt-6 flex flex-col md:flex-row justify-between items-center gap-4"
			>
				<p class="text-white/50 text-sm">&copy; 2026 Biyuyo ERP. Todos los derechos reservados.</p>
				<div class="flex gap-4 text-white/50">
					<a href="#" aria-label="Twitter" class="hover:text-white transition-colors">
						<i class="fa-brands fa-x-twitter text-lg"></i>
					</a>
					<a href="#" aria-label="GitHub" class="hover:text-white transition-colors">
						<i class="fa-brands fa-github text-lg"></i>
					</a>
					<a href="#" aria-label="Instagram" class="hover:text-white transition-colors">
						<i class="fa-brands fa-instagram text-lg"></i>
					</a>
				</div>
			</div>
		</div>
	</footer>
</template>
