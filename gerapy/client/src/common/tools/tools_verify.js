/**
 * @file: tools_verify.
 * @intro: 常用验证工具类.
 * @author: zzmhot.
 * @email: zzmhot@163.com.
 * @Date: 2017/5/9 13:45.
 * @Copyright(©) 2017 by zzmhot.
 *
 */

import {phone} from './regex'

export default new class Verify {
  constructor() {
  }

  //验证url是否正确，true/false
  isUrl(url) {
    return (/(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/i).test(url)
  }

  //验证手机号码是否正确， true/false
  isTel(tel) {
    return (phone).test(tel)
  }

  //判断是否是object对象
  isObject(value) {
    return !!value && Object.prototype.toString.call(value) === '[object Object]';
  }

  //判断是否是数组
  isArray(value) {
    return Object.prototype.toString.call(value) === '[object Array]';
  }
}
