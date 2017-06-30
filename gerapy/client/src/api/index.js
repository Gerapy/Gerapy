import * as apiClient from './client'
import * as apiProject from './project'
const apiObj = {
  apiClient,
  apiProject
}
const install = function(Vue) {
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
