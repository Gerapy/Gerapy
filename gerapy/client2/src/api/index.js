import * as apiClient from './client'
import * as apiProject from './project'
import * as apiHome from './home'
import * as apiMonitor from './monitor'
import * as apiTask from './task'
import * as apiUtil from './util'
const apiObj = {
  apiClient,
  apiProject,
  apiHome,
  apiMonitor,
  apiTask,
  apiUtil,
}
const install = function (Vue) {
  if (install.installed) return
  install.installed = true
  Object.defineProperties(Vue.prototype, {
    $fetch: {
      get() {
        return apiObj
      }
    }
  })
}
export default {
  install
}
