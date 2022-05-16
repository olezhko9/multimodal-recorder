const state = () => ({
  devices: [],
  startedDevices: []
})

const getters = {
  isDeviceStarted: state => deviceId => {
    return state.startedDevices.includes(deviceId)
  }
}

const mutations = {
  SET_DEVICES(state, data) {
    state.devices = data
  },

  ADD_STARTED_DEVICE(state, deviceId) {
    state.startedDevices.push(deviceId)
  },

  REMOVE_STARTED_DEVICE(state, deviceId) {
    state.startedDevices = state.startedDevices.filter(d => d !== deviceId)
  }
}

const actions = {
  async getDevices({ commit },) {
    const res = await this.$axios.$get("/devices")
    commit('SET_DEVICES', res)

    return res
  },

  async startDevice({ commit }, device) {
    const res = await this.$axios.$post('/device/start', device)
    if (res === true) {
      commit('ADD_STARTED_DEVICE', device.device_id)
    }

    return res
  },

  async stopDevice({ commit }, { deviceId }) {
    const res = await this.$axios.$post('/device/stop', { device_id: deviceId })
    if (res === true) {
      commit('REMOVE_STARTED_DEVICE', deviceId)
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
