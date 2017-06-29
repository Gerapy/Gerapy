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

export function projects(params) {
  return fetch({
    url: client.projects,
    method: 'get',
    params,
  })
}

export function listSpiders(params) {
  return fetch({
    url: client.listSpiders,
    method: 'get',
    params,
  })
}

export function startSpider(params) {
  return fetch({
    url: client.startSpider,
    method: 'post',
    params,
  })
}

export function listJobs(params) {
  return fetch({
    url: client.listJobs,
    method: 'get',
    params,
  })
}

