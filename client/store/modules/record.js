const state = () => ({
  recordState: 'INACTIVE', // INACTIVE, ACTIVE, PAUSED, STOPPED
})

const getters = {}

const mutations = {
  SET_STATE(state, recordState) {
    state.recordState = recordState
  },
}

const actions = {
  async startRecord({ commit }) {
    const res = await this.$axios.$post("/record/start", {})
    if (res === true) {
      commit('SET_STATE', 'ACTIVE')
    }
    return res
  },

  async stopRecord({ commit }) {
    const res = await this.$axios.$post("/record/stop", {})
    if (res === true) {
      commit('SET_STATE', 'STOPPED')
    }
    return res
  }
}

export default {
  state,
  getters,
  mutations,
  actions,
}
