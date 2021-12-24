<template>
  <div>
    <bar title="Szacowany czas i postęp pracy">
      <v-progress-linear
        :value="commandProcess"
        height="25"
        class="mt-2 px-3"
        color="green"
      >
        <strong>{{ commandProcess.toFixed(2) }}%</strong>
      </v-progress-linear>
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

  mounted() {
    this.retrieve_loop(this.getProgress);
  }

  async getProgress() {
    let progressInfo = await getProgressInfoPlotterProgressInfoGet();

    this.commandsCompleted = progressInfo.data.commandsDone;
    this.allCommands = progressInfo.data.commandsTotal;
  }

  get commandProcess(): number {
    return (this.commandsCompleted / this.allCommands) * 100;
  }
}
</script>

<style scoped></style>
