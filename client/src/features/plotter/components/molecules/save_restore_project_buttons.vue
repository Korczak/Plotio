<template>
  <div>
    <v-btn @click="SaveProject">Zapisz projekt</v-btn>
    <v-btn @click="RestoreProject">Załaduj projekt</v-btn>
  </div>
</template>

<script lang="ts">
import {
  restoreProjectPlotterProjectRestorePost,
  saveProjectPlotterProjectSaveToFilePost,
} from "@/api";
import { Component, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class SaveRestoreProjectButtons extends Vue {
  async SaveProject() {
    await saveProjectPlotterProjectSaveToFilePost();
  }

  async RestoreProject() {
    await restoreProjectPlotterProjectRestorePost();
  }
}
</script>

<style scoped></style>
