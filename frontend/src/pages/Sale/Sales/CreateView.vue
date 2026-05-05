<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import StepsItem from '@/components/StepsItem.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useInventoryStore } from '@/stores/inventory'
import { useSalesStore } from '@/stores/sales'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const inventoryStore = useInventoryStore()
const salesStore = useSalesStore()
const toastStore = useToastStore()

const currentStep = ref(1)
const steps = [
	{ step: 1, label: 'Agregar productos' },
	{ step: 2, label: 'Método de pago' },
	{ step: 3, label: 'Recibo' },
]

const searchQuery = ref('')
const cart = ref<any[]>([])
const paymentMethod = ref('cash')
const saleId = ref<number | null>(null)

const IVA_RATE = 0.16

onMounted(async () => {
	await inventoryStore.fetchProducts()
})

const filteredProducts = computed(() => {
	if (!searchQuery.value) return inventoryStore.products
	const query = searchQuery.value.toLowerCase()
	return inventoryStore.products.filter(
		p => p.name.toLowerCase().includes(query) || p.sku.toLowerCase().includes(query)
	)
})

const cartTotal = computed(() => {
	return cart.value.reduce((sum, item) => sum + item.total, 0)
})

const cartSubtotal = computed(() => cartTotal.value)
const cartIva = computed(() => cartTotal.value * IVA_RATE)
const cartTotalWithIva = computed(() => cartSubtotal.value + cartIva.value)

const addToCart = (product: any) => {
	const existing = cart.value.find(item => item.product === product.id)
	if (existing) {
		existing.quantity += 1
		existing.total = existing.quantity * product.sell_price
	} else {
		cart.value.push({
			product: product.id,
			product_name: product.name,
			quantity: 1,
			unit_price: product.sell_price,
			total: product.sell_price,
			stock: product.stock,
		})
	}
}

const removeFromCart = (index: number) => {
	cart.value.splice(index, 1)
}

const updateQuantity = (index: number, delta: number) => {
	const item = cart.value[index]
	const newQty = item.quantity + delta
	if (newQty < 1) return
	if (newQty > item.stock) {
		toastStore.warning(`Stock máximo: ${item.stock}`)
		return
	}
	item.quantity = newQty
	item.total = item.quantity * item.unit_price
}

const goToPayment = () => {
	if (cart.value.length === 0) {
		toastStore.warning('Agrega productos al carrito')
		return
	}
	currentStep.value = 2
}

const processPayment = async () => {
	if (cart.value.length === 0) return

	const stockErrors: string[] = []
	for (const item of cart.value) {
		if (item.quantity > item.stock) {
			stockErrors.push(`${item.product_name}: stock insuficiente`)
		}
	}

	if (stockErrors.length > 0) {
		toastStore.error(stockErrors.join(', '))
		return
	}

	const saleData = {
		customer: 1,
		subtotal: cartSubtotal.value,
		discount: 0,
		tax: cartIva.value,
		total: cartTotalWithIva.value,
		items: cart.value.map(item => ({
			product: item.product,
			quantity: item.quantity,
			unit_price: item.unit_price,
			total_price: item.total,
		})),
		payments: [
			{
				method: paymentMethod.value,
				amount: cartTotalWithIva.value,
				reference: '',
			},
		],
	}

	const result = await salesStore.createSale(saleData)

	if (result && result.id) {
		saleId.value = result.id
		toastStore.success('Venta procesada correctamente')
		currentStep.value = 3
		await inventoryStore.fetchProducts()
	} else {
		toastStore.error(salesStore.error || 'Error al procesar la venta')
	}
}

