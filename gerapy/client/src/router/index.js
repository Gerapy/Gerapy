/**
 * Created by zzmhot on 2017/3/23.
 *
 * 路由Map
 *
 * @author: zzmhot
 * @github: https://github.com/zzmhot
 * @email: zzmhot@163.com
 * @Date: 2017/3/23 18:30
 * @Copyright(©) 2017 by zzmhot.
 *
 */

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
//login
import loginComponent from 'pages/user/login'
//base table
import baseTableComponent from 'pages/table/base'
//sort table
import sortTableComponent from 'pages/table/sort'
//save table
import saveTableComponent from 'pages/table/save'

//bar charts
import barChartsComponent from 'pages/charts/bar'

import listTaskComponent from 'pages/task/list'
import saveTaskComponent from 'pages/task/save'
import listPatternComponent from 'pages/pattern/list'
import savePatternComponent from 'pages/pattern/save'
import updatePatternComponent from 'pages/pattern/update'

Vue.use(VueRouter)

//使用AMD方式加载
// component: resolve => require(['pages/home'], resolve),
const routes = [{
  path: '/404',
  name: 'notPage',
  component: noPageComponent
}, {
  path: '*',
  redirect: '/404'
}, {
  path: '/user/login',
  name: 'login',
  component: loginComponent
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
    path: '/table/base',
    name: 'tableBase',
    component: baseTableComponent,
    meta: {
      title: "基本表格",
      auth: true
    }
  }, {
    path: '/table/sort',
    name: 'tableSort',
    component: sortTableComponent,
    meta: {
      title: "排序表格",
      auth: true
    }
  }, {
    path: '/table/update/:id',
    name: 'tableUpdate',
    component: saveTableComponent,
    meta: {
      title: "数据修改",
      auth: true
    }
  }, {
    path: '/table/add',
    name: 'tableAdd',
    component: saveTableComponent,
    meta: {
      title: "添加数据",
      auth: true
    }
  }, {
    path: '/charts/bar',
    name: 'chartsBar',
    component: barChartsComponent,
    meta: {
      title: "柱状图表",
      auth: true
    }
  }, {
    path: '/task',
    name: 'tasksList',
    component: listTaskComponent,
    meta: {
      title: "所有任务",
      auth: true
    }
  }, {
  path: '/task/add',
    name: 'taskAdd',
    component: saveTaskComponent,
    meta: {
      title: "添加任务",
      auth: true
    }
  },{
    path: '/task/update/:id',
    name: 'taskUpdate',
    component: saveTaskComponent,
    meta: {
      title: "任务修改",
      auth: true
    }
  }, {
    path: '/pattern',
    name: 'patternList',
    component: listPatternComponent,
    meta: {
      title: "所有规则",
      auth: true
    }
  }, {
    path: '/pattern/add',
    name: 'patternAdd',
    component: savePatternComponent,
    meta: {
      title: "添加规则",
      auth: true
    }
  }, {
    path: '/pattern/update/:id',
    name: 'patternUpdate',
    component: updatePatternComponent,
    meta: {
      title: "修改规则",
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

//全局路由配置
//路由开始之前的操作
// router.beforeEach((to, from, next) => {
//   NProgress.done().start()
  // let toName = to.name
  // // let fromName = from.name
  // let is_login = store.state.user_info.login
  //
  // if (!is_login && toName !== 'login') {
  //   next({
  //     name: 'login'
  //   })
  // } else {
  //   if (is_login && toName === 'login') {
  //     next({
  //       path: '/'
  //     })
  //   } else {
  //     next()
  //   }
  // }
// })

//路由完成之后的操作
router.afterEach(route => {
  NProgress.done()
})

export default router
