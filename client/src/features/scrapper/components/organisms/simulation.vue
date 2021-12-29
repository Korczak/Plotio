<template>
  <div>
    <canvas id="my-canvas" :width="width" :height="height"> </canvas>
  </div>
</template>

<script lang="ts">
import { Component, Mixins, Prop } from "vue-property-decorator";
import CanvasDrawer from "../atoms/canvas-drawer";
import {
  getPositionPlotterPositionGet,
  getProjectImagePlotterProjectCurrentImageGet,
} from "@/api/index";
import Position from "../atoms/position";
import RetrieverLoop from "../atoms/retriever-loop";

@Component({ components: {} })
export default class Simulation extends Mixins(RetrieverLoop) {
  @Prop() readonly width!: number;
  @Prop() readonly height!: number;

  translate: Position = { x: 0, y: 0 };
  plotterPosition: Position = { x: 0, y: 0 };

  positionLoop: boolean = true;

  async getActualPosition() {
    let plotterPosition = await getPositionPlotterPositionGet();
    let redrawImage: boolean = false;
    if (
      this.plotterPosition.x != plotterPosition.data.positionX ||
      this.plotterPosition.y != plotterPosition.data.positionY
    )
      redrawImage = true;
    this.plotterPosition.x = plotterPosition.data.positionX;
    this.plotterPosition.y = plotterPosition.data.positionY;

    if (redrawImage) this.redrawCanvas();
  }

  context: any = null;
  canvas: any = null;
  originalImage = new Image();
  isImageLoaded: boolean = false;

  async mounted() {
    this.originalImage.src = "";
    this.canvas = document.querySelector("#my-canvas") as any;
    this.context = this.canvas.getContext("2d");
    this.redrawCanvas();
    this.retrieve_loop(this.getActualPosition, 50);
    this.context.scale(1, 1);
    let imageContent = await getProjectImagePlotterProjectCurrentImageGet();
    if (imageContent.data != null) {
      this.originalImage.src = "data:image/png;base64," + imageContent.data;
      this.isImageLoaded = true;
      this.redrawCanvas();
    }
  }

  private redrawCanvas() {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);

    this.context.translate(this.translate.x, this.translate.y);
    if (this.isImageLoaded) {
      this.context.drawImage(this.originalImage, 0, 0);
    }
    CanvasDrawer.drawSquarePoint(
      this.context!,
      this.plotterPosition.x,
      this.plotterPosition.y,
      "red",
      10
    );
  }
}
</script>

<style scoped></style>

function RetrieverLoop(RetrieverLoop: any) { throw new Error("Function not
implemented."); }
