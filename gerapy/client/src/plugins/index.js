
import dateFormat from 'plugins/date'

const install = function (Vue) {
  if (install.installed) return
  install.installed = true

  //定义属性到Vue原型中
  Object.defineProperties(Vue.prototype, {
    $dateFormat: {
      get() {
        return dateFormat
      }
    }
  })
}

export default {
  install
}
