import fetch from 'common/fetch'
import {port_pattern} from 'common/port_uri'
//数据列表
export function list(params) {
  return fetch({
    url: port_pattern.list,
    method: 'get',
    params
  })
}
//添加或修改数据
export function save(data) {
  console.log(port_pattern.save)
  return fetch({
    url: port_pattern.save,
    method: 'post',
    data
  })
}
export function update(data) {
  console.log(port_pattern.save)
  return fetch({
    url: port_pattern.save + '/' + data['envTag'],
    method: 'put',
    data
  })
}
//根据id查询数据
export function get(params) {
  return fetch({
    url: port_pattern.get + '/' + params['envTag'],
    method: 'get',
  })
}
//根据id删除数据
export function del(data) {
  return fetch({
    url: port_pattern.del + '/' + data['envTag'],
    method: 'delete',
  })
}