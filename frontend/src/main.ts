import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ToastService from 'primevue/toastservice'

import App from './App.vue'
import router from './router'
import '@/styles.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ToastService)

router.isReady().then(() => {
	app.mount('#app')
})
