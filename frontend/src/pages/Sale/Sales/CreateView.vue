<script setup lang="ts">
import { ref } from 'vue'

import StepsItem from '@/components/StepsItem.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const currentStep = ref<number>(1)
const steps = [
	{
		step: 1,
		label: 'Agregar productos',
	},
	{
		step: 2,
		label: 'Método de pago',
	},
	{
		step: 3,
		label: 'Recibo',
	},
]
</script>

<template>
	<section
		class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start overflow-hidden"
	>
		<div>
			<h1 class="text-primary text-2xl font-bold">Punto de Venta (POS)</h1>
			<p>Registra nuevas ventas y administra el proceso de venta en tiempo real</p>
		</div>
		<StepsItem :step="currentStep" :steps="steps" />
		<section class="w-full flex justify-start items-start overflow-hidden">
			<article
				:class="currentStep === 1 ? 'translate-x-0' : '-translate-x-full'"
				class="shrink-0 basis-full w-full transform transition duration-200 flex flex-col gap-4"
			>
				<div class="grid grid-cols-12 grid-rows-[minmax(0,1fr)] lg:grid-rows-6 w-full gap-8">
					<BaseCard
						variant="outlined"
						class="col-span-full order-2 lg:order-1 lg:col-span-9 lg:row-span-6 overflow-y-auto"
					></BaseCard>
					<BaseInput
						class="col-span-full order-1 lg:order-2 lg:col-span-3 lg:row-span-1"
						placeholder="Busca producto por nombre"
					/>
					<BaseCard
						variant="secondary"
						class="col-span-full order-3 lg:order-3 lg:col-span-3 lg:row-span-5"
					>
						<div class="flex flex-col w-full h-full gap-4">
							<h2 class="text-2xl font-bold text-primary">Total del pedido</h2>
							<div class="flex flex-col gap-2">
								<div class="flex justify-between items-center">
									<p>Subtotal</p>
									<p class="font-bold">$0,00</p>
								</div>
								<div class="flex justify-between items-center">
									<p>IVA</p>
									<p class="font-bold">$0,00</p>
								</div>
							</div>
							<hr />
							<div class="flex justify-between items-center">
								<p class="font-medium">Total</p>
								<div>
									<p class="font-bold text-2xl text-right font-heading text-primary mb-2">$0,00</p>
									<p class="text-sm text-right">Bs. 0,00</p>
								</div>
							</div>
							<BaseButton class="mt-auto" text="Método de pago" @click="currentStep++" />
						</div>
					</BaseCard>
				</div>
			</article>
			<article
				:class="currentStep === 2 ? '-translate-x-full' : 'translate-x-0'"
				class="shrink-0 basis-full w-full transform transition duration-200 flex flex-col gap-4"
			>
				<div class="grid grid-cols-12 grid-rows-[minmax(0,1fr)] lg:grid-rows-5 w-full gap-8">
					<BaseCard
						variant="outlined"
						class="col-span-full order-2 lg:order-1 lg:col-span-9 lg:row-span-5 overflow-y-auto"
					></BaseCard>
					<BaseCard
						variant="outlined"
						class="col-span-full order-1 lg:order-2 lg:col-span-3 lg:row-span-2"
					>
						<div class="flex flex-col justify-center items-center gap-4">
							<h2 class="text-lg font-semibold">Total del pedido</h2>
							<p class="text-4xl font-heading font-bold text-primary">$0,00</p>
							<p class="text-lg">Bs. 0,00</p>
						</div>
					</BaseCard>
					<BaseCard
						variant="secondary"
						class="col-span-full order-3 lg:order-3 lg:col-span-3 lg:row-span-3"
					>
						<div class="flex flex-col w-full h-full gap-4">
							<h2 class="text-lg font-semibold text-white">Nota cambiaria</h2>
							<p class="text-sm">
								La tasa cambiaria se actualiza cada 30 minutos y se toma como referencia la tasa actual del
								Dólar Estadounidense (US$) del Banco Central de Venezuela. La tasa actual es de
								<span class="text-primary font-medium">1 USD = 465.75 Bs</span>
							</p>
							<BaseButton class="mt-auto" text="¡Listo!" @click="currentStep++" />
						</div>
					</BaseCard>
				</div>
			</article>
			<article
				:class="currentStep === 3 ? '-translate-x-[200%]' : 'translate-x-0'"
				class="shrink-0 basis-full w-full transform transition duration-200 flex flex-col gap-4"
			>
				<div class="grid grid-cols-12 grid-rows-[minmax(0,1fr)] lg:grid-rows-3 w-full gap-8">
					<BaseCard
						variant="outlined"
						class="col-span-full order-1 lg:col-span-9 lg:row-span-3 overflow-y-auto"
					>
						<div class="flex flex-col justify-center items-center h-full gap-4">
							<div class="rounded-full bg-primary size-32 flex justify-center items-center">
								<i class="fa-solid fa-circle-check text-6xl text-[#fff]"></i>
							</div>
							<h2 class="text-4xl font-heading font-bold text-center text-primary">
								¡Venta completada exitosamente!
							</h2>
							<p class="">La venta ha sido procesada y registrada en Biyuyo con éxito.</p>
							<hr />
							<BaseCard variant="outlined">
								<div class="flex flex-col justify-center items-start gap-2">
									<h2 class="text-xl font-semibold text-primary">ID. de Transacción</h2>
									<p class="text-2xl font-bold">#ISA-0000-0000-000</p>
								</div>
							</BaseCard>
						</div>
					</BaseCard>
					<BaseCard variant="secondary" class="col-span-full order-2 lg:col-span-3 lg:row-span-1">
						<div class="flex flex-col justify-center items-start gap-2">
							<h2 class="text-xl font-semibold text-white">Monto total</h2>
							<p class="text-4xl font-bold text-primary">$1.240,00</p>
							<p class="font-medium">Bs. 45.560,00</p>
						</div>
					</BaseCard>
					<BaseCard variant="outlined" class="col-span-full order-3 lg:col-span-3 lg:row-span-2">
						<div class="flex flex-col justify-center items-center gap-4">
							<h2 class="text-lg font-semibold">Opciones</h2>
							<BaseButton text="Imprimir recibo" variant="outlined" />
							<BaseButton text="Guardar recibo" variant="outlined" />
							<BaseButton text="Enviar recibo" variant="outlined" />
							<hr />
							<BaseButton text="Inicio" variant="outlined" />
							<BaseButton text="Nueva venta" />
						</div>
					</BaseCard>
				</div>
			</article>
		</section>
	</section>
</template>
