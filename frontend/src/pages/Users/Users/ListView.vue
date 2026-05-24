<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import EmptyState from '@/components/ui/EmptyState.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const search = ref('')
const showDeleteAlert = ref(false)
const userToDelete = ref<number | null>(null)

onMounted(() => {
	search.value = (route.query.search as string) || ''
	fetchUsers()
})

const fetchUsers = () => {
	const params: {
		search?: string
		ordering?: string
		page?: string
	} = {}

	if (search.value) params.search = search.value
	if (route.query.ordering) params.ordering = route.query.ordering as string
	if (route.query.page) params.page = route.query.page as string

	authStore.fetchUsers(params)
}

watch(search, () => {
	const query: Record<string, string> = {}
	if (search.value) query.search = search.value
	router.push({ query })
})

const confirmDelete = (id: number) => {
	userToDelete.value = id
	showDeleteAlert.value = true
}

const handleDelete = async () => {
	if (userToDelete.value) {
		await authStore.deleteUser(userToDelete.value)
		showDeleteAlert.value = false
		userToDelete.value = null
	}
}

const cancelDelete = () => {
	showDeleteAlert.value = false
	userToDelete.value = null
}

const formatDate = (dateString: string) => {
	if (!dateString) return '-'
	const date = new Date(dateString)
	return date.toLocaleDateString('es-VE', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric',
	})
}
</script>

<template>
	<section class="w-full flex flex-col gap-8 mx-8 justify-start items-start self-start">
		<div>
			<h1 class="text-primary text-2xl font-bold">Usuarios</h1>
			<p>Administra y controla los usuarios de tu negocio</p>
		</div>

		<div class="grid grid-cols-12 grid-rows-1 gap-4 w-full">
			<BaseButton to="/users/add" text="Añadir usuario" class="col-span-12 lg:col-span-3" />
			<BaseInput v-model="search" placeholder="Buscar usuario por nombre o email" class="col-span-12 lg:col-span-9" />
		</div>

		<div v-if="authStore.loading" class="w-full text-center py-8">
			<p>Cargando usuarios...</p>
		</div>

		<div v-else-if="authStore.users.length === 0" class="w-full">
			<EmptyState
				icon="fa-solid fa-users"
				title="No hay usuarios"
				description="Aún no se han registrado usuarios en el sistema. ¡Agrega el primer usuario para comenzar!"
				actionText="Añadir usuario"
				actionLink="/users/add"
			/>
		</div>

		<div v-else class="w-full">
			<BaseCard variant="outlined" class="col-span-12">
				<h2 class="text-primary font-semibold text-xl mb-8">Usuarios del negocio</h2>
				<table class="min-w-full divide-y-2 divide-gray-200">
					<thead class="ltr:text-left rtl:text-right">
						<tr class="*:font-medium *:text-gray-900">
							<th class="px-4 py-2 whitespace-nowrap">Nombre</th>
							<th class="px-4 py-2 whitespace-nowrap">Email</th>
							<th class="px-4 py-2 whitespace-nowrap">Teléfono</th>
							<th class="px-4 py-2 whitespace-nowrap">Cédula</th>
							<th class="px-4 py-2 whitespace-nowrap">Rol</th>
							<th class="px-4 py-2 whitespace-nowrap">Desde</th>
							<th class="px-4 py-2 whitespace-nowrap text-right">Acciones</th>
						</tr>
					</thead>

					<tbody class="divide-y divide-gray-200 *:even:bg-gray-50">
						<tr v-for="user in authStore.users" :key="user.id" class="*:text-gray-900 *:first:font-medium">
							<td class="px-4 py-2 whitespace-nowrap">{{ user.first_name }} {{ user.last_name }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ user.email }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ user.phone }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ user.identification_number }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ user.role || 'Usuario' }}</td>
							<td class="px-4 py-2 whitespace-nowrap">{{ formatDate(user.created_at) }}</td>
							<td class="px-4 py-2 whitespace-nowrap flex justify-end items-center gap-2">
								<BaseButton :to="'/users/edit/' + user.id" text="Editar" variant="secondary" width="auto" />
								<BaseButton text="Eliminar" width="auto" @click="confirmDelete(user.id)" />
							</td>
						</tr>
					</tbody>
				</table>
			</BaseCard>
		</div>
	</section>
</template>