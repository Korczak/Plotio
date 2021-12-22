<template>
  <v-app>
    <v-main class="grey lighten-3">
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class App extends Vue {
  @Prop() private msg!: string;
}
</script>

<style lang="scss">
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>

<style>
.cardColor {
  background-color: rgba(255, 255, 255, 0.2) !important;
  border-color: white !important;
}
</style>
