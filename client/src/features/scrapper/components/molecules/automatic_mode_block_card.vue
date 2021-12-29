<template>
  <div>
    <v-overlay v-if="isOverlay" absolute> </v-overlay>
  </div>
</template>

<script lang="ts">
import { Component, Inject } from "vue-property-decorator";
import { PlotterStore } from "../../store/plotter-store";
import RetrieverLoop from "../atoms/retriever-loop";

@Component({ components: {} })
export default class AutomaticModeBlockCard extends RetrieverLoop {
  @Inject() readonly plotterStore!: PlotterStore;
  isOverlay: boolean = false;

  mounted() {
    setInterval(() => this.updateOverlay(), 1000);
  }

  updateOverlay() {
    if (this.plotterStore.work_mode == "Automatic") {
      this.isOverlay = true;
    } else {
      this.isOverlay = false;
    }
  }
}
</script>

<style scoped></style>
