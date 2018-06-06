import fetch from 'common/fetch'
import {home} from 'common/uri'
export function status(params) {
  return fetch({
    url: home.status,
    method: 'get',
    params
  })
}
