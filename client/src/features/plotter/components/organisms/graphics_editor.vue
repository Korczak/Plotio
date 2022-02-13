<template>
  <div>
    <card-dialog
      v-model="dialog"
      title="Edytor grafik"
      :persistent="optimizationInProgress"
    >
      <template v-slot:card v-if="optimizationInProgress">
        <loading-in-progress title="Optymalizuje..."></loading-in-progress>
      </template>
      <v-btn @click="optimize()">Optymalizuj obrazek</v-btn>
      <save-restore-project-buttons></save-restore-project-buttons>
    </card-dialog>
  </div>
</template>

<script lang="ts">
import { optimizeProjectOptimizeOptimizeProjectActualPost } from "@/api";
import { Component, VModel, Vue } from "vue-property-decorator";
import SaveRestoreProjectButtons from "../molecules/save_restore_project_buttons.vue";

@Component({ components: { SaveRestoreProjectButtons } })
export default class GraphicsEditor extends Vue {
  @VModel({ type: Boolean }) dialog: boolean | undefined;

  optimizationInProgress: boolean = false;

  async optimize() {
    this.optimizationInProgress = true;
    await optimizeProjectOptimizeOptimizeProjectActualPost();
    this.optimizationInProgress = false;
    this.dialog = false;
  }
}
</script>

<style scoped></style>
