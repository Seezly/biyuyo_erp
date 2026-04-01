import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/login',
			name: 'Login',
			component: () => import('@/pages/Auth/LoginView.vue'),
		},
		{
			path: '/register',
			name: 'Register',
			component: () => import('@/pages/Auth/RegisterView.vue'),
		},
	],
})

export default router
