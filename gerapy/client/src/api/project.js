import fetch from 'common/fetch'
import {project} from 'common/uri'

export function projects(params) {
  return fetch({
    url: project.projects,
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

export function projectFileRead(data) {
  return fetch({
    url: project.projectFileRead,
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

export function projectFileCreate(data) {
  return fetch({
    url: project.projectFileCreate,
    method: 'post',
    data,
  })
}

export function projectFileRename(data) {
  return fetch({
    url: project.projectFileRename,
    method: 'post',
    data,
  })
}

export function projectList() {
  return fetch({
    url: project.projectList,
    method: 'get',
  })
}

export function projectRemove(params) {
  return fetch({
    url: project.projectRemove,
    method: 'post',
    params
  })
}

export function buildInfo(params) {
  return fetch({
    url: project.buildInfo,
    method: 'get',
    params
  })
}

export function build(params, data) {
  return fetch({
    url: project.build,
    method: 'post',
    params,
    data
  })
}

export function projectGetConfiguration(params) {
  return fetch({
    url: project.projectConfigure,
    method: 'get',
    params,
  })
}

export function projectSaveConfiguration(params, data) {
  return fetch({
    url: project.projectConfigure,
    method: 'post',
    params,
    data
  })
}

export function projectCreate(data) {
  return fetch({
    url: project.projectCreate,
    method: 'post',
    data,
  })
}

export function projectGenerate(params) {
  return fetch({
    url: project.projectGenerate,
    method: 'post',
    params,
  })
}

export function projectParse(params, data) {
  return fetch({
    url: project.projectParse,
    method: 'post',
    params,
    data
  })
}
