import axios from 'axios'
import {Message} from 'element-ui'
export default function fetch(options) {
  return new Promise((resolve, reject) => {
    //创建一个axios实例
    const instance = axios.create({
      //设置默认根地址
      baseURL: '/',
      //设置请求超时设置
      timeout: 2000,
      //设置请求时的header
      headers: {
        'Content-Type': 'application/json',
      }
    })
    if (options.method == 'get') {
      let params = options.params
      let url = options.url
      for (let key in params) {
        url = url.replace(':' + key, params[key])
      }
      options.url = url
      delete options.params
    }
    //请求处理
    instance(options)
      .then((data) => {
        //请求成功时,根据业务判断状态
        resolve(data);
      })
      .catch((error) => {
        //请求失败时,根据业务判断状态
        if (error.response) {
          let resError = error.response
          let resCode = resError.status
          let resMsg = error.message
          Message.error('操作失败！错误原因 ' + resMsg)
          reject({code: resCode, msg: resMsg})
        }
      })
  })
}
