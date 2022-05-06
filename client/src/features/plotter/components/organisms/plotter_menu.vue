<template>
  <div>
    <v-card>
      <v-row>
        <v-col cols="4">
          <v-btn class="my-3 ma-2 wrapper">
            <div @click="emitEvent('onImport')">
              <div>Wgraj</div>
              <v-icon>mdi-cloud-upload</v-icon>
            </div>
          </v-btn>
        </v-col> 
        <v-col cols="8">
          <control></control>
        </v-col> 
      </v-row>    
      <!-- <v-btn class="ma-2 fab-height">
        <div class="wrapper" @click="emitEvent('onSettings')">
          <div>Ustawienia</div>
          <div>
            <v-icon>mdi-cog</v-icon>
          </div>
        </div>
      </v-btn>
      <v-btn class="fab-height" @click="emitEvent('onGraphicsEditor')">
        <div class="wrapper">
          <div>Edycja grafiki</div>
          <div>
            <v-icon>mdi-image-size-select-large</v-icon>
          </div>
        </div>
      </v-btn> -->
      <!-- <automatic-mode-block-card></automatic-mode-block-card> -->
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import AutomaticModeBlockCard from "../molecules/automatic_mode_block_card.vue";
import Control from "../molecules/control.vue";

@Component({ components: { AutomaticModeBlockCard, Control } })
export default class PlotterMenu extends Vue {
  emitEvent(event: string) {
    console.log("EVENT");
    this.$emit(event);
  }
}
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.fab-height {
  height: 56px;
}
</style>
