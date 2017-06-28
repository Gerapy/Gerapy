

export default new class Uri {
  constructor() {
  }

  //URI 解码
  decode(value) {
    return decodeURIComponent(value)
  }

  //URI 编码
  encode(value) {
    return encodeURIComponent(value)
  }
}
