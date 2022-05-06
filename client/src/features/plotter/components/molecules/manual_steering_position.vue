<template>
  <div>
    <v-row class="mx-3">
      <v-col cols="9" class="px-0">
        <v-text-field label="X:" hide-details v-model="xValue"></v-text-field>
      </v-col>
      <v-col cols="3" align-self="end" class="px-0">
        <v-btn text @click="move(xValue, 'X')">Jedź</v-btn>
      </v-col>
    </v-row>
    <v-row class="mx-3 mt-5">
      <v-col cols="9" class="pa-0">
        <v-text-field label="Y:" hide-details v-model="yValue"></v-text-field>
      </v-col>
      <v-col cols="3" align-self="end" class="pa-0">
        <v-btn text @click="move(yValue, 'Y')">Jedź</v-btn>
      </v-col>
    </v-row>
    <v-row class="mx-3 pt-3 mb-1">
      <v-btn @click="positioning()">Pozycjonowanie </v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="zeroing()">Zerowanie </v-btn>
    </v-row>
    <error-snackbar v-model="error" :text="errorMessage"></error-snackbar>
  </div>
</template>

<script lang="ts">
import {
  moveToPositionPlotterCommandMoveToPost,
  positioningPlotterCommandPositioningPost,
  zeroingPlotterCommandZeroingPost,
} from "@/api";
import { Component, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class ManualSteeringPosition extends Vue {
  xValue: number = 0;
  yValue: number = 0;
  error: boolean = false;
  errorMessage: string = "";

  async move(value: number, direction: "X" | "Y") {
    await moveToPositionPlotterCommandMoveToPost({
      body: {
        position: value,
        direction: direction,
      },
    });
  }

  async positioning() {
    let response = await positioningPlotterCommandPositioningPost();

    if (!response.data.isSuccess) {
      this.error = true;
      this.errorMessage = response.data.message;
    }
  }

  async zeroing() {
    await zeroingPlotterCommandZeroingPost();
  }
}
</script>

<style scoped></style>
