<template>
  <div>
    <div>
      <v-text-field label="X:" hide-details></v-text-field>
      <v-text-field label="Y:" hide-details></v-text-field>
      <v-text-field label="Z:" hide-details></v-text-field>
    </div>
    <v-card-title class="justify-center">
      <v-btn>Pozycjonowanie </v-btn>
    </v-card-title>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class ManualSteeringPosition extends Vue {}
</script>

<style scoped></style>
