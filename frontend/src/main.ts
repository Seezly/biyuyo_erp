import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import '@/styles.css'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(router)

const initApp = async () => {
	const auth = useAuthStore()

	await auth.fetchUser()

	app.mount('#app')
}

initApp()
