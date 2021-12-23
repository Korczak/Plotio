<template>
  <div>
    <v-card>
      <v-row class="pt-2">
        <v-col cols="6">
          <manual-steering-buttons></manual-steering-buttons>
        </v-col>
        <v-col cols="6">
          <manual-steering-position class="mr-3"></manual-steering-position>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ManualSteeringButtons from "../molecules/manual_steering_buttons.vue";
import ManualSteeringPosition from "../molecules/manual_steering_position.vue";

@Component({ components: { ManualSteeringPosition, ManualSteeringButtons } })
export default class ManualSteering extends Vue {}
</script>

<style scoped></style>
