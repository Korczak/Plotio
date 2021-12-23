<template>
  <div>
    <v-container fluid>
      <h3 justify-center>{{ title }}</h3>
      <v-progress-circular
        :size="50"
        color="primary"
        indeterminate
      ></v-progress-circular>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class LoadingInProgress extends Vue {
  @Prop({ default: "Ładowanie..." }) readonly title!: string;
}
</script>

<style scoped></style>
