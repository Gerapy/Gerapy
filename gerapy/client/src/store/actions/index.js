export default {
  setTimeout: ({commit}, timeout) => {
    commit('setTimeout', timeout)
  },
  clearTimeout: ({commit}) => {
    commit('clearTimeout')
  }
}
