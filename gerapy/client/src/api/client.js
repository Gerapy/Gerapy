import fetch from 'common/fetch'
import {client} from 'common/uri'
export function index(params) {
  return fetch({
    url: client.index,
    method: 'get',
    params
  })
}