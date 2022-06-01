import createMultiTabState from 'vuex-multi-tab-state'

export default ({ store }) => {
  createMultiTabState({
    statesPaths: ['device', 'record']
  })(store)
}