const startNewSale = () => {
	currentStep.value = 1
	cart.value = []
	saleId.value = null
	paymentMethod.value = 'cash'
	searchQuery.value = ''
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start overflow-hidden">
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
					<div class="col-span-full order-2 lg:order-1 lg:col-span-9 lg:row-span-6 overflow-y-auto">
						<div v-if="inventoryStore.loading" class="text-center py-8">
							<p>Cargando productos...</p>
						</div>
						<div v-else-if="filteredProducts.length === 0" class="text-center py-8">
							<p class="text-gray-500">No hay productos disponibles</p>
						</div>
						<div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
							<BaseCard
								v-for="product in filteredProducts"
								:key="product.id"
								variant="outlined"
								class="cursor-pointer hover:border-primary transition-colors"
								@click="addToCart(product)"
							>
								<div class="flex flex-col gap-2">
									<div class="flex justify-between items-start">
										<span
											:class="product.stock === 0 ? 'bg-red-500' : product.stock <= product.min_stock ? 'bg-yellow-500' : 'bg-green-500'"
											class="text-xs text-white px-2 py-1 rounded"
										>
											{{ product.stock }} uds
										</span>
									</div>
									<h3 class="font-bold text-sm truncate">{{ product.name }}</h3>
									<p class="text-lg font-bold text-primary">${{ product.sell_price }}</p>
									<BaseButton text="Agregar" size="sm" width="full" />
								</div>
							</BaseCard>
						</div>
					</div>
					<BaseInput
						v-model="searchQuery"
						class="col-span-full order-1 lg:order-2 lg:col-span-3 lg:row-span-1"
						placeholder="Busca producto por nombre"
					/>
					<BaseCard
						variant="secondary"
						class="col-span-full order-3 lg:order-3 lg:col-span-3 lg:row-span-5"
					>
						<div class="flex flex-col w-full h-full gap-4">
							<h2 class="text-2xl font-bold text-primary">Total del pedido</h2>

							<div v-if="cart.length === 0" class="text-center py-8 text-white/70">
								<p>Carrito vacío</p>
							</div>

							<div v-else class="flex flex-col gap-2 max-h-48 overflow-y-auto">
								<div
									v-for="(item, index) in cart"
									:key="index"
									class="flex justify-between items-center bg-white/10 p-2 rounded"
								>
									<div class="flex-1">
										<p class="text-sm font-medium truncate">{{ item.product_name }}</p>
										<p class="text-xs text-white/70">${{ item.unit_price }} c/u</p>
									</div>
									<div class="flex items-center gap-2">
										<button
											class="w-6 h-6 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center"
											@click="updateQuantity(index, -1)"
										>
											-
										</button>
										<span class="text-sm font-bold">{{ item.quantity }}</span>
										<button
											class="w-6 h-6 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center"
											@click="updateQuantity(index, 1)"
										>
											+
										</button>
									</div>
									<p class="text-sm font-bold">${{ item.total }}</p>
									<button
										class="text-red-400 hover:text-red-300"
										@click="removeFromCart(index)"
									>
										<i class="fa-solid fa-trash"></i>
									</button>
								</div>
							</div>

							<div v-if="cart.length > 0" class="flex flex-col gap-2">
								<div class="flex justify-between items-center">
									<p class="text-white/80">Subtotal</p>
									<p class="font-bold">${{ cartSubtotal.toFixed(2) }}</p>
								</div>
								<div class="flex justify-between items-center">
									<p class="text-white/80">IVA (16%)</p>
									<p class="font-bold">${{ cartIva.toFixed(2) }}</p>
								</div>
							</div>
							<hr class="border-white/20" />
							<div class="flex justify-between items-center">
								<p class="font-medium text-white">Total</p>
								<div>
									<p class="font-bold text-2xl text-right font-heading text-primary mb-2">
										${{ cartTotalWithIva.toFixed(2) }}
									</p>
									<p class="text-sm text-right text-white/70">Bs. {{ (cartTotalWithIva * 500).toFixed(2) }}</p>
								</div>
							</div>
							<BaseButton
								class="mt-auto"
								text="Método de pago"
								:disabled="cart.length === 0"
								@click="goToPayment"
							/>
						</div>
					</BaseCard>
				</div>
			</article>

			<article
				:class="currentStep === 2 ? '-translate-x-full' : 'translate-x-0'"
				class="shrink-0 basis-full w-full transform transition duration-200 flex flex-col gap-4"
			>
				<div class="grid grid-cols-12 grid-rows-[minmax(0,1fr)] lg:grid-rows-5 w-full gap-8">
					<div class="col-span-full order-2 lg:order-1 lg:col-span-9 lg:row-span-5 overflow-y-auto">
						<BaseCard variant="outlined" class="p-6">
							<h2 class="text-xl font-bold mb-4">Selecciona el método de pago</h2>
							<div class="grid grid-cols-2 md:grid-cols-3 gap-4">
								<BaseCard
									variant="outlined"
									:class="paymentMethod === 'cash' ? 'border-primary bg-primary/10' : ''"
									class="cursor-pointer"
									@click="paymentMethod = 'cash'"
								>
									<div class="flex flex-col items-center gap-2 p-4">
										<i class="fa-solid fa-money-bill text-3xl text-primary"></i>
										<p class="font-bold">Efectivo</p>
									</div>
								</BaseCard>
								<BaseCard
									variant="outlined"
									:class="paymentMethod === 'card' ? 'border-primary bg-primary/10' : ''"
									class="cursor-pointer"
									@click="paymentMethod = 'card'"
								>
									<div class="flex flex-col items-center gap-2 p-4">
										<i class="fa-solid fa-credit-card text-3xl text-primary"></i>
										<p class="font-bold">Tarjeta</p>
									</div>
								</BaseCard>
								<BaseCard
									variant="outlined"
									:class="paymentMethod === 'transfer' ? 'border-primary bg-primary/10' : ''"
									class="cursor-pointer"
									@click="paymentMethod = 'transfer'"
								>
									<div class="flex flex-col items-center gap-2 p-4">
										<i class="fa-solid fa-building-columns text-3xl text-primary"></i>
										<p class="font-bold">Transferencia</p>
									</div>
								</BaseCard>
							</div>
						</BaseCard>
					</div>
					<BaseCard
						variant="outlined"
						class="col-span-full order-1 lg:order-2 lg:col-span-3 lg:row-span-2"
					>
						<div class="flex flex-col justify-center items-center gap-4">
							<h2 class="text-lg font-semibold">Total del pedido</h2>
							<p class="text-4xl font-heading font-bold text-primary">${{ cartTotalWithIva.toFixed(2) }}</p>
							<p class="text-lg">Bs. {{ (cartTotalWithIva * 500).toFixed(2) }}</p>
						</div>
					</BaseCard>
					<BaseCard
						variant="secondary"
						class="col-span-full order-3 lg:order-3 lg:col-span-3 lg:row-span-3"
					>
						<div class="flex flex-col w-full h-full gap-4">
							<h2 class="text-lg font-semibold text-white">Nota cambiaria</h2>
							<p class="text-sm text-white/80">
								La tasa cambiaria se actualiza cada 30 minutos y se toma como referencia la tasa actual del
								Dólar Estadounidense (US$) del Banco Central de Venezuela. La tasa actual es de
								<span class="text-primary font-medium">1 USD = 500 Bs</span>
							</p>
							<BaseButton
								class="mt-auto"
								text="¡Procesar pago!"
								@click="processPayment"
								:loading="salesStore.loading"
							/>
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
								¡Venta completada!
							</h2>
							<p class="">La venta ha sido procesada y registrada en Biyuyo con éxito.</p>
							<hr class="w-full" />
							<BaseCard variant="outlined">
								<div class="flex flex-col justify-center items-start gap-2">
									<h2 class="text-xl font-semibold text-primary">ID. de Transacción</h2>
									<p class="text-2xl font-bold">#{{ saleId }}</p>
								</div>
							</BaseCard>
						</div>
					</BaseCard>
					<BaseCard variant="secondary" class="col-span-full order-2 lg:col-span-3 lg:row-span-1">
						<div class="flex flex-col justify-center items-start gap-2">
							<h2 class="text-xl font-semibold text-white">Monto total</h2>
							<p class="text-4xl font-bold text-primary">${{ cartTotalWithIva.toFixed(2) }}</p>
							<p class="font-medium">Bs. {{ (cartTotalWithIva * 500).toFixed(2) }}</p>
						</div>
					</BaseCard>
					<BaseCard variant="outlined" class="col-span-full order-3 lg:col-span-3 lg:row-span-2">
						<div class="flex flex-col justify-center items-center gap-4">
							<h2 class="text-lg font-semibold">Opciones</h2>
							<BaseButton text="Imprimir recibo" variant="outlined" />
							<BaseButton text="Guardar recibo" variant="outlined" />
							<BaseButton text="Enviar recibo" variant="outlined" />
							<hr class="w-full" />
							<BaseButton text="Nueva venta" @click="startNewSale" />
						</div>
					</BaseCard>
				</div>
			</article>
		</section>
	</section>
</template>