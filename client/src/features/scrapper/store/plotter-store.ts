import { getWorkModePlotterPlotterWorkModeGet } from "@/api";
import { Vue as _Vue } from "vue/types/vue";

export class PlotterStore {
  work_mode: "Automatic" | "Manual" = "Manual";

  constructor() {
    console.log("CONSTRUCTOR");
    this.work_mode = "Manual";
    setInterval(async () => await this.update_work_mode(), 1000);
  }

  async update_work_mode() {
    console.log(this.work_mode);
    const workMode = await getWorkModePlotterPlotterWorkModeGet();

    this.work_mode = workMode.data;
  }
}
