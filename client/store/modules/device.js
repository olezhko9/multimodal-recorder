const state = () => ({
  devices: []
})

const getters = {}

const mutations = {
  SET_DEVICES(state, data) {
    state.devices = data
  },
}

const actions = {
  async getDevices({ commit },) {
    const res = await this.$axios.$get("/devices")
    commit('SET_DEVICES', res)

    return res
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
