<template>
  <div>
    <v-row>
      <v-col cols="4" class="py-2"> Kontrast </v-col>
      <v-col cols="8" class="py-2">
        <v-slider
          v-model="imageAttributes.contrast"
          thumb-label="always"
          min="-100"
          max="100"
        ></v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4" class="py-2"> Jasność </v-col>
      <v-col cols="8" class="py-2">
        <v-slider
          v-model="imageAttributes.brightness"
          thumb-label="always"
          min="-100"
          max="100"
        ></v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4" class="py-2"> Wyostrzenie </v-col>
      <v-col cols="8" class="py-2">
        <v-slider
          v-model="imageAttributes.sharpness"
          thumb-label="always"
          min="-100"
          max="100"
        ></v-slider>
      </v-col>
    </v-row>
    <!-- <v-row>
      <v-col cols="4" class="py-2"> Ekspozycja </v-col>
      <v-col cols="8" class="py-2">
        <v-slider
          v-model="imageAttributes.exposition"
          thumb-label="always"
          min="-100"
          max="100"
        ></v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4" class="py-2"> Prześwietlenie </v-col>
      <v-col cols="8" class="py-2">
        <v-slider
          v-model="imageAttributes.highlights"
          thumb-label="always"
          min="-100"
          max="100"
        ></v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4" class="py-2"> Cienie </v-col>
      <v-col cols="8" class="py-2">
        <v-slider
          v-model="imageAttributes.shadow"
          thumb-label="always"
          min="-100"
          max="100"
        ></v-slider>
      </v-col>
    </v-row> -->
    <v-row>
      <v-col cols="4" class="py-2"> Algorytm ditheringu </v-col>
      <v-col cols="8" class="py-2">
        <v-select
          v-model="imageAttributes.ditherAlgorithm"
          :items="ditherAlgorithms"
        >
        </v-select>
      </v-col>
    </v-row>
    <v-row v-if="imageAttributes.ditherAlgorithm == 'Threshold'">
      <v-col cols="4" class="py-2"> Próg </v-col>
      <v-col cols="8" class="py-2">
        <v-text-field
          type="number"
          v-model="imageAttributes.threshold"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row v-if="imageAttributes.ditherAlgorithm == 'Threshold 2-rows'">
      <v-col cols="4" class="py-2"> Próg dolny </v-col>
      <v-col cols="8" class="py-2">
        <v-text-field
          type="number"
          v-model="imageAttributes.threshold2Row.threshold_1"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row v-if="imageAttributes.ditherAlgorithm == 'Threshold 2-rows'">
      <v-col cols="4" class="py-2"> Próg górny </v-col>
      <v-col cols="8" class="py-2">
        <v-text-field
          type="number"
          v-model="imageAttributes.threshold2Row.threshold_2"
        ></v-text-field>
      </v-col>
    </v-row>
    <!-- <v-row>
      <v-col cols="4" class="py-2"> Normalizacja histogramu </v-col>
      <v-col cols="8" class="py-2">
        <v-select
          v-model="imageAttributes.histogramType"
          :items="histogramTypes"
        >
        </v-select>
      </v-col>
    </v-row> -->
  </div>
</template>

<script lang="ts">
import { editImageImageEditImagePost } from "@/api";
import { Component, Vue, Watch } from "vue-property-decorator";

interface Threshold2Row {
  threshold_1: number;
  threshold_2: number;
}

interface ImageAttributeSettings {
  ditherAlgorithm:
    | "Brak"
    | "Floyd-Steinberg"
    | "False Floyd-Steinberg"
    | "Stucki"
    | "Sierra"
    | "Sierra lite"
    | "Sierra 2-rows";
  contrast: number;
  brightness: number;
  sharpness: number;
  shadow: number;
  highlights: number;
  exposition: number;
  histogramType: "Brak" | "Equalization" | "CLAHE";
  threshold: number;
  threshold2Row: Threshold2Row;
}

@Component({ components: {} })
export default class ImageSettings extends Vue {
  ditherAlgorithms: string[] = [
    "Brak",
    "Floyd-Steinberg",
    "False Floyd-Steinberg",
    "Stucki",
    "Sierra",
    "Sierra lite",
    "Sierra 2-rows",
    "Threshold",
    "Threshold 2-rows",
  ];
  histogramTypes: string[] = ["Brak", "Equalization", "CLAHE"];
  imageAttributes: ImageAttributeSettings = {
    ditherAlgorithm: "Brak",
    contrast: 0,
    brightness: 0,
    sharpness: 0,
    shadow: 0,
    highlights: 0,
    exposition: 0,
    histogramType: "Brak",
    threshold: 0,
    threshold2Row: { threshold_1: 0, threshold_2: 100 },
  };

  attributeChanging: boolean = false;
  areAttributesOutdated: boolean = false;

  @Watch("imageAttributes", { deep: true })
  async onImageAttributesChanged() {
    if (!this.attributeChanging) {
      this.attributeChanging = true;
      await this.updateAttributes();
      while (this.areAttributesOutdated) {
        await this.updateAttributes();
        this.areAttributesOutdated = false;
      }
      this.attributeChanging = false;
      this.$emit("onChange");
    } else {
      this.areAttributesOutdated = true;
    }
  }

  private async updateAttributes() {
    await editImageImageEditImagePost({
      body: {
        shadow: this.imageAttributes.shadow,
        contrast: this.imageAttributes.contrast,
        brightness: this.imageAttributes.brightness,
        sharpness: this.imageAttributes.sharpness,
        highlights: this.imageAttributes.highlights,
        exposition: this.imageAttributes.exposition,
        ditherAlgorithm: this.imageAttributes.ditherAlgorithm,
        histogramType: this.imageAttributes.histogramType,
        threshold: this.imageAttributes.threshold,
        threshold2Row: this.imageAttributes.threshold2Row,
      },
    });
  }
}
</script>

<style scoped></style>
