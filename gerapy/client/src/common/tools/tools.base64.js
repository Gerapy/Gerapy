

//存储前缀
import {base64Prefix} from 'common/config'

import base64 from 'js-base64'

export default new class Base64 {
  constructor() {
    this.prefix = base64Prefix
    this.base64 = base64.Base64
  }

  //base64加密
  encode(val) {
    return this.base64.encode(base64Prefix + val)
  }

  //base解密
  decode(val) {
    return this.base64.decode(base64Prefix + val)
  }
}
