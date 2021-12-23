<template>
  <div>
    <bar title="Komunikaty">
      <v-virtual-scroll :items="items" height="auto" item-height="20">
        <template v-slot:default="{ item }">
          {{ item }}
        </template>
      </v-virtual-scroll>
    </bar>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class MessagesBar extends Vue {
  items: string[] = [
    "Komunikat 1 BARDZO DLUGI DLUGOSCI",
    "Komunikat 2",
    "Komunikat 3",
  ];
}
</script>

<style scoped></style>
