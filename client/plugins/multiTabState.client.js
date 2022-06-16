import createMultiTabState from 'vuex-multi-tab-state'

export default ({ store }) => {
  createMultiTabState({
    statesPaths: ['device.startedDevices', 'device.startedDevicesParams', 'record.recordState']
  })(store)
}
