import { commit } from "lodash/seq"

export default async function ({ store, $axios }) {
  console.log('middleware')
  if (!store.state.synchronized) {
    const session = await $axios.$get('/session')
    if (session.is_recording) {
      store.commit('record/SET_STATE', 'ACTIVE')
    }
    if (session.started_devices) {
      for (let deviceId of session.started_devices) {
        store.commit('device/ADD_STARTED_DEVICE', deviceId)
      }
    }
    store.commit('SET_SYNCHRONIZED', true)
  }
}
