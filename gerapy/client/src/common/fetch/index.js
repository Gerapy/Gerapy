import axios from 'axios'
import {Message} from 'element-ui'
export default function fetch(options) {

  return new Promise((resolve, reject) => {
    //创建一个axios实例
    const instance = axios.create({
      //设置默认根地址
      baseURL: '/',
      //设置请求超时设置
      timeout: 10000,
      //设置请求时的header
      headers: {
        'Content-Type': 'application/json',
      }
    })
    if (options.params) {
      console.log(options.params)
      let params = options.params
      let url = options.url
      for (let key in params) {
        url = url.replace(':' + key, params[key])
      }
      options.url = url
      delete options.params
    }
    console.log(options)
    instance(options)
      .then((data) => {
        resolve(data);
      })
      .catch((error) => {
        reject(error)
      })
  })
}
