import en from './en'
import zhCN from './zh-cn'


const langObj = {
  en,
  zhCN,
}
const install = function (Vue) {
  if (install.installed) return
  install.installed = true
  Object.defineProperties(Vue.prototype, {
    $lang: {
      get() {
        return langObj
      }
    }
  })
}

export default {
  install
}
