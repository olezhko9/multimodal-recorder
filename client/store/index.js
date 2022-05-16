import Vue from 'vue'
import Vuex from 'vuex'

import recorder from "./modules/recorder"
import research from './modules/research'
import device from './modules/device'

Vue.use(Vuex)

const getNamespacedModule = (module) => ({
  namespaced: true,
  ...module
})

const store = () => new Vuex.Store({
  modules: {
    recorder: getNamespacedModule(recorder),
    research: getNamespacedModule(research),
    device: getNamespacedModule(device),
  },
  strict: true
})

export default store
