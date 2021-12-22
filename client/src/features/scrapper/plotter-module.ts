import { Vue as _Vue } from "vue/types/vue";
import { VueModule } from "vue-modules";
import VueRouter from "vue-router";
import { RouteConfig } from "vue-router";
import { Store } from "vuex";
import { plotterStore } from "./store/store";
import Vue from "vue";

import Plotter from "./pages/Plotter.vue";
import HelloWorld from "@/components/organisms/HelloWorld.vue";
import Provide from "@/plugins/provide";
import IconTextBtn from "./components/atoms/icon-text-btn.vue";

Vue.component("icon-text-btn", IconTextBtn);

const plotterRoutes: RouteConfig[] = [
  {
    path: "/plotter",
    name: "plotter",
    component: Plotter,
  },
  {
    path: "/",
    name: "home",
    component: HelloWorld,
  },
];

export class PlotterModule implements VueModule {
  readonly name = "web-scrapper";
  constructor(
    private router: VueRouter,
    private store: Store<any>,
    private provide: Provide
  ) {}

  install(Vue: typeof _Vue) {
    this.router.addRoutes(plotterRoutes);
    this.provide.addProvider({});
    this.store.registerModule([this.name], plotterStore);
  }
}
