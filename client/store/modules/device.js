const state = () => ({
  devices: [],
  startedDevices: [],
  startedDevicesParams: {}
})

const getters = {
  isDeviceStarted: state => deviceId => {
    return state.startedDevices.includes(deviceId)
  },

  deviceById: state => deviceId => {
    return state.devices.find(d => d.device_id === deviceId)
  },

  startedDeviceParams: state => deviceId => {
    return state.startedDevicesParams[deviceId] || {}
  }
}

const mutations = {
  SET_DEVICES(state, data) {
    state.devices = data
  },

  SET_STARTED_DEVICES(state, devices) {
    state.startedDevices = devices
  },

  ADD_STARTED_DEVICE(state, device) {
    if (!state.startedDevices.includes(device.device_id)) {
      state.startedDevices.push(device.device_id)
      state.startedDevicesParams[device.device_id] = device
    }
  },

  REMOVE_STARTED_DEVICE(state, deviceId) {
    state.startedDevices = state.startedDevices.filter(d => d !== deviceId)
  },

  DELETE_DEVICE(state, deviceId) {
    state.devices = state.devices.filter(device => device.device_id !== deviceId)
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
    for (let device of res) {
      commit('ADD_STARTED_DEVICE', device)
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
  },

  async deleteDevice({ commit }, deviceId) {
    const res = await this.$axios.$delete(`/device/${deviceId}`)
    commit('DELETE_DEVICE', deviceId)
    return res
  }
}

export default {
  state,
  getters,
  mutations,
  actions,
}
