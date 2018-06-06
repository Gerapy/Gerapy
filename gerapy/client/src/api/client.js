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

export function status(params) {
  return fetch({
    url: client.status,
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

export function remove(params) {
  return fetch({
    url: client.remove,
    method: 'post',
    params,
  })
}

export function create(data) {
  return fetch({
    url: client.create,
    method: 'post',
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
    method: 'get',
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


export function getLog(params) {
  return fetch({
    url: client.getLog,
    method: 'get',
    params,
  })
}

export function cancelJob(params) {
  return fetch({
    url: client.cancelJob,
    method: 'get',
    params,
  })
}

export function projectVersion(params) {
  return fetch({
    url: client.projectVersion,
    method: 'get',
    params,
  })
}

export function projectDeploy(params) {
  return fetch({
    url: client.projectDeploy,
    method: 'post',
    params,
  })
}
