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
import clientCreateComponent from 'pages/client/create'
import clientScheduleComponent from 'pages/client/schedule'
// project
import projectIndexComponent from 'pages/project/index'
import projectEditComponent from 'pages/project/edit'
import projectConfigureComponent from 'pages/project/configure'
import projectDeployComponent from 'pages/project/deploy'
// task
import taskIndexComponent from 'pages/task/index'
import taskCreateComponent from 'pages/task/create'
import taskEditComponent from 'pages/task/edit'
import taskStatusComponent from 'pages/task/status'


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
  }, {
    path: '/client/create',
    name: 'clientCreate',
    component: clientCreateComponent,
    meta: {
      title: "新增主机",
      auth: true
    }
  }, {
    path: '/client/:id',
    name: 'clientEdit',
    component: clientEditComponent,
    meta: {
      title: "修改主机",
      auth: true
    }
  }, {
    path: '/client/:id/schedule',
    name: 'clientSchedule',
    component: clientScheduleComponent,
    meta: {
      title: "调度主机",
      auth: true
    }
  }, {
    path: '/project',
    name: 'projectIndex',
    component: projectIndexComponent,
    meta: {
      title: "项目管理",
      auth: false
    }
  }, {
    path: '/project/:name/edit',
    name: 'projectEdit',
    component: projectEditComponent,
    meta: {
      title: "项目编辑",
      auth: true
    }
  }, {
    path: '/project/:name/configure',
    name: 'projectConfigure',
    component: projectConfigureComponent,
    meta: {
      title: "项目配置",
      auth: true
    }
  }, {
    path: '/project/:name/deploy',
    name: 'projectDeploy',
    component: projectDeployComponent,
    meta: {
      title: "项目部署",
      auth: true
    }
  }, {
    path: '/task',
    name: 'taskIndex',
    component: taskIndexComponent,
    meta: {
      title: "任务管理",
      auth: false
    }
  }, {
    path: '/task/create',
    name: 'taskCreate',
    component: taskCreateComponent,
    meta: {
      title: "任务添加",
      auth: false
    }
  }, {
    path: '/task/:id/edit',
    name: 'taskEdit',
    component: taskEditComponent,
    meta: {
      title: "任务编辑",
      auth: true
    }
  }, {
    path: '/task/:id/status',
    name: 'taskStatus',
    component: taskStatusComponent,
    meta: {
      title: "任务状态",
      auth: true
    }
  }]
}]
const router = new VueRouter({
  routes,
  mode: 'hash', //default: hash ,history
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return {x: 0, y: 0}
    }
  }
})

//路由完成之后的操作
router.afterEach(() => {
  console.log('Clear')
  router.app.$store.dispatch('clearIntervals')
  router.app.$store.dispatch('clearTimeout')
})
export default router
