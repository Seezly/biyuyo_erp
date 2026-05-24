import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
	linkActiveClass: 'text-primary font-bold',
	linkExactActiveClass: 'border border-primary text-primary font-bold rounded-full',
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/login',
			name: 'Login',
			component: () => import('@/pages/Auth/LoginView.vue'),
			meta: { guestOnly: true, title: 'Iniciar Sesión' },
		},
		{
			path: '/register',
			name: 'Register',
			component: () => import('@/pages/Auth/RegisterView.vue'),
			meta: { guestOnly: true, title: 'Registrarse' },
		},
		{
			path: '/dashboard',
			name: 'Dashboard',
			component: () => import('@/pages/DashboardView.vue'),
			meta: { requiresAuth: true, title: 'Panel de Control' },
		},
		{
			path: '/profile',
			meta: { requiresAuth: true, title: 'Perfil' },
			children: [
				{
					path: '',
					name: 'Profile',
					component: () => import('@/pages/Users/Profile/ProfileView.vue'),
					meta: { title: 'Perfil' },
				},
				{
					path: 'change-password',
					name: 'ChangePassword',
					component: () => import('@/pages/Users/Profile/ChangePasswordView.vue'),
					meta: { title: 'Cambiar Contraseña' },
				},
				{
					path: 'notifications',
					name: 'Notifications',
					component: () => import('@/pages/Users/Profile/NotificationsView.vue'),
					meta: { title: 'Notificaciones' },
				},
				{
					path: 'reminders',
					name: 'Reminders',
					component: () => import('@/pages/Users/Profile/RemindersView.vue'),
					meta: { title: 'Recordatorios' },
				},
			],
		},
		{
			path: '/users',
			meta: { requiresAuth: true, adminOnly: true, title: 'Usuarios' },
			children: [
				{
					path: '',
					name: 'Users',
					component: () => import('@/pages/Users/Users/ListView.vue'),
					meta: { title: 'Lista de Usuarios' },
				},
				{
					path: 'add',
					name: 'AddUser',
					component: () => import('@/pages/Users/Users/CreateView.vue'),
					meta: { title: 'Crear Usuario' },
				},
				{
					path: 'edit/:userId',
					name: 'EditUser',
					component: () => import('@/pages/Users/Users/EditView.vue'),
					meta: { title: 'Editar Usuario' },
				},
			],
		},
		{
			path: '/sales',
			meta: { requiresAuth: true, title: 'Ventas' },
			children: [
				{
					path: '',
					name: 'Sales',
					component: () => import('@/pages/Sale/Sales/ShowView.vue'),
					meta: { title: 'Resumen de Ventas' },
				},
				{
					path: 'pos',
					name: 'POS',
					component: () => import('@/pages/Sale/Sales/CreateView.vue'),
					meta: { title: 'Punto de Venta' },
				},
				{
					path: 'all',
					name: 'ListSales',
					component: () => import('@/pages/Sale/Sales/ListView.vue'),
					meta: { title: 'Lista de Ventas' },
				},
			],
		},
		{
			path: '/inventory',
			meta: { requiresAuth: true, title: 'Inventario' },
			children: [
				{
					path: '',
					name: 'Inventory',
					component: () => import('@/pages/Inventory/Inventory/ShowView.vue'),
					meta: { title: 'Resumen de Inventario' },
				},
				{
					path: 'all',
					name: 'ListInventory',
					component: () => import('@/pages/Inventory/Products/ListView.vue'),
					meta: { title: 'Lista de Productos' },
				},
				{
					path: 'products',
					name: 'Products',
					meta: { title: 'Productos' },
					children: [
						{
							path: 'add',
							name: 'AddProduct',
							component: () => import('@/pages/Inventory/Products/CreateView.vue'),
							meta: { title: 'Crear Producto' },
						},
						{
							path: 'edit/:productId',
							name: 'EditProduct',
							component: () => import('@/pages/Inventory/Products/EditView.vue'),
							meta: { title: 'Editar Producto' },
						},
					],
				},
				{
					path: 'categories',
					meta: { requiresAuth: true, title: 'Categorías' },
					children: [
						{
							path: '',
							name: 'Categories',
							component: () => import('@/pages/Inventory/Categories/ListView.vue'),
							meta: { title: 'Lista de Categorías' },
						},
						{
							path: 'add',
							name: 'AddCategory',
							component: () => import('@/pages/Inventory/Categories/CreateView.vue'),
							meta: { title: 'Crear Categoría' },
						},
						{
							path: 'edit/:categoryId',
							name: 'EditCategory',
							component: () => import('@/pages/Inventory/Categories/EditView.vue'),
							meta: { title: 'Editar Categoría' },
						},
					],
				},
			],
		},
		{
			path: '/suppliers',
			meta: { requiresAuth: true, title: 'Proveedores' },
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
			meta: { requiresAuth: true, title: 'Clientes' },
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
			meta: { requiresAuth: true, title: 'Reportes' },
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
			path: '/audit',
			meta: { requiresAuth: true, adminOnly: true, title: 'Auditoría' },
			children: [
				{
					path: '',
					name: 'AuditLogs',
					component: () => import('@/pages/audit/ListView.vue'),
					meta: { title: 'Registro de Auditoría' },
				},
				{
					path: ':id',
					name: 'AuditLogDetail',
					component: () => import('@/pages/audit/DetailView.vue'),
					meta: { title: 'Detalle de Auditoría' },
				},
			],
		},
		{
			path: '/admin',
			meta: { requiresAuth: true, adminOnly: true, title: 'Administración' },
			children: [
				{
					path: '',
					name: 'AdminDashboard',
					component: () => import('@/pages/Admin/DashboardView.vue'),
				},
				{
					path: 'statistics',
					name: 'AdminStatistics',
					component: () => import('@/pages/Admin/StatisticsView.vue'),
				},
				{
					path: 'settings',
					name: 'AdminSettings',
					component: () => import('@/pages/Admin/SettingsView.vue'),
				},
				{
					path: 'reports',
					name: 'AdminReports',
					component: () => import('@/pages/Admin/ReportsView.vue'),
				},
				{
					path: 'businesses',
					meta: { title: 'Negocios' },
					children: [
						{
							path: '',
							name: 'AdminBusinesses',
							component: () => import('@/pages/Businesses/ListView.vue'),
							meta: { title: 'Lista de Negocios' },
						},
						{
							path: 'add',
							name: 'AdminAddBusiness',
							component: () => import('@/pages/Businesses/CreateView.vue'),
							meta: { title: 'Crear Negocio' },
						},
						{
							path: 'edit/:businessId',
							name: 'AdminEditBusiness',
							component: () => import('@/pages/Businesses/EditView.vue'),
							meta: { title: 'Editar Negocio' },
						},
					],
				},
				{
					path: 'roles',
					meta: { title: 'Roles' },
					children: [
						{
							path: '',
							name: 'AdminRoles',
							component: () => import('@/pages/Roles/ListView.vue'),
							meta: { title: 'Lista de Roles' },
						},
						{
							path: 'add',
							name: 'AdminAddRole',
							component: () => import('@/pages/Roles/CreateView.vue'),
							meta: { title: 'Crear Rol' },
						},
						{
							path: 'edit/:roleId',
							name: 'AdminEditRole',
							component: () => import('@/pages/Roles/EditView.vue'),
							meta: { title: 'Editar Rol' },
						},
					],
				},
			],
		},
		{
			path: '/billing',
			meta: { requiresAuth: true, adminOnly: true, title: 'Facturación' },
			children: [
				{
					path: 'plans',
					name: 'Plans',
					component: () => import('@/pages/Billing/Plans/ListView.vue'),
				},
				{
					path: 'subscriptions',
					name: 'Subscriptions',
					component: () => import('@/pages/Billing/Subscriptions/ListView.vue'),
				},
				{
					path: 'invoices',
					name: 'Invoices',
					component: () => import('@/pages/Billing/Invoices/InvoicesView.vue'),
				},
			],
		},
		{
			path: '/logout',
			name: 'Logout',
			component: () => import('@/pages/Auth/LogoutView.vue'),
			meta: { guestOnly: true, title: 'Cerrar Sesión' },
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
	const adminOnly = to.matched.some((r) => r.meta.adminOnly)

	if (requiresAuth && auth.user?.role === 'admin' && !to.matched.some((r) => r.meta.adminOnly)) {
		return next('/admin')
	}

	if (requiresAuth && !auth.isAuthenticated) {
		return next('/login')
	}

	if (guestOnly && auth.isAuthenticated) {
		return next('/dashboard')
	}

	if (adminOnly && auth.user?.role !== 'admin') {
		return next('/dashboard')
	}

	document.title = to.matched.find((r) => r.meta.title)?.meta.title + ' | Biyuyo ERP' || 'Biyuyo ERP'

	next()
})

export default router
