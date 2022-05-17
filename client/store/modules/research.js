const state = () => ({
  researches: [],
})

const getters = {
  researchById: state => researchId => {
    return state.researches.find(r => r._id === researchId)
  }
}

const mutations = {
  SET_RESEARCHES(state, data) {
    state.researches = data
  },

  ADD_RESEARCH(state, research) {
    state.researches.push(research)
  },

  REMOVE_RESEARCH(state, researchId) {
    state.researches = state.researches.filter(r => r._id !== researchId)
  },
}

const actions = {
  async getResearches({ commit },) {
    const res = await this.$axios.$get("/research")
    commit('SET_RESEARCHES', res)

    return res
  },

  async createResearch({ commit }, research) {
    const res = await this.$axios.$post('/research', research)
    commit('ADD_RESEARCH', res)

    return res
  },

  async deleteResearch({ commit }, { id }) {
    const res = await this.$axios.$delete(`/research/${id}`)
    commit('REMOVE_RESEARCH', id)

    return res
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
