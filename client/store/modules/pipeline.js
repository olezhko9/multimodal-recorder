const state = () => ({
  allMethods: [],
})

const getters = {}

const mutations = {
  SET_METHODS(state, data) {
    state.allMethods = data
  }
}

const actions = {
  async getMethods({ commit },) {
    const res = await this.$axios.$get('/pipeline/methods')
    commit('SET_METHODS', res)

    return res
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
