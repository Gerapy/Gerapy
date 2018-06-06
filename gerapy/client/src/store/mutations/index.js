export default {
  setTimeout: (state, timeout) => {
    if (state.timeout) {
      clearTimeout(state.timeout)
    }
    state.timeout = timeout
  },
  clearTimeout: (state) => {
    clearTimeout(state.timeout)
  },
  addInterval: (state, interval) => {
    state.intervals.push(interval)
  },
  clearIntervals: (state) => {
    state.intervals.forEach(interval => {
      clearInterval(interval)
    })
    state.intervals = []
  },
  setLang: (state, lang) => {
    state.lang = lang
  }
}
