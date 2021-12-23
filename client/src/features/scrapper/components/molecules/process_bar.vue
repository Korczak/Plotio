<template>
  <div>
    <bar title="Szacowany czas i postęp pracy">
      <v-progress-linear
        :value="processTime"
        height="25"
        class="mx-3"
        color="blue"
      >
        <strong>Pozostało: {{ processTimeExpectedToDo }}</strong>
      </v-progress-linear>
      <v-progress-linear
        :value="commandProcess"
        height="25"
        class="mt-2 mx-3"
        color="green"
      >
        <strong
          >Ukończono komend {{ commandsCompleted }} z {{ allCommands }}</strong
        >
      </v-progress-linear>
    </bar>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class ProcessBar extends Vue {
  processTime: number = 30;
  processTimeExpectedToDo: number = 0;
  commandProcess: number = 60;
  commandsCompleted: number = 0;
  allCommands: number = 0;
}
</script>

<style scoped></style>
