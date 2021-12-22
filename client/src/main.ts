import Vue from "vue";
import { PlotterModule } from "./features/scrapper/plotter-module";
import { RouterModule } from "@/plugins/router";
import { StoreModule } from "./plugins/store";
import { CoreModule } from "./plugins/core";
import Provide from "./plugins/provide";
import "./plugins/socketio/socketio";

Vue.config.productionTip = false;

function bootstrap() {
  const routerModule = new RouterModule();
  routerModule.install(Vue);

  const providers = new Provide();

  const storeModule = new StoreModule();
  storeModule.install(Vue);

  const plotterModule = new PlotterModule(
    routerModule.router!,
    storeModule.store!,
    providers
  );
  plotterModule.install(Vue);

  const coreModule = new CoreModule(
    routerModule.router!,
    storeModule.store!,
    providers
  );
  coreModule.install(Vue);
}

bootstrap();
