import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/login',
			name: 'Login',
			component: () => import('@/pages/Auth/LoginView.vue'),
			meta: { requiresAuth: true },
		},
		{
			path: '/register',
			name: 'Register',
			component: () => import('@/pages/Auth/RegisterView.vue'),
			meta: { guestOnly: true },
		},
	],
})

router.beforeEach((to, from, next) => {
	const auth = useAuthStore()

	if (to.meta.requiresAuth && !auth.isAuthenticated) {
		return next('/login')
	}

	if (to.meta.guestOnly && auth.isAuthenticated) {
		return next('/dashboard')
	}

	next()
})

export default router
