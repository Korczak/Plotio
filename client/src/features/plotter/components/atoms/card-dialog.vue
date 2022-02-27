<template>
  <div>
    <v-dialog
      v-model="dialog"
      :width="width"
      :max-width="maxWidth"
      :persistent="persistent"
    >
      <v-card>
        <slot name="card">
          <slot name="title">
            <v-card-title>{{ title }}</v-card-title>
          </slot>
          <v-card-text>
            <slot> </slot>
          </v-card-text>
          <v-card-actions>
            <slot name="actions"></slot>
          </v-card-actions>
        </slot>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Prop, VModel, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class CardDialog extends Vue {
  @Prop() readonly title!: string;
  @Prop({ default: false }) readonly persistent!: boolean;
  @Prop({ default: 600 }) readonly maxWidth!: number;
  @Prop() readonly width!: number;
  @VModel({ type: Boolean }) dialog: boolean | undefined;
}
</script>

<style scoped></style>
