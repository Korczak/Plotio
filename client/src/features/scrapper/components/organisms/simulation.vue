<template>
  <div>
    <canvas
      id="my-canvas"
      :width="width"
      :height="height"
      @mousewheel="onMouseWheel"
      @mousedown="onMouseDown"
      @mousemove="onMouseMove"
      @mouseup="onMouseUp"
      @mouseleave="onMouseUp"
    >
    </canvas>
  </div>
</template>

<script lang="ts">
import { Component, Mixins, Prop } from "vue-property-decorator";
import CanvasDrawer from "../atoms/canvas-drawer";
import {
  getPositionPlotterPositionGet,
  getProjectImagePlotterProjectCurrentProcessedImageGet,
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

    this.plotterPosition.x = plotterPosition.data.positionX;
    this.plotterPosition.y = plotterPosition.data.positionY;

    this.redrawCanvas();
  }

  context: any = null;
  canvas: any = null;
  originalImage = new Image();
  isImageLoaded: boolean = false;
  scale: number = 1;
  originx: number = 0;
  originy: number = 0;

  async mounted() {
    this.originalImage.src = "";
    this.canvas = document.querySelector("#my-canvas") as any;
    this.context = this.canvas.getContext("2d");
    this.redrawCanvas();
    this.retrieve_loop(this.getActualPosition, 50);
    this.context.scale(1, 1);
    setInterval(() => this.updateImage(), 500);
    this.redrawCanvas();
  }

  private async updateImage() {
    let imageContent =
      await getProjectImagePlotterProjectCurrentProcessedImageGet();
    if (imageContent.data != null) {
      this.originalImage.src = "data:image/png;base64," + imageContent.data;
      this.isImageLoaded = true;
    }
  }

  private redrawCanvas() {
    this.context.clearRect(
      0,
      0,
      (this.width * 1) / this.scale,
      (this.height * 1) / this.scale
    );
    this.context.save();
    this.context.translate(this.translate.x, this.translate.y);
    this.context.drawImage(this.originalImage, 0, 0);
    CanvasDrawer.drawSquarePoint(
      this.context!,
      this.plotterPosition.x,
      this.plotterPosition.y,
      "red",
      10
    );
    this.context.restore();
    this.context.save();
    this.context.translate(this.translate.x, 0);
    this.drawVerticalLine();
    this.drawMarksOnXAxis();
    this.context.restore();
    this.context.save();
    this.context.translate(0, this.translate.y);
    this.drawHorizontalLines();
    this.drawMarksOnYAxis();
    this.context.restore();
  }

  get size_of_text(): number {
    return 12 / this.scale;
  }
  line_width: number = 0.5;
  grid_size: number = 25;
  x_axis_starting_point = { start: 0, step: 25, suffix: "" };
  y_axis_starting_point = { start: 0, step: 25, suffix: "" };

  get get_num_lines_x() {
    return Math.floor(this.height / this.grid_size);
  }

  // no of horizontal grid lines
  get get_num_lines_y() {
    return Math.floor(this.width / this.grid_size);
  }

  private drawHorizontalLines() {
    for (var i = -this.get_num_lines_x; i <= this.get_num_lines_x; i++) {
      this.context.beginPath();
      this.context.lineWidth = this.line_width;

      // If line represents X-axis draw in different color
      // if (i == this.x_axis_distance_grid_lines)
      //   this.context.strokeStyle = "#000000";
      // else this.context.strokeStyle = "#e9e9e9";
      this.context.strokeStyle = "#e9e9e9";
      if (i == this.get_num_lines_x) {
        this.context.moveTo(0, this.grid_size * i);
        this.context.lineTo(this.width, this.grid_size * i);
      } else {
        this.context.moveTo(0, this.grid_size * i + 0.5);
        this.context.lineTo(this.width, this.grid_size * i + 0.5);
      }
      this.context.stroke();
    }
  }

  private drawVerticalLine() {
    // Draw grid lines along Y-axis
    for (let i = -this.get_num_lines_y; i <= this.get_num_lines_y; i++) {
      this.context.beginPath();
      this.context.lineWidth = this.line_width;

      // If line represents X-axis draw in different color
      // if (i == this.y_axis_distance_grid_lines)
      //   this.context.strokeStyle = "#000000";
      // else this.context.strokeStyle = "#e9e9e9";
      this.context.strokeStyle = "#e9e9e9";
      if (i == this.get_num_lines_y) {
        this.context.moveTo(this.grid_size * i, 0);
        this.context.lineTo(this.grid_size * i, this.height);
      } else {
        this.context.moveTo(this.grid_size * i + 0.5, 0);
        this.context.lineTo(this.grid_size * i + 0.5, this.height);
      }
      this.context.stroke();
    }
  }
  // Translate to the new origin. Now Y-axis of the canvas is opposite to the Y-axis of the graph. So the y-coordinate of each element will be negative of the actual

  private drawMarksOnXAxis() {
    // Ticks marks along the positive X-axis
    for (let i = 0; i < 100; i++) {
      this.context.beginPath();
      this.context.lineWidth = this.line_width;
      this.context.strokeStyle = "#000000";

      // Draw a tick mark 6px long (-3 to 3)
      this.context.moveTo(this.grid_size * i + 0.5, -3);
      this.context.lineTo(this.grid_size * i + 0.5, 3);
      this.context.stroke();

      // Text value at that point
      this.context.font = this.size_of_text + "px Arial";
      this.context.textAlign = "start";
      this.context.fillText(
        this.x_axis_starting_point.start +
          i * this.x_axis_starting_point.step +
          this.x_axis_starting_point.suffix,
        this.grid_size * i - 2,
        15
      );
    }

    // Ticks marks along the negative X-axis
    for (let i = 1; i < 100; i++) {
      this.context.beginPath();
      this.context.lineWidth = this.line_width;
      this.context.strokeStyle = "#000000";

      // Draw a tick mark 6px long (-3 to 3)
      this.context.moveTo(-this.grid_size * i + 0.5, -3);
      this.context.lineTo(-this.grid_size * i + 0.5, 3);
      this.context.stroke();

      // Text value at that point
      this.context.font = this.size_of_text + "px Arial";
      this.context.textAlign = "end";
      this.context.fillText(
        -this.x_axis_starting_point.start +
          i * this.x_axis_starting_point.step +
          this.x_axis_starting_point.suffix,
        -this.grid_size * i + 3,
        15
      );
    }
  }

  private drawMarksOnYAxis() {
    // Ticks marks along the positive Y-axis
    // Positive Y-axis of graph is negative Y-axis of the canvas
    for (let i = 0; i < 100; i++) {
      this.context.beginPath();
      this.context.lineWidth = this.line_width;
      this.context.strokeStyle = "#000000";

      // Draw a tick mark 6px long (-3 to 3)
      this.context.moveTo(-3, this.grid_size * i + 0.5);
      this.context.lineTo(3, this.grid_size * i + 0.5);
      this.context.stroke();

      // Text value at that point
      this.context.font = this.size_of_text + "px Arial";
      this.context.textAlign = "start";
      this.context.fillText(
        -this.y_axis_starting_point.start +
          i * this.x_axis_starting_point.step +
          this.y_axis_starting_point.suffix,
        8,
        this.grid_size * i + 3
      );
    }

    // Ticks marks along the negative Y-axis
    // Negative Y-axis of graph is positive Y-axis of the canvas
    for (let i = 1; i < 100; i++) {
      this.context.beginPath();
      this.context.lineWidth = this.line_width;
      this.context.strokeStyle = "#000000";

      // Draw a tick mark 6px long (-3 to 3)
      this.context.moveTo(-3, -this.grid_size * i + 0.5);
      this.context.lineTo(3, -this.grid_size * i + 0.5);
      this.context.stroke();

      // Text value at that point

      this.context.font = this.size_of_text + `px Arial`;
      this.context.textAlign = "start";
      this.context.fillText(
        this.y_axis_starting_point.start +
          i * this.x_axis_starting_point.step +
          this.y_axis_starting_point.suffix,
        8,
        -this.grid_size * i + 3
      );
    }
  }
  isDragging: boolean = false;
  prevX: number = 0;
  prevY: number = 0;
  private onMouseDown() {
    this.prevX = 0;
    this.prevY = 0;
    this.isDragging = true;
  }
  private onMouseUp() {
    this.prevX = 0;
    this.prevY = 0;
    this.isDragging = false;
  }
  private onMouseMove(event: any) {
    if (this.isDragging == true) {
      if (this.prevX > 0 || this.prevY > 0) {
        this.translate.x += event.pageX - this.prevX;
        this.translate.y += event.pageY - this.prevY;
      }
      this.prevX = event.pageX;
      this.prevY = event.pageY;
    }
  }

  private onMouseWheel(event: any) {
    var mousex = event.clientX - this.canvas.offsetLeft;
    var mousey = event.clientY - this.canvas.offsetTop;
    var wheel = event.deltaY < 0 ? 1 : -1;

    //according to Chris comment
    var zoom = Math.pow(1 + Math.abs(wheel) / 2, wheel > 0 ? 1 : -1);

    // this.context.save();
    // this.context.translate(this.originx, this.originy);
    this.context.scale(zoom, zoom);
    console.log(zoom);
    console.log(this.canvas.width);
    // this.canvas.width = this.canvas.width * (1 / zoom);
    // this.context.translate(
    //   -(mousex / this.scale + this.originx - mousex / (this.scale * zoom)),
    //   -(mousey / this.scale + this.originy - mousey / (this.scale * zoom))
    // );
    // this.context.restore();

    this.originx =
      mousex / this.scale + this.originx - mousex / (this.scale * zoom);
    this.originy =
      mousey / this.scale + this.originy - mousey / (this.scale * zoom);
    this.scale *= zoom;
  }
}
</script>

<style scoped></style>
