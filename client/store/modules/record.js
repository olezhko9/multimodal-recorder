const state = () => ({
  recordState: 'INACTIVE', // INACTIVE, ACTIVE, PAUSED, STOPPED
  researchRecords: [],
})

const getters = {}

const mutations = {
  SET_STATE(state, recordState) {
    state.recordState = recordState
  },

  SET_RECORDS(state, records) {
    state.researchRecords = records
  },

  REMOVE_RECORD(state, recordId) {
    state.researchRecords = state.researchRecords.filter(r => r._id !== recordId)
  },
}

const actions = {
  async startRecord({ commit }, { researchId }) {
    const res = await this.$axios.$post(`/research/${researchId}/record/start`, {})
    commit('SET_STATE', 'ACTIVE')

    return res
  },

  async stopRecord({ commit }) {
    const res = await this.$axios.$post(`/record/stop`, {})
    commit('SET_STATE', 'STOPPED')

    return res
  },

  async getResearchRecords({ commit }, { researchId }) {
    const res = await this.$axios.$get(`/research/${researchId}/record`)
    commit('SET_RECORDS', res)

    return res
  },

  async deleteRecord({ commit }, { recordId }) {
    const res = await this.$axios.$delete(`/record/${recordId}`)
    commit('REMOVE_RECORD', recordId)

    return res
  }
}

export default {
  state,
  getters,
  mutations,
  actions,
}
