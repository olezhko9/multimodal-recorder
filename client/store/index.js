import Vue from 'vue'
import Vuex from 'vuex'

import recorder from "./recorder"

Vue.use(Vuex)

const store = () => new Vuex.Store({
  modules: {
    recorder: {
      namespaced: true,
      ...recorder
    }
  },
  strict: true
})

export default store
