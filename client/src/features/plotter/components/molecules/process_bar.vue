<template>
  <div>
    <bar>
      <v-progress-linear
        :value="commandProcess"
        height="25"
        class="mt-2 px-3"
        color="green"
      >
        <strong>{{ commandProcess.toFixed(2) }}%</strong>
      </v-progress-linear>
    </bar>
    <bar>
      <v-template v-slot:title>
        Szacowany czas
      </v-template>
      <strong>{{ (durationLeft/60).toFixed(0) }} h {{ (durationLeft%60).toFixed(0) }} m</strong>
      {{ durationLeft.toFixed(2) }}
    </bar>
  </div>
</template>

<script lang="ts">
import { getProgressInfoPlotterProgressInfoGet } from "@/api";
import { Component, Mixins } from "vue-property-decorator";
import RetrieverLoop from "../atoms/retriever-loop";

@Component({ components: {} })
export default class ProcessBar extends Mixins(RetrieverLoop) {
  commandsCompleted: number = 0;
  allCommands: number = 0;
  durationLeft: number = 0;

  mounted() {
    this.retrieve_loop(this.getProgress);
  }

  async getProgress() {
    let progressInfo = await getProgressInfoPlotterProgressInfoGet();

    this.commandsCompleted = progressInfo.data.commandsDone;
    this.allCommands = progressInfo.data.commandsTotal;
    this.durationLeft = progressInfo.data.durationLeft;
  }

  get commandProcess(): number {
    return (this.commandsCompleted / this.allCommands) * 100;
  }
}
</script>

<style scoped></style>
