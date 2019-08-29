import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import store from './store'

const router = new Router({
	// mode: 'history',
	routes: [
		{
			path: '/',
			name: 'home',
			component: () => import('./views/home/Index.vue')
		},
		/*
		{
			path: '/login',
			name: 'login',
			component: () => import('./views/Login.vue')
		},
		{
			path: '/config/:domain',
			component: () => import('./views/Base.vue'),
			children: [
				{
					path: '',
					name: 'configHome',
					component: () => import('./views/config/Home.vue')
				},
				{
					path: 'edit/:id',
					name: 'configEdit',
					component: () => import('./views/config/Edit.vue')
				}
			]
		},
		{
			path: '/media/:domain',
			component: () => import('./views/Base.vue'),
			children: [
				{
					path: '',
					name: 'mediaHome',
					component: () => import('./views/media/Home.vue')
				},
				{
					path: 'edit/:name',
					name: 'mediaEdit',
					component: () => import('./views/media/Edit.vue')
				}
			]
		},
		{
			path: '/detection/:domain',
			component: () => import('./views/Base.vue'),
			children: [
				{
					path: '',
					name: 'detectionHome',
					component: () => import('./views/detection/Home.vue')
				}
			]
		},
		{
			path: '/task/:domain',
			component: () => import('./views/Base.vue'),
			children: [
				{
					path: '',
					name: 'taskHome',
					component: () => import('./views/task/Home.vue')
				}
			]
		},
		{
			path: '/editor/:domain',
			component: () => import('./views/Base.vue'),
			children: [
				{
					path: '',
					name: 'editorHome',
					component: () => import('./views/editor/Home.vue')
				},
				{
					path: 'edit/:id',
					name: 'editorEdit',
					component: () => import('./views/editor/Edit.vue')
				}
			]
		},
		{
			path: '/script/:domain',
			component: () => import('./views/Base.vue'),
			children: [
				{
					path: '',
					name: 'scriptHome',
					component: () => import('./views/script/Home.vue')
				},
				{
					path: 'edit/:id',
					name: 'scriptEdit',
					component: () => import('./views/script/Edit.vue')
				}
			]
		}
		*/
	]
})

export default router