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

  async startDevice({ commit }, devices) {
    if (!Array.isArray(devices)) devices = [devices]
    const res = await this.$axios.$post('/device/start', devices)
    if (res === true) {
      for (let device of devices) {
        commit('ADD_STARTED_DEVICE', device.device_id)
      }
    }

    return res
  },

  async stopDevice({ commit }, devices) {
    if (!Array.isArray(devices)) devices = [devices]
    const res = await this.$axios.$post('/device/stop', devices)
    if (res === true) {
      for (let device of devices) {
        commit('REMOVE_STARTED_DEVICE', device.device_id)
      }
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
