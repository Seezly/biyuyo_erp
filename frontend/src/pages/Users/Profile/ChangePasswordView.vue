<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Cambiar contraseña</h1>
			<p>Cambia la contraseña de tu cuenta en cualquier momento</p>
		</div>
		<BaseCard variant="outlined" class="mx-auto">
			<div class="flex flex-col gap-4">
				<form action="" class="flex justify-start items-start flex-col gap-4 w-md">
					<label for="" class="w-full flex flex-col text-dark">
						Contraseña actual
						<BaseInput name="current_password" type="password" model-value="" />
					</label>
					<label for="" class="w-full flex flex-col text-dark">
						Contraseña nueva
						<BaseInput name="new_password" type="password" model-value="" />
					</label>
					<label for="" class="w-full flex flex-col text-dark">
						Repite la contraseña
						<BaseInput name="confirm_password" type="password" model-value="" />
					</label>
					<BaseButton text="Cambiar contraseña" class="mt-4" />
				</form>
			</div>
		</BaseCard>
	</section>
</template>
