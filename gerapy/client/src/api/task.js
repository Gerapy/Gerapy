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
