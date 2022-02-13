<template>
  <div>
    <v-card>
      <v-card-title class="justify-center">
        <span>Współrzędne </span>
      </v-card-title>
      <div>
        <v-row>
          <v-col cols="3">X:</v-col>
          <v-col cols="9">{{ plotterPosition.x }}</v-col>
        </v-row>
        <v-row>
          <v-col cols="3">Y:</v-col>
          <v-col cols="9">{{ plotterPosition.y }}</v-col>
        </v-row>
      </div>
    </v-card>
  </div>
</template>

<script lang="ts">
import { getPositionPlotterPositionGet } from "@/api/index";
import { Component, Vue } from "vue-property-decorator";
import Position from "../atoms/position";

@Component({ components: {} })
export default class Coordinates extends Vue {
  plotterPosition: Position = { x: 0, y: 0 };
  positionLoop: boolean = true;

  async getActualPositionLoop() {
    while (this.positionLoop) {
      await this.delay(1000);
      await this.getActualPosition();
    }
  }

  delay(milliseconds: number) {
    return new Promise((resolve) => {
      setTimeout(resolve, milliseconds);
    });
  }

  async getActualPosition() {
    let plotterPosition = await getPositionPlotterPositionGet();
    this.plotterPosition.x = plotterPosition.data.positionX;
    this.plotterPosition.y = plotterPosition.data.positionY;
    //console.log(this.plotterPosition.x);
  }

  mounted() {
    this.getActualPositionLoop();
  }
}
</script>

<style scoped>
dd {
  display: block;
  margin-left: 40px;
}
</style>
