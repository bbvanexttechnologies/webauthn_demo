import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: 'UnAuthenticated',
    status: false,
  },
  methods: {
  },
  actions: {
    isAuthenticated: state => !!state.token,
    authStatus: state => state.status,
  },
  modules: {
  },
  getters: {
    token: state => state.token
  }
})
