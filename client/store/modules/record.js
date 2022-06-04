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

  SET_DIRECTORY_TREE(state, { recordId, tree }) {
    state.researchRecords = state.researchRecords.map(record => {
      if (record._id === recordId) {
        return { ...record, tree }
      }
      return record
    })
  }
}

const actions = {
  async startRecord({ commit }, { researchId, subjectId }) {
    const res = await this.$axios.$post(`/record/start`, {
      research_id: researchId,
      subject_id: subjectId,
    })
    commit('SET_STATE', 'ACTIVE')

    return res
  },

  async stopRecord({ commit }) {
    const res = await this.$axios.$post(`/record/stop`, {})
    commit('SET_STATE', 'STOPPED')

    return res
  },

  async getResearchRecords({ commit }, { researchId, subjectId }) {
    const res = await this.$axios.$get(`/research/${researchId}/subject/${subjectId}/record`)
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
