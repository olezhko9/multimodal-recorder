const state = () => ({
  subjects: [],
})

const getters = {
  subjectById: state => subjectId => {
    return state.subjects.find(s => s._id === subjectId)
  },

  subjectName: state => subjectId => {
    const subject = state.subjects.find(s => s._id === subjectId)
    if (subject) {
      if (subject.info && subject.info["Имя"])
        return subject.info["Имя"]
      else
        return subject._id
    }
    return ''
  },
}

const mutations = {
  SET_SUBJECTS(state, subjects) {
    state.subjects = subjects
  },

  REMOVE_SUBJECT(state, subjectId) {
    state.subjects = state.subjects.filter(r => r._id !== subjectId)
  },

  ADD_SUBJECT(state, subject) {
    state.subjects.push(subject)
  }
}

const actions = {
  async createSubject({ commit }, { researchId, ...subject }) {
    const res = await this.$axios.$post(`/research/${researchId}/subject`, {
      ...subject
    })
    commit('ADD_SUBJECT', res)

    return res
  },

  async getSubjects({ commit }, { researchId }) {
    const res = await this.$axios.$get(`/research/${researchId}/subject`)
    commit('SET_SUBJECTS', res)

    return res
  },

  async deleteSubject({ commit }, { subjectId }) {
    const res = await this.$axios.$delete(`/subject/${subjectId}`)
    commit('REMOVE_SUBJECT', subjectId)

    return res
  }
}

export default {
  state,
  getters,
  mutations,
  actions,
}
