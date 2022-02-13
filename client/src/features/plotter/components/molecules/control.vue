<template>
  <div>
    <v-card>
      <v-btn class="my-3 ma-2" small @click="startProject()">
        <v-icon>mdi-play</v-icon>
      </v-btn>
      <v-btn class="ma-2" small @click="pauseProject()">
        <v-icon>mdi-pause</v-icon>
      </v-btn>
      <v-btn class="ma-2" small @click="stopProject()">
        <v-icon>mdi-stop</v-icon>
      </v-btn>
    </v-card>
  </div>
</template>

<script lang="ts">
import {
  pauseProjectPlotterProjectPausePost,
  startProjectPlotterProjectStartPost,
  stopProjectPlotterProjectStopPost,
} from "@/api";
import { Component, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class Control extends Vue {
  async startProject() {
    await startProjectPlotterProjectStartPost();
  }
  async stopProject() {
    await stopProjectPlotterProjectStopPost();
  }
  async pauseProject() {
    await pauseProjectPlotterProjectPausePost();
  }
}
</script>

<style scoped></style>
