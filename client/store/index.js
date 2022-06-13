import Vue from 'vue'
import Vuex from 'vuex'

import record from "./modules/record"
import research from './modules/research'
import device from './modules/device'
import subject from './modules/subject'
import notebook from './modules/notebook'
import pipeline from './modules/pipeline'

Vue.use(Vuex)

const getNamespacedModule = (module) => ({
  namespaced: true,
  ...module
})

const store = () => new Vuex.Store({
  modules: {
    record: getNamespacedModule(record),
    research: getNamespacedModule(research),
    device: getNamespacedModule(device),
    subject: getNamespacedModule(subject),
    notebook: getNamespacedModule(notebook),
    pipeline: getNamespacedModule(pipeline),
  },
  strict: true,

  state: {
    synchronized: false,
  },

  mutations: {
    SET_SYNCHRONIZED(state, isSynchronized) {
      state.synchronized = isSynchronized
    }
  }
})

export default store
