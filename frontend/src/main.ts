import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import csrfToken from '@/utils/csrfToken'
import '@/styles.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

csrfToken().finally(() => {
	router.isReady().then(() => {
		app.mount('#app')
	})
})
