/**
 * @file: tools_base64.
 * @intro: base64加密解密工具.
 * @author: zzmhot.
 * @email: zzmhot@163.com.
 * @Date: 2017/5/9 13:45.
 * @Copyright(©) 2017 by zzmhot.
 *
 */

//存储前缀
import {base64_prefix} from 'common/config'

import base64 from 'js-base64'

export default new class Base64 {
  constructor() {
    this.prefix = base64_prefix
    this.base64 = base64.Base64
  }

  //base64加密
  encode(val) {
    return this.base64.encode(base64_prefix + val)
  }

  //base解密
  decode(val) {
    return this.base64.decode(base64_prefix + val)
  }
}
