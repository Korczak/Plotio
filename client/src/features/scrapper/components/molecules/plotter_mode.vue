<template>
  <div>
    <v-card>
      <v-card-title class="justify-center">
        <span>Parametry </span>
      </v-card-title>

      <div>
        <v-radio-group v-model="plotterMode">
          <v-row>
            <v-col cols="6">
              <v-radio
                :ripple="false"
                label="Tryb pracy"
                value="Work"
                @click="selectWorkMode"
              ></v-radio>
            </v-col>
            <v-col cols="6">
              <v-radio
                :ripple="false"
                label="Tryb symulacji"
                value="Simulation"
                @click="selectSimulationMode"
              ></v-radio>
            </v-col>
          </v-row>
        </v-radio-group>
        <v-text-field label="Zagłębienie"></v-text-field>
        <v-text-field label="Prędkość obróbkix XY"></v-text-field>
      </div>
    </v-card>
    <connect-dialog
      :dialog.sync="dialog"
      @onConnect="onConnect"
    ></connect-dialog>
  </div>
</template>

<script lang="ts">
import {
  getModePlotterPlotterModeGet,
  isConnectedPlotterPlotterPlotterConnectGet,
  setModePlotterPlotterModePost,
} from "@/api/index";
import { Component, Vue } from "vue-property-decorator";
import ConnectDialog from "./connect_dialog.vue";

@Component({ components: { ConnectDialog } })
export default class PlotterMode extends Vue {
  plotterMode: "Simulation" | "Work" = "Simulation";
  isConnected: boolean = false;
  dialog: boolean = false;

  async mounted() {
    let plotterMode = await getModePlotterPlotterModeGet();
    let isConnected = await isConnectedPlotterPlotterPlotterConnectGet();

    this.plotterMode = plotterMode.data;
    this.isConnected = isConnected.data;
  }

  selectWorkMode() {
    if (!this.isConnected) {
      this.dialog = true;
      this.plotterMode = "Simulation";
    } else {
      this.plotterMode = "Work";
      setModePlotterPlotterModePost({
        query: {
          input: this.plotterMode,
        },
      });
    }
  }

  selectSimulationMode() {
    this.plotterMode = "Simulation";
    setModePlotterPlotterModePost({
      query: {
        input: this.plotterMode,
      },
    });
  }

  onConnect() {
    this.plotterMode = "Work";
    setModePlotterPlotterModePost({
      query: {
        input: this.plotterMode,
      },
    });
  }
}
</script>

<style scoped></style>
