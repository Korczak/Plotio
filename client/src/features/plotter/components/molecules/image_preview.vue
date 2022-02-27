<template>
  <div>
    <canvas id="my-canvas" :width="width" :height="height"> </canvas>
  </div>
</template>

<script lang="ts">
import { getImagePreviewImagePreviewGet } from "@/api";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class ImagePreview extends Vue {
  @Prop() readonly width!: number;
  @Prop() readonly height!: number;

  context: any = null;
  canvas: any = null;
  originalImage = new Image();
  isImageLoaded: boolean = false;

  async mounted() {
    this.originalImage.src = "";
    this.canvas = document.querySelector("#my-canvas") as any;
    this.context = this.canvas.getContext("2d");

    await this.updateImage();
    this.context.drawImage(this.originalImage, 0, 0);
  }

  private async updateImage() {
    let imageContent = await getImagePreviewImagePreviewGet();
    if (imageContent.data != null) {
      this.originalImage.src = "data:image/png;base64," + imageContent.data;
      this.isImageLoaded = true;
    }
  }

  public async reloadImage() {
    this.context.clearRect(0, 0, this.width, this.height);
    await this.updateImage();
    this.context.drawImage(this.originalImage, 0, 0);
  }
}
</script>

<style scoped></style>
