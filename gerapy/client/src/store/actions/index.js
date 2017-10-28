export default {
  setTimeout: ({commit}, timeout) => {
    commit('setTimeout', timeout)
  },
  clearTimeout: ({commit}) => {
    commit('clearTimeout')
  },
  addInterval: ({commit}, interval) => {
    commit('addInterval', interval)
  },
  clearIntervals: ({commit}) => {
    commit('clearIntervals')
  },
  setLang: ({commit}, lang) => {
    commit('setLang', lang)
  },
}
