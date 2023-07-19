import { createStore } from 'vuex'

export default createStore({
  state: {
    selectedBuilding: {
      propertiesData: null
    }
  },
  mutations: {
    setSelectedBuilding (state, building) {
      state.selectedBuilding = building
    }
  },
  actions: {
  },
  modules: {
  }
})
