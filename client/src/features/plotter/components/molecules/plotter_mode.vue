<template>
  <div>
    <v-card>
      <v-card-title class="pa-2 pb-0 justify-center">
        <span>Parametry </span>
      </v-card-title>

      <v-container class="px-2">
        <v-radio-group v-model="plotterMode" class="py-0" hide-details>
          <v-row>
            <v-col cols="6" class="pt-0">
              <v-radio
                :ripple="false"
                label="Tryb pracy"
                value="Work"
                @click="selectWorkMode"
              ></v-radio>
            </v-col>
            <v-col cols="6" class="pt-0">
              <v-radio
                :ripple="false"
                label="Tryb symulacji"
                value="Simulation"
                @click="selectSimulationMode"
              ></v-radio>
            </v-col>
          </v-row>
        </v-radio-group>
        <v-row>
          <v-col cols="9">
            <v-text-field
              v-model="hitCount"
              type="number"
              label="Liczba uderzeń"
              hide-details
            ></v-text-field>
            <v-text-field
              v-model="speedOfMotors"
              type="number"
              label="Prędkość obróbki XY"
              hide-details
            ></v-text-field>
            <v-text-field
              v-model="pixelDensity"
              type="number"
              label="Liczba kroków na piksel"
              hide-details
            ></v-text-field>
          </v-col>
          <v-col cols="3" class="px-0">
            <v-btn
              color="success"
              class="px-2 mt-5"
              max-width="80px"
              height="120px"
              @click="setPlotterSettings"
              >Zapisz</v-btn
            >
          </v-col>
        </v-row>
      </v-container>
      <automatic-mode-block-card></automatic-mode-block-card>
    </v-card>
    <connect-dialog
      :dialog.sync="dialog"
      @onConnect="onConnect"
    ></connect-dialog>
    <error-snackbar v-model="error" :text="errorMessage"></error-snackbar>
  </div>
</template>

<script lang="ts">
import {
  getModePlotterPlotterModeGet,
  isConnectedPlotterPlotterPlotterConnectGet,
  setModePlotterPlotterModePost,
  setPlotterSettingsPlotterPlotterSettingsPost,
  getPlotterSettingsPlotterPlotterSettingsGet
} from "@/api/index";
import { Component, Vue } from "vue-property-decorator";
import ConnectDialog from "./connect_dialog.vue";
import AutomaticModeBlockCard from "./automatic_mode_block_card.vue";


@Component({ components: { ConnectDialog, AutomaticModeBlockCard } })
export default class PlotterMode extends Vue {
  plotterMode: "Simulation" | "Work" = "Simulation";
  isConnected: boolean = false;
  dialog: boolean = false;

  speedOfMotors: number = 0;
  hitCount: number = 0;
  pixelDensity: number = 0;

  error: boolean = false;
  errorMessage: string = "";

  async mounted() {
    let plotterMode = await getModePlotterPlotterModeGet();
    let isConnected = await isConnectedPlotterPlotterPlotterConnectGet();
    const settings = await getPlotterSettingsPlotterPlotterSettingsGet();

    this.speedOfMotors = settings.data.speedOfMotors;
    this.hitCount = settings.data.hitCount;
    this.pixelDensity = settings.data.pixelDensity;

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

  async setPlotterSettings() {
    const response = await setPlotterSettingsPlotterPlotterSettingsPost({
      body: {
        speedOfMotors: this.speedOfMotors,
        hitCount: this.hitCount,
        pixelDensity: this.pixelDensity,
      },
    });

    if (!response.data.is_success) {
      this.error = true;
      this.errorMessage = response.data.message;
    }
  }
}
</script>

<style scoped></style>
