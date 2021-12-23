<template>
  <div>
    <v-snackbar v-model="value" :timeout="timeout">
      {{ text }}

      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="value = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class ErrorSnackbar extends Vue {
  @Prop({ default: 5000 }) readonly timeout!: number;
  @Prop() readonly text!: string;
  @Model() readonly value!: boolean;
}
</script>

<style scoped></style>
