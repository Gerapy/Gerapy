
import * as actions from 'store/actions/type'
import * as mutations from 'store/mutations/type'

export default {
  //设置用户信息和登录
  [actions.SET_USER_INFO]({commit}, userinfo){
    commit(mutations.SET_USER_INFO, userinfo)
  }
}
