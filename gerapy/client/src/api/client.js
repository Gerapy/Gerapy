import fetch from 'common/fetch'
import {client} from 'common/uri'
export function index(params) {
  return fetch({
    url: client.index,
    method: 'get',
    params
  })
}
export function show(params) {
  return fetch({
    url: client.show,
    method: 'get',
    params
  })
}

export function update(params, data) {
  return fetch({
    url: client.update,
    method: 'post',
    params,
    data,
  })
}