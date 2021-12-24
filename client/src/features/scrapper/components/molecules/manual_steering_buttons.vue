<template>
  <div>
    <v-row justify="center">
      <v-btn elevation="0" tile fab><v-icon>mdi-arrow-top-left</v-icon></v-btn>
      <v-btn elevation="0" tile fab @click="move('Up')"
        ><v-icon>mdi-arrow-up</v-icon></v-btn
      >
      <v-btn elevation="0" tile fab><v-icon>mdi-arrow-top-right</v-icon></v-btn>
    </v-row>
    <v-row justify="center">
      <v-btn elevation="0" tile fab @click="move('Left')"
        ><v-icon>mdi-arrow-left</v-icon></v-btn
      >
      <v-btn elevation="0" tile fab @click="move('Hit')"
        ><v-icon>mdi-flash</v-icon></v-btn
      >
      <v-btn elevation="0" tile fab @click="move('Right')"
        ><v-icon>mdi-arrow-right</v-icon></v-btn
      >
    </v-row>
    <v-row justify="center">
      <v-btn elevation="0" tile fab
        ><v-icon>mdi-arrow-bottom-left</v-icon></v-btn
      >
      <v-btn elevation="0" tile fab @click="move('Down')"
        ><v-icon>mdi-arrow-down</v-icon></v-btn
      >
      <v-btn elevation="0" tile fab
        ><v-icon>mdi-arrow-bottom-right</v-icon></v-btn
      >
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { sendCommandPlotterCommandPost } from "@/api/index";

@Component({ components: {} })
export default class ManualSteeringButtons extends Vue {
  move(command: string) {
    sendCommandPlotterCommandPost({
      body: {
        command: command,
      },
    });
  }
}
</script>

<style scoped></style>
