<template>
  <v-card elevation="0">
    <slot name="title">
      <h3 justify-center class="mb-2">{{ title }}</h3>
    </slot>
    <slot> </slot>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class Bar extends Vue {
  @Prop() readonly title!: string;
}
</script>

<style scoped></style>
