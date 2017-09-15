export default {
  setTimeout: (state, timeout) => {
    if (state.timeout) {
      clearTimeout(state.timeout)
    }
    state.timeout = timeout
  },
  clearTimeout: (state) => {
    clearTimeout(state.timeout)
  }
}
