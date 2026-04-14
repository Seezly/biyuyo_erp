<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Recordatorios</h1>
			<p>Personaliza cómo y cuándo tus clientes reciben recordatorios sobre sus pagos pendientes.</p>
		</div>
		<div class="flex flex-col gap-4 w-full">
			<div>
				<h2 class="text-primary text-lg font-semibold">Canales de envío</h2>
				<p class="text-sm text-dark">
					Selecciona los canales por los cuales deseas que tus clientes reciban recordatorios de pagos
					pendientes
				</p>
			</div>
			<div class="flex flex-col lg:flex-row gap-8 w-full">
				<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
					<div class="flex relative">
						<div class="w-10/12">
							<h2 class="text-lg font-semibold text-dark">Recordatorios por WhatsApp</h2>
							<p class="text-sm text-dark">Mensajería instantánea directa.</p>
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
				<h2 class="text-primary text-lg font-semibold">Frecuencia de envío</h2>
				<p class="text-sm text-dark">
					Personaliza la frecuencia con la que tus clientes reciben recordatorios de pagos pendientes
					para mantenerlos informados y motivados a realizar sus pagos a tiempo.
				</p>
			</div>
			<div class="flex flex-col lg:flex-row gap-8 w-full">
				<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
					<div class="flex relative">
						<div class="w-10/12">
							<h2 class="text-lg font-semibold text-dark">Recordatorio preventivo</h2>
							<p class="text-sm text-dark">Enviar 3 días antes de la fecha de vencimiento del pago.</p>
						</div>
						<label class="flex items-center gap-4">
							<input type="checkbox" class="absolute top-1/2 right-4 transform -translate-y-1/2" />
						</label>
					</div>
				</BaseCard>
				<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
					<div class="flex relative">
						<div class="w-10/12">
							<h2 class="text-lg font-semibold text-dark">Recordatorio de vencimiento</h2>
							<p class="text-sm text-dark">Enviar el mismo día de la fecha de vencimiento del pago.</p>
						</div>
						<label class="flex items-center gap-4">
							<input type="checkbox" class="absolute top-1/2 right-4 transform -translate-y-1/2" />
						</label>
					</div>
				</BaseCard>
				<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
					<div class="flex relative">
						<div class="w-10/12">
							<h2 class="text-lg font-semibold text-dark">Recordatorio de mora</h2>
							<p class="text-sm text-dark">
								Enviar cada 7 días después de la fecha de vencimiento del pago.
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
				<h2 class="text-primary text-lg font-semibold">Mensaje predefinido</h2>
				<p class="text-sm text-dark">
					Personaliza el mensaje que se enviará a tus clientes en cada recordatorio para mantener una
					comunicación clara
				</p>
			</div>
			<div class="flex flex-col lg:flex-row gap-8 w-full">
				<BaseCard variant="outlined" class="flex-1 hover:shadow-lg transition-shadow">
					<div class="flex flex-col gap-4">
						<h2 class="text-lg font-semibold text-dark">Plantilla del mensaje</h2>
						<div class="flex flex-col lg:flex-row justify-between items-start gap-4">
							<textarea
								name="messageTemplate"
								class="w-full lg:w-2/3 h-48 lg:h-32 py-2 px-4 rounded border border-secondary text-dark"
							>
Hola [nombre], te recordamos que tienes un pago pendiente de [monto] con fecha próxima a vencer el día [fecha]. Por favor, puedes realizar el pago por cualquier medio que manejemos. ¡Gracias por tu atención!</textarea
							>
							<div class="flex-1 w-full flex flex-col items-center gap-4">
								<p class="text-lg font-semibold">Variables utilizables</p>
								<div class="flex gap-4">
									<span
										class="bg-secondary px-4 py-2 rounded-full hover:bg-primary text-white transition cursor-pointer"
										>[nombre]</span
									>
									<span
										class="bg-secondary px-4 py-2 rounded-full hover:bg-primary text-white transition cursor-pointer"
										>[monto]</span
									>
									<span
										class="bg-secondary px-4 py-2 rounded-full hover:bg-primary text-white transition cursor-pointer"
										>[fecha]</span
									>
								</div>
							</div>
						</div>
						<p class="text-sm font-italic">
							Las etiquetas entre corchetes se reemplazarán automáticamente con los datos del cliente.
						</p>
					</div>
				</BaseCard>
			</div>
			<div class="flex flex-col lg:flex-row gap-8 w-full">
				<BaseCard variant="primary" class="flex-1 hover:shadow-lg transition-shadow">
					<div class="flex flex-col gap-4">
						<h2 class="text-lg font-semibold text-white">Vista previa del mensaje</h2>
						<div class="flex justify-between items-start bg-[#fff] rounded-lg p-8">
							<p>
								Hola <span class="text-primary font-medium">José</span>, te recordamos que tienes un pago
								pendiente de <span class="text-primary font-medium">$100</span> con fecha próxima a vencer
								el día <span class="text-primary font-medium">15/04/2026</span>. Por favor, puedes realizar
								el pago por cualquier medio que manejemos. ¡Gracias por tu atención!
							</p>
						</div>
					</div>
				</BaseCard>
			</div>
		</div>
		<div class="flex gap-4 w-full">
			<BaseButton text="Descartar cambios" variant="outlined" />
			<BaseButton text="Guardar cambios" />
		</div>
	</section>
</template>
