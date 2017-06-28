import * as apiClient from './client'
const apiObj = {
  apiClient,
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
