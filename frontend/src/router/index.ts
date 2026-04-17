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
			meta: { requiresAuth: false },
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
				{
					path: 'reminders',
					name: 'Reminders',
					component: () => import('@/pages/Users/Profile/RemindersView.vue'),
				},
			],
		},
		{
			path: '/sales',
			meta: { requiresAuth: true },
			children: [
				{
					path: '',
					name: 'Sales',
					component: () => import('@/pages/Sale/Sales/ShowView.vue'),
				},
				{
					path: 'pos',
					name: 'POS',
					component: () => import('@/pages/Sale/Sales/CreateView.vue'),
				},
			],
		},
		{
			path: '/inventory',
			meta: { requiresAuth: true },
			children: [
				{
					path: '',
					name: 'Inventory',
					component: () => import('@/pages/Inventory/Inventory/ShowView.vue'),
				},
			],
		},
		{
			path: '/reports',
			meta: { requiresAuth: true },
			children: [
				{
					path: '',
					name: 'Reports',
					component: () => import('@/pages/Reports/ReportsView.vue'),
				},
				{
					path: ':reportType',
					name: 'CustomReport',
					component: () => import('@/pages/Reports/CustomReportView.vue'),
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
