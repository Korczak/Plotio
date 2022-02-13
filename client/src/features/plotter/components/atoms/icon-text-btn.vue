<template>
  <v-btn text outlined style="height: 100%" x-small>
    <v-col cols="12">
      <v-row width="100%" style="place-content: center">
        <v-icon large color="rgb(0, 0, 0, 0.5)"> {{ icon }} </v-icon>
      </v-row>
      <v-row width="100%" style="place-content: center">
        <span> {{ text }} </span>
      </v-row>
    </v-col>
  </v-btn>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class IconTextBtn extends Vue {
  @Prop() readonly icon!: string;
  @Prop() readonly text!: string;
}
</script>

<style scoped></style>
