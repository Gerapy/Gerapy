import fetch from 'common/fetch'
import {monitor} from 'common/uri'
export function index(params) {
  return fetch({
    url: monitor.index,
    method: 'get',
    params
  })
}

export function create(data) {
  return fetch({
    url: monitor.create,
    method: 'post',
    data
  })
}

export function getDBList(data) {
  return fetch({
    url: monitor.getDBList,
    method: 'post',
    data
  })
}


export function getCollectionList(data) {
  return fetch({
    url: monitor.getCollectionList,
    method: 'post',
    data
  })
}
