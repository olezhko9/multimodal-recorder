export default async function ({ store, $axios }) {
  console.log('middleware')
  if (!store.state.synchronized) {
    const session = await $axios.$get('/session')
    if (session.is_recording) {
      store.commit('record/SET_STATE', 'ACTIVE')
    } else {
      store.commit('record/SET_STATE', 'INACTIVE')
    }

    if (session.started_devices) {
      store.commit('device/SET_STARTED_DEVICES', session.started_devices)
    }
    store.commit('SET_SYNCHRONIZED', true)
  }
}
