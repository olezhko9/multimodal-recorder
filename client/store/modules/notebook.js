const state = () => ({
  notebooks: [],
})

const getters = {
  // researchById: state => researchId => {
  //   return state.researches.find(r => r._id === researchId)
  // }
}

const mutations = {
  SET_NOTEBOOKS(state, data) {
    state.notebooks = data
  }
}

const actions = {
  async getNotebooks({ commit },) {
    const res = await this.$axios.$get("/notebook")
    commit('SET_NOTEBOOKS', res)

    return res
  },

  async runNotebook(context, { notebook, dataPath, recordId }) {
    return this.$axios.$post('/notebook/run', {
      record_id: recordId,
      notebook,
      data_path: dataPath,
    })
  }
}

export default {
  state,
  getters,
  mutations,
  actions,
}
