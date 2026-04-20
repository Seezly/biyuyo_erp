<script setup lang="ts">
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Lista de categorías</h1>
			<p>Administra las categorías en tu inventario</p>
		</div>
		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseButton
				to="/inventory/categories/add"
				text="Añadir categoría"
				class="col-span-12 lg:col-span-3"
			/>
			<BaseInput placeholder="Buscar categoría por nombre" class="col-span-12 lg:col-span-5" />
			<div class="flex lg:justify-end justify-between items-center gap-2 col-span-12 lg:col-span-4">
				<label
					for="1"
					class="px-4 py-2 text-ellipsis overflow-hidden whitespace-nowrap bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition"
				>
					Todas
					<input
						type="checkbox"
						class="absolute opacity-0 cursor-pointer h-full w-full"
						name="1"
						id=""
						checked
					/>
				</label>
				<label
					for="2"
					class="px-4 py-2 text-ellipsis overflow-hidden whitespace-nowrap bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-[#fff] relative transition"
				>
					Subcategorías (n)
					<input
						type="checkbox"
						class="absolute opacity-0 cursor-pointer h-full w-full"
						name="2"
						id=""
					/>
				</label>
				<label
					for="3"
					class="px-4 py-2 text-ellipsis overflow-hidden whitespace-nowrap bg-[#fff] has-checked:bg-primary has-checked:text-[#fff] has-checked:hover:bg-primary/90 border border-primary rounded-full flex flex-col justify-center items-center text-center hover:bg-primary/90 hover:text-white relative transition"
				>
					Categorías (n)
					<input
						type="checkbox"
						class="absolute opacity-0 cursor-pointer h-full w-full"
						name="3"
						id=""
					/>
				</label>
			</div>
		</div>
		<div class="grid grid-cols-12 gap-4 w-full">
			<BaseCard variant="outlined" class="col-span-full lg:col-span-3 row-span-1">
				<div class="flex flex-col gap-4 justify-start items-start">
					<div class="flex justify-between w-full items-center">
						<div class="flex flex-col gap-2">
							<h2 class="font-bold text-lg text-primary">Categoría 1</h2>
							<span class="text-xs">Categoría padre</span>
						</div>
					</div>
				</div>
			</BaseCard>
		</div>
	</section>
</template>
