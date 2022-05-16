const state = () => ({
  status: ''
})

const getters = {}

const mutations = {
  SET_STATUS(state, status) {
    state.status = status
  },
}

export default {
  state,
  getters,
  mutations,
}
