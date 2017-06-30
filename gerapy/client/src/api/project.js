import fetch from 'common/fetch'
import {project} from 'common/uri'
export function index(params) {
  return fetch({
    url: project.index,
    method: 'get',
    params
  })
}
export function show(params) {
  return fetch({
    url: project.show,
    method: 'get',
    params
  })
}

export function update(params, data) {
  return fetch({
    url: project.update,
    method: 'post',
    params,
    data,
  })
}

export function projects(params) {
  return fetch({
    url: project.projects,
    method: 'get',
    params,
  })
}

export function listSpiders(params) {
  return fetch({
    url: project.listSpiders,
    method: 'get',
    params,
  })
}

export function startSpider(params) {
  return fetch({
    url: project.startSpider,
    method: 'get',
    params,
  })
}

export function listJobs(params) {
  return fetch({
    url: project.listJobs,
    method: 'get',
    params,
  })
}


export function getLog(params) {
  return fetch({
    url: project.getLog,
    method: 'get',
    params,
  })
}

export function cancelJob(params) {
  return fetch({
    url: project.cancelJob,
    method: 'get',
    params,
  })
}

export function projectTree(params) {
  return fetch({
    url: project.projectTree,
    method: 'get',
    params,
  })
}

export function projectFile(data) {
  return fetch({
    url: project.projectFile,
    method: 'post',
    data,
  })
}

export function projectFileUpdate(data) {
  return fetch({
    url: project.projectFileUpdate,
    method: 'post',
    data,
  })
}

export function projectFileDelete(data) {
  return fetch({
    url: project.projectFileDelete,
    method: 'post',
    data,
  })
}


