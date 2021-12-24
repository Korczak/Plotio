<template>
  <div>
    <v-snackbar v-model="model" :timeout="timeout" :color="color">
      {{ text }}

      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="model = false"> Zamknij </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";

@Component({ components: {} })
export default class ErrorSnackbar extends Vue {
  @Prop({ default: "error" }) readonly color!: string;
  @Prop({ default: 5000 }) readonly timeout!: number;
  @Prop() readonly text!: string;
  @Prop() value: Boolean | undefined;

  model: Boolean = false;

  @Watch("value")
  onValueChanged(val: Boolean) {
    this.model = val;
  }

  @Watch("model")
  onInformationEnd(val: Boolean) {
    this.$emit("input", val);
  }
}
</script>

<style scoped></style>
