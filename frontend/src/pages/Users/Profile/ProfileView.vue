<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCheckbox from '@/components/ui/BaseCheckbox.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Mi perfil</h1>
			<p>Maneja tu información personal y preferencias</p>
		</div>
		<div class="w-full h-screen grid grid-cols-12 grid-rows-12 gap-8">
			<BaseCard
				variant="outlined"
				class="col-span-full w-full row-span-full lg:col-span-8 lg:row-span-8"
			>
				<div class="flex flex-col gap-4">
					<form action="" class="flex justify-start items-start flex-col gap-4 w-full">
						<h2 class="text-xl text-primary font-bold">Información del negocio</h2>
						<div class="flex justify-between items-center gap-4 w-full">
							<label for="" class="w-full flex flex-col text-dark">
								Nombre del negocio
								<BaseInput name="business_name" model-value="" disabled />
							</label>
							<label for="" class="w-full flex flex-col text-dark">
								Correo electrónico
								<BaseInput name="email" type="email" model-value="" disabled />
							</label>
						</div>
						<label for="" class="w-full flex flex-col text-dark">
							Teléfono
							<BaseInput name="phone" model-value="" disabled />
						</label>
						<div class="flex justify-between items-center gap-4 w-full">
							<label for="" class="w-full flex flex-col text-dark">
								Estado
								<BaseInput name="state" model-value="" disabled />
							</label>
							<label for="" class="w-full flex flex-col text-dark">
								Municipio
								<BaseInput name="municipality" model-value="" disabled />
							</label>
						</div>
						<label for="" class="w-full flex flex-col text-dark">
							Dirección
							<BaseInput name="business_address" model-value="" disabled />
						</label>
					</form>
				</div>
			</BaseCard>
			<BaseCard
				variant="outlined"
				class="col-span-full w-full row-span-full lg:col-span-4 lg:row-span-6"
			>
				<div class="flex flex-col gap-4">
					<h2 class="text-xl text-primary font-bold">Seguridad de la cuenta</h2>
					<BaseButton to="/profile/change-password" text="Cambiar contraseña" />
					<BaseButton to="/profile/2fa" text="Autenticación 2FA" />
					<hr />
					<BaseButton to="/profile/notifications" text="Notificaciones" />
					<BaseButton to="/profile/reminders" text="Recordatorios" />
				</div>
			</BaseCard>
			<BaseCard class="col-span-full w-full row-span-full lg:col-span-4 lg:row-span-4">
				<div class="flex flex-col gap-4 justify-between h-full w-full">
					<div>
						<h2 class="text-2xl font-bold text-white mb-2">¿Necesitas ayuda?</h2>
						<p class="text-sm text-white">
							Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos.
						</p>
					</div>
					<BaseButton variant="secondary" to="/contact" width="auto" text="Chatea con soporte" />
				</div>
			</BaseCard>
			<BaseCard
				variant="outlined"
				class="col-span-full w-full row-span-full lg:col-span-8 lg:row-span-4"
			>
				<div class="flex flex-col gap-4">
					<form action="" class="flex justify-start items-start flex-col gap-4 w-full">
						<h2 class="text-xl text-primary font-bold">Métodos de pago aceptados</h2>
						<div class="flex gap-4 w-full">
							<BaseCheckbox text="Punto de Venta (POS)" type="button" />
							<BaseCheckbox text="Binance" type="button" />
							<BaseCheckbox text="Zelle" type="button" />
							<BaseCheckbox text="Pago móvil" type="button" />
							<BaseCheckbox text="Transferencia bancaria" type="button" />
							<BaseCheckbox text="Efectivo" type="button" />
						</div>
					</form>
				</div>
			</BaseCard>
		</div>
	</section>
</template>
