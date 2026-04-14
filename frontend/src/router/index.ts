import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/login',
			name: 'Login',
			component: () => import('@/pages/Auth/LoginView.vue'),
			meta: { guestOnly: true },
		},
		{
			path: '/register',
			name: 'Register',
			component: () => import('@/pages/Auth/RegisterView.vue'),
			meta: { guestOnly: true },
		},
		{
			path: '/dashboard',
			name: 'Dashboard',
			component: () => import('@/pages/DashboardView.vue'),
			meta: { requiresAuth: true },
		},
		{
			path: '/profile',
			meta: { requiresAuth: true },
			children: [
				{
					path: '',
					name: 'Profile',
					component: () => import('@/pages/Users/Profile/ProfileView.vue'),
				},
				{
					path: 'change-password',
					name: 'ChangePassword',
					component: () => import('@/pages/Users/Profile/ChangePasswordView.vue'),
				},
				{
					path: 'notifications',
					name: 'Notifications',
					component: () => import('@/pages/Users/Profile/NotificationsView.vue'),
				},
			],
		},
		{
			path: '/logout',
			name: 'Logout',
			component: () => import('@/pages/Auth/LogoutView.vue'),
			meta: { guestOnly: true },
		},
	],
})

router.beforeEach(async (to, from, next) => {
	const auth = useAuthStore()

	if (auth.loading) {
		await auth.fetchUser()
	}

	const requiresAuth = to.matched.some((r) => r.meta.requiresAuth)
	const guestOnly = to.matched.some((r) => r.meta.guestOnly)

	if (requiresAuth && !auth.isAuthenticated) {
		return next('/login')
	}

	if (guestOnly && auth.isAuthenticated) {
		return next('/dashboard')
	}

	next()
})

export default router
