import Vue from 'vue'
import VueRouter from 'vue-router'
import store from 'store'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
//import components
//view page warp component
import viewPageComponent from 'pages/App'
//home
import homeComponent from 'pages/home'
//404
import noPageComponent from 'pages/error/404'
//client
import clientIndexComponent from 'pages/client/index'
import clientEditComponent from 'pages/client/edit'
Vue.use(VueRouter)

const routes = [{
  path: '/404',
  name: 'notPage',
  component: noPageComponent
}, {
  path: '*',
  redirect: '/404'
}, {
  path: '/',
  redirect: '/home',
  component: viewPageComponent,
  children: [{
    path: '/home',
    name: 'home',
    component: homeComponent,
    meta: {
      title: "主页",
      auth: true
    }
  }, {
    path: '/client',
    name: 'clientIndex',
    component: clientIndexComponent,
    meta: {
      title: "主机管理",
      auth: false
    }
  },{
    path: '/client/:id',
    name: 'clientEdit',
    component: clientEditComponent,
    meta: {
      title: "修改主机",
      auth: true
    }
  }]
}]
const router = new VueRouter({
  routes,
  mode: 'hash', //default: hash ,history
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return {x: 0, y: 0}
    }
  }
})
//路由完成之后的操作
router.afterEach(route => {
  NProgress.done()
})
export default router
