import fetch from 'common/fetch'
import {util} from 'common/uri'

export function render(data) {
  return fetch({
    url: util.render,
    method: 'post',
    data
  })
}
