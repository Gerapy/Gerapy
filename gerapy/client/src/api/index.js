import * as apiClient from './client'
import * as apiProject from './project'
import * as apiHome from './home'
const apiObj = {
  apiClient,
  apiProject,
  apiHome
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
