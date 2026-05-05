import { describe, it, expect } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import { mount } from '@vue/test-utils'
import App from '../App.vue'

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: '/', name: 'home', component: { template: '<div>Home</div>' } },
	],
})

describe('App', () => {
	it('mounts renders properly', () => {
		setActivePinia(createPinia())
		
		const wrapper = mount(App, {
			global: {
				plugins: [router],
			},
		})
		
		expect(wrapper.exists()).toBe(true)
	})
})