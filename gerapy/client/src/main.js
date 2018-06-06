import 'normalize.css'
import 'font-awesome/scss/font-awesome.scss'
import 'element-ui/lib/theme-default/index.css'
import Vue from 'vue'
import '../theme/index.css'
import ElementUI from 'element-ui'
import router from './router'
import store from 'store'
import api from './api'
import lang from './lang'
import App from './App'
import VueCodeMirror from 'vue-codemirror'

Vue.use(ElementUI)

Vue.use(api)

Vue.use(lang)

Vue.use(VueCodeMirror)

Vue.config.productionTip = false

Vue.config.devtools = process.env.NODE_ENV === 'development'

new Vue({
  router,
  store,
  ...App
}).$mount('mainbody')
