import fetch from 'common/fetch'
import {task} from 'common/uri'

export function index(params) {
  return fetch({
    url: task.index,
    method: 'get',
    params,
  })
}
