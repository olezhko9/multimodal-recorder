import Vue from 'vue'
import Vuex from 'vuex'

import recorder from "./modules/recorder"
import research from './modules/research'

Vue.use(Vuex)

const store = () => new Vuex.Store({
  modules: {
    recorder: {
      namespaced: true,
      ...recorder
    },
    research: {
      namespaced: true,
      ...research
    }
  },
  strict: true
})

export default store
