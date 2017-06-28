/**
 * @file: index.
 * @intro: Storage工具类.
 * @author: zzmhot.
 * @email: zzmhot@163.com.
 * @Date: 2017/4/27 15:28.
 * @Copyright(©) 2017 by zzmhot.
 *
 */

//存储前缀
import {storage_prefix} from 'common/config'

import {tools_verify, tools_uri} from 'common/tools'

class Storage {

  constructor(type) {
    if (type === 'local') {
      this.store = window.localStorage
    } else if (type === 'session') {
      this.store = window.sessionStorage
    }
    this.prefix = storage_prefix
  }

  set(key, value) {
    try {
      value = JSON.stringify(value)
    } catch (e) {
      value = value
    }

    this.store.setItem(tools_uri.encode(this.prefix + key), tools_uri.encode(value))

    return this
  }

  get(key) {
    if (!key) {
      throw new Error('没有找到key。')
      return
    }
    if (typeof key === 'object') {
      throw new Error('key不能是一个对象。')
      return
    }
    let value = this.store.getItem(tools_uri.encode(this.prefix + key))

    if (value === null) {
      return {}
    }

    try {
      value = JSON.parse(tools_uri.decode(value))
    } catch (e) {
      value = {}
    }
    return value
  }

  remove(key) {
    this.store.removeItem(tools_uri.encode(this.prefix + key))
    return this
  }
}

export const localStorage = new Storage('local')
export const sessionStorage = new Storage('session')
