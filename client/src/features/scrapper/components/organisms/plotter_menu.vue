<template>
  <div>
    <v-card>
      <v-btn class="fab-height">
        <div class="wrapper" @click="emitEvent('onImport')">
          <div>Wgraj z pliku</div>
          <div>
            <v-icon>mdi-cloud-upload</v-icon>
          </div>
        </div>
      </v-btn>
      <v-btn class="ma-2 fab-height">
        <div class="wrapper" @click="emitEvent('onSttings')">
          <div>Ustawienia</div>
          <div>
            <v-icon>mdi-cog</v-icon>
          </div>
        </div>
      </v-btn>
      <v-btn class="fab-height" @click="emitEvent('onEditor')">
        <div class="wrapper">
          <div>Edycja grafiki</div>
          <div>
            <v-icon>mdi-image-size-select-large</v-icon>
          </div>
        </div>
      </v-btn>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class PlotterMenu extends Vue {
  emitEvent(event: string) {
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
