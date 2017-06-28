import fetch from 'common/fetch'
import {port_task} from 'common/port_uri'

//数据列表
export function list(params) {
  return fetch({
    url: port_task.list,
    method: 'get',
    params
  })
}

//添加或修改数据
export function save(data) {
  return fetch({
    url: port_task.save,
    method: 'post',
    data
  })
}

export function cancel(row) {
  return fetch({
    url: port_task.change_status + '/' + row.id + '/status',
    method: 'post',
    data: '"Canceled"'
  })
}
