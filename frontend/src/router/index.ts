import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
	linkActiveClass: 'text-primary font-bold',
	linkExactActiveClass: 'border border-primary rounded-full py-2 px-4 text-primary font-bold',
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
				{
					path: 'reminders',
					name: 'Reminders',
					component: () => import('@/pages/Users/Profile/RemindersView.vue'),
				},
			],
		},
		{
			path: '/users',
			meta: { requiresAuth: true },
			children: [
				{
					path: '',
					name: 'Users',
					component: () => import('@/pages/Users/Users/ListView.vue'),
				},
				{
					path: 'add',
					name: 'AddUser',
					component: () => import('@/pages/Users/Users/CreateView.vue'),
				},
				{
					path: 'edit/:userId',
					name: 'EditUser',
					component: () => import('@/pages/Users/Users/EditView.vue'),
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
				{
					path: 'all',
					name: 'ListSales',
					component: () => import('@/pages/Sale/Sales/ListView.vue'),
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
				{
					path: 'all',
					name: 'ListInventory',
					component: () => import('@/pages/Inventory/Products/ListView.vue'),
				},
				{
					path: 'products',
					name: 'Products',
					children: [
						{
							path: 'add',
							name: 'AddProduct',
							component: () => import('@/pages/Inventory/Products/CreateView.vue'),
						},
						{
							path: 'edit/:productId',
							name: 'EditProduct',
							component: () => import('@/pages/Inventory/Products/EditView.vue'),
						},
					],
				},
				{
					path: 'categories',
					children: [
						{
							path: '',
							name: 'Categories',
							component: () => import('@/pages/Inventory/Categories/ListView.vue'),
						},
						{
							path: 'add',
							name: 'AddCategory',
							component: () => import('@/pages/Inventory/Categories/CreateView.vue'),
						},
						{
							path: 'edit/:categoryId',
							name: 'EditCategory',
							component: () => import('@/pages/Inventory/Categories/EditView.vue'),
						},
					],
				},
			],
		},
		{
			path: '/suppliers',
			meta: { requiresAuth: true },
			children: [
				{
					path: '',
					name: 'Suppliers',
					component: () => import('@/pages/Suppliers/Suppliers/ListView.vue'),
				},
				{
					path: 'add',
					name: 'AddSupplier',
					component: () => import('@/pages/Suppliers/Suppliers/CreateView.vue'),
				},
				{
					path: 'edit/:supplierId',
					name: 'EditSupplier',
					component: () => import('@/pages/Suppliers/Suppliers/EditView.vue'),
				},
				{
					path: 'purchases',
					children: [
						{
							path: '',
							name: 'Purchases',
							component: () => import('@/pages/Suppliers/Purchases/ListView.vue'),
						},
						{
							path: 'add',
							name: 'AddPurchase',
							component: () => import('@/pages/Suppliers/Purchases/CreateView.vue'),
						},
						{
							path: 'edit/:purchaseId',
							name: 'EditPurchase',
							component: () => import('@/pages/Suppliers/Purchases/EditView.vue'),
						},
					],
				},
			],
		},
		{
			path: '/customers',
			meta: { requiresAuth: true },
			children: [
				{
					path: '',
					name: 'Customers',
					component: () => import('@/pages/Customers/ListView.vue'),
				},
				{
					path: 'add',
					name: 'AddCustomer',
					component: () => import('@/pages/Customers/CreateView.vue'),
				},
				{
					path: 'edit/:customerId',
					name: 'EditCustomer',
					component: () => import('@/pages/Customers/EditView.vue'),
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
