const state = () => ({
  researches: []
})

const getters = {}

const mutations = {
  SET_RESEARCHES(state, data) {
    state.researches = data
  },

  REMOVE_RESEARCH(state, researchId) {
    state.researches = state.researches.filter(r => r._id !== researchId)
  }
}

const actions = {
  async getResearches({ commit },) {
    const res = await this.$axios.$get("/research")
    commit('SET_RESEARCHES', res)

    return res
  },

  async deleteResearch({ commit }, { id }) {
    const res = await this.$axios.$delete(`/research/${id}`)
    commit('REMOVE_RESEARCH', id)

    return res
  }
}

export default {
  state,
  getters,
  mutations,
  actions,
}
