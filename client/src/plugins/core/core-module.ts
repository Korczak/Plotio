import { Vue as _Vue } from "vue/types/vue";
import { VueModule } from "vue-modules";
import VueRouter from "vue-router";
import { Store } from "vuex";
import App from "@/App.vue";
import vuetify from "@/plugins/vuetify";
import Provide from "@/plugins/provide";

export class CoreModule implements VueModule {
  readonly name = "core";
  constructor(
    private router: VueRouter,
    private store: Store<any>,
    private provide: Provide
  ) {}
  install(Vue: typeof _Vue) {
    new Vue({
      router: this.router,
      store: this.store,
      vuetify: vuetify,
      provide: this.provide.getProviders(),
      render: (h) => h(App),
    }).$mount("#app");
  }
}
