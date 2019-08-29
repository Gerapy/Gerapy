import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import './assets/scss/element.scss'
import './assets/scss/main.scss'
import store from './store'
import {mapGetters} from 'vuex'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(ElementUI)
Vue.use(VueAxios, axios)

Vue.config.productionTip = false

// 注册全局语言配置
Vue.mixin({
	computed: {
		...mapGetters(['$lang'])
	}
})

new Vue({
	router,
	store,
	render:
		h => h(App),
}).$mount('#app')
