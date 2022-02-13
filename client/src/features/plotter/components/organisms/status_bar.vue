<template>
  <div>
    <v-row class="px-3">
      <v-col cols="6">
        <messages-bar></messages-bar>
      </v-col>
      <v-col cols="6">
        <process-bar></process-bar>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import MessagesBar from "../molecules/messages_bar.vue";
import ProcessBar from "../molecules/process_bar.vue";

@Component({ components: { MessagesBar, ProcessBar } })
export default class StatusBar extends Vue {}
</script>

<style scoped></style>
