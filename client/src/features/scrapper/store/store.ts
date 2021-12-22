import { Module } from "vuex";
import { ActionTree, GetterTree } from "vuex";

const INCREASE_COUNTER = "INCREASE_COUNTER";
const DECREASE_COUNTER = "DECREASE_COUNTER";
const GET_COUNTER = "GET_COUNTER";

const actions: ActionTree<any, HomeState> = {
  [INCREASE_COUNTER]({ commit }) {
    commit(INCREASE_COUNTER);
  },
  [DECREASE_COUNTER]({ commit }) {
    commit(DECREASE_COUNTER);
  },
};

const getters: GetterTree<any, HomeState> = {
  [GET_COUNTER]: (state: HomeState) => state.counter,
};

const mutations = {
  [INCREASE_COUNTER](state: HomeState) {
    ++state.counter;
  },
  [DECREASE_COUNTER](state: HomeState) {
    --state.counter;
  },
};

interface HomeState {
  counter: number;
}

const initialState: HomeState = {
  counter: 0,
};

export const plotterStore: Module<any, HomeState> = {
  namespaced: true,
  state: initialState,
  getters,
  mutations,
  actions,
};
