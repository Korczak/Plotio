<template>
  <div>
    <v-row class="px-3 mt-3">
      <v-col cols="12">
        <messages-bar></messages-bar>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import MessagesBar from "../molecules/messages_bar.vue";

@Component({ components: { MessagesBar } })
export default class StatusBar extends Vue {}
</script>

<style scoped></style>
