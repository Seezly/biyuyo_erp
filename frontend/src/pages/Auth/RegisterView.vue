<script setup lang="ts">
import { ref } from 'vue'
import router from '@/router'

import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import StepsItem from '@/components/StepsItem.vue'

import { apiFetch } from '@/utils/helpers'

interface RegisterForm {
	first_name: string
	last_name: string
	email: string
	identification_number: string
	phone: string
	password: string
	confirm_password: string
	business_name: string
	business_address: string
	state: string
	municipality: string
	business_rif: string
	business_description: string
}

const step = ref<number>(1)

const emit = defineEmits(['submit'])

const form = ref<RegisterForm>({
	first_name: '',
	last_name: '',
	email: '',
	identification_number: '',
	phone: '',
	password: '',
	confirm_password: '',
	business_name: '',
	business_address: '',
	state: '',
	municipality: '',
	business_rif: '',
	business_description: '',
})

const submit = async () => {
	try {
		const response = await apiFetch('http://localhost:8000/api/register/', {
			method: 'POST',
			body: JSON.stringify(form.value),
		})

		if (!response.ok) {
			const errorData = await response.json()
			console.error('Register failed:', errorData)
			return
		}

		const data = await response.json()

		emit('submit', data)

		router.push({ path: '/login' })
	} catch (error) {
		console.error('Network error:', error)
	}
}
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
							<BaseInput
								v-model="form.first_name"
								type="text"
								name="firstName"
								placeholder="Primer Nombre"
							/>
						</label>
						<label class="w-full flex flex-col text-dark">
							Primer Apellido
							<BaseInput
								v-model="form.last_name"
								type="text"
								name="lastName"
								placeholder="Primer Apellido"
							/>
						</label>
					</div>
					<label class="w-full flex flex-col text-dark">
						Correo electrónico
						<BaseInput v-model="form.email" type="email" name="email" placeholder="Correo electrónico" />
					</label>
					<label class="w-full flex flex-col text-dark">
						Cédula de identidad
						<BaseInput
							v-model="form.identification_number"
							type="text"
							name="identificationNumber"
							placeholder="E123456789 ó V12345678"
						/>
					</label>
					<label class="w-full flex flex-col text-dark">
						Teléfono
						<BaseInput v-model="form.phone" type="text" name="phone" placeholder="Teléfono" />
					</label>
					<div class="flex justify-between items-center gap-4 mb-8">
						<label class="w-full flex flex-col text-dark">
							Contraseña
							<BaseInput
								v-model="form.password"
								type="password"
								name="password"
								placeholder="Contraseña"
							/>
						</label>
						<label class="w-full flex flex-col text-dark">
							Confirmar Contraseña
							<BaseInput
								v-model="form.confirm_password"
								type="password"
								name="confirmPassword"
								placeholder="Confirmar Contraseña"
							/>
						</label>
					</div>
					<BaseButton text="Siguiente paso" @click="step++" />
				</article>
				<article
					:class="step === 2 ? '-translate-x-full' : 'translate-x-0'"
					class="shrink-0 basis-full w-full transform transition duration-200 flex flex-col gap-4"
				>
					<label class="w-full flex flex-col text-dark">
						Nombre del negocio
						<BaseInput
							v-model="form.business_name"
							type="text"
							name="businessName"
							placeholder="Nombre del negocio"
						/>
					</label>
					<label class="w-full flex flex-col text-dark">
						Dirección del negocio
						<BaseInput
							v-model="form.business_address"
							type="text"
							name="businessAddress"
							placeholder="Dirección del negocio"
						/>
					</label>
					<div class="flex justify-between items-center gap-4">
						<label class="w-full flex flex-col text-dark">
							Estado
							<BaseInput v-model="form.state" type="text" name="state" placeholder="Estado" />
						</label>
						<label class="w-full flex flex-col text-dark">
							Municipio
							<BaseInput
								v-model="form.municipality"
								type="text"
								name="municipality"
								placeholder="Municipio"
							/>
						</label>
					</div>
					<label class="w-full flex flex-col text-dark">
						R.I.F. del negocio (o personal)
						<BaseInput
							v-model="form.business_rif"
							type="text"
							name="rif"
							placeholder="J123456789 ó V123456789"
						/>
					</label>
					<label class="w-full flex flex-col text-dark mb-8">
						Descripción del negocio
						<BaseInput
							v-model="form.business_description"
							type="text"
							name="businessDescription"
							placeholder="Descripción del negocio"
						/>
					</label>
					<BaseButton @click="submit" text="Crear cuenta" />
				</article>
			</section>
		</form>
	</section>
</template>
