<script setup lang="ts">
import { ref } from 'vue'

import ButtonItem from '@/components/ui/ButtonItem.vue'
import InputItem from '@/components/ui/InputItem.vue'
import StepsItem from '@/components/StepsItem.vue'

const step = ref<number>(1)
</script>

<template>
	<section class="min-h-screen w-full flex flex-col items-center justify-center">
		<div class="mb-8">
			<h1 class="text-3xl text-center font-bold text-primary mb-4">Crear cuenta</h1>
			<p class="text-dark text-center">
				Rellena tus datos para crear una cuenta y empezar a utilizar Biyuyo ERP
			</p>
		</div>
		<StepsItem
			:step="step"
			:steps="[
				{ step: 1, label: 'Datos personales' },
				{ step: 2, label: 'Datos del negocio' },
			]"
		/>
		<form action="" class="flex justify-start items-center flex-col gap-4 w-md">
			<section class="w-full flex justify-start items-start overflow-hidden">
				<article
					:class="step === 1 ? 'translate-x-0' : '-translate-x-full'"
					class="shrink-0 basis-full w-full transform transition duration-200 flex flex-col gap-4"
				>
					<div class="flex justify-between items-center gap-4">
						<label class="w-full flex flex-col text-dark">
							Primer Nombre
							<InputItem type="text" name="firstName" placeholder="Primer Nombre" />
						</label>
						<label class="w-full flex flex-col text-dark">
							Primer Apellido
							<InputItem type="text" name="lastName" placeholder="Primer Apellido" />
						</label>
					</div>
					<label class="w-full flex flex-col text-dark">
						Correo electrónico
						<InputItem type="email" name="email" placeholder="Correo electrónico" />
					</label>
					<label class="w-full flex flex-col text-dark">
						Cédula de identidad
						<InputItem type="text" name="identification_number" placeholder="E123456789 ó V12345678" />
					</label>
					<label class="w-full flex flex-col text-dark">
						Teléfono
						<InputItem type="text" name="phone" placeholder="Teléfono" />
					</label>
					<div class="flex justify-between items-center gap-4 mb-8">
						<label class="w-full flex flex-col text-dark">
							Contraseña
							<InputItem type="password" name="password" placeholder="Contraseña" />
						</label>
						<label class="w-full flex flex-col text-dark">
							Confirmar Contraseña
							<InputItem type="password" name="confirmPassword" placeholder="Confirmar Contraseña" />
						</label>
					</div>
					<ButtonItem text="Siguiente paso" @click.prevent="step++" />
				</article>
				<article
					:class="step === 2 ? '-translate-x-full' : 'translate-x-0'"
					class="shrink-0 basis-full w-full transform transition duration-200 flex flex-col gap-4"
				>
					<label class="w-full flex flex-col text-dark">
						Nombre del negocio
						<InputItem type="text" name="businessName" placeholder="Nombre del negocio" />
					</label>
					<label class="w-full flex flex-col text-dark">
						Dirección del negocio
						<InputItem type="text" name="businessAddress" placeholder="Dirección del negocio" />
					</label>
					<div class="flex justify-between items-center gap-4">
						<label class="w-full flex flex-col text-dark">
							Estado
							<InputItem type="text" name="state" placeholder="Estado" />
						</label>
						<label class="w-full flex flex-col text-dark">
							Municipio
							<InputItem type="text" name="municipality" placeholder="Municipio" />
						</label>
					</div>
					<label class="w-full flex flex-col text-dark">
						R.I.F. del negocio (o personal)
						<InputItem type="text" name="rif" placeholder="J123456789 ó V123456789" />
					</label>
					<label class="w-full flex flex-col text-dark mb-8">
						Descripción del negocio
						<InputItem type="text" name="businessDescription" placeholder="Descripción del negocio" />
					</label>
					<ButtonItem text="Crear cuenta" />
				</article>
			</section>
		</form>
	</section>
</template>
