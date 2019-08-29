import fetch from 'common/fetch'
import {task} from 'common/uri'

export function index(params) {
  return fetch({
    url: task.index,
    method: 'get',
    params,
  })
}

export function create(data) {
  return fetch({
    url: task.create,
    method: 'post',
    data,
  })
}

export function info(params) {
  return fetch({
    url: task.info,
    method: 'get',
    params
  })
}


export function status(params) {
  return fetch({
    url: task.status,
    method: 'get',
    params
  })
}

export function update(params, data) {
  return fetch({
    url: task.update,
    method: 'post',
    params,
    data,
  })
}

export function remove(params) {
  return fetch({
    url: task.remove,
    method: 'post',
    params,
  })
}
