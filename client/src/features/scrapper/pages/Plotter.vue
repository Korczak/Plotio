<template>
  <div>
    <import-image :dialog.sync="isImageImport"></import-image>
    <v-container fluid class="py-0">
      <v-row class="mt-2">
        <v-col cols="7">
          <v-row>
            <v-col cols="8" class="py-0">
              <plotter-menu @onImport="isImageImport = true"></plotter-menu>
            </v-col>
            <v-col cols="4" class="py-0">
              <control></control>
            </v-col>
          </v-row>
          <v-row class="mt-3">
            <v-col cols="6" class="">
              <plotter-mode></plotter-mode>
            </v-col>
            <v-col cols="6" class="">
              <coordinates></coordinates>
            </v-col>
          </v-row>
          <v-row class="mt-2">
            <v-col cols="12">
              <manual-steering></manual-steering>
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="5" class="pa-0" id="canvas-area">
          <simulation
            v-if="simulationAreaCalculated"
            :width="simulationWidth"
            :height="simulationHeight"
          ></simulation>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" class="pa-0">
          <status-bar></status-bar>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Control from "../components/molecules/control.vue";
import Coordinates from "../components/molecules/coordinates.vue";
import PlotterMenu from "../components/organisms/plotter_menu.vue";
import PlotterMode from "../components/molecules/plotter_mode.vue";
import ManualSteering from "../components/organisms/manual_steering.vue";
import Simulation from "../components/organisms/simulation.vue";
import ImportImage from "../components/organisms/import_image.vue";
import StatusBar from "../components/organisms/status_bar.vue";
//import { rootGet } from "@/api/index";

@Component({
  components: {
    PlotterMenu,
    Control,
    Coordinates,
    PlotterMode,
    ManualSteering,
    Simulation,
    ImportImage,
    StatusBar,
  },
})
export default class Plotter extends Vue {
  message: string = "";
  isImageImport = false;

  created() {
    console.log(this.$socket);

    this.$socket.on("connect", () => {
      console.log("connect");
    });
    this.$socket.on("message", () => {
      console.log("message");
    });
    this.$socket.on("PlotterPositionChanged", (arg: any) => {
      console.log("plotter");
      console.log(arg);
    });
    this.$socket.on("PlotterPositionChanged", () => {
      console.log("plotter");
    });
  }

  async mounted() {
    //const result = await rootGet();
    //this.message = result.data;

    this.$socket.on("PlotterPositionChanged", (arg: any) => {
      console.log("plotter");
      console.log(arg);
    });
    this.$socket.on("PlotterPositionChanged", () => {
      console.log("plotter");
    });

    this.calculateSimulationArea();
  }

  simulationAreaCalculated: boolean = false;
  simulationWidth: number = 0;
  simulationHeight: number = 0;

  calculateSimulationArea() {
    let width = document.getElementById("canvas-area")?.clientWidth;

    console.log(width);
    if (width) this.simulationWidth = width;
    let height = document.getElementById("canvas-area")?.clientHeight;

    if (height) this.simulationHeight = height;

    this.simulationAreaCalculated = true;
    console.log(this.simulationAreaCalculated);
  }
}
</script>

<style scoped></style>
