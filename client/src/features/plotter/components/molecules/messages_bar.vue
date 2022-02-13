<template>
  <div>
    <bar title="Komunikaty">
      <v-virtual-scroll
        :items="items"
        min-height="60px"
        height="100px"
        item-height="24"
      >
        <template v-slot:default="{ item }">
          <p :class="getItemClass(item) + ' white--text'">{{ item.text }}</p>
        </template>
      </v-virtual-scroll>
    </bar>
  </div>
</template>

<script lang="ts">
import { getAlertsPlotterAlertsGet } from "@/api";
import { Component, Mixins } from "vue-property-decorator";
import RetrieverLoop from "../atoms/retriever-loop";

interface Alert {
  text: string;
  type: "Error" | "Warning" | "Success";
}

@Component({ components: {} })
export default class MessagesBar extends Mixins(RetrieverLoop) {
  items: Alert[] = [];

  async mounted() {
    this.retrieve_loop(this.getAlerts);
  }

  async getAlerts() {
    let alerts = await getAlertsPlotterAlertsGet();

    this.items = alerts.data.alerts;
  }

  getItemClass(item: Alert): string {
    if (item.type == "Success") return "success";
    if (item.type == "Error") return "error";
    if (item.type == "Warning") return "warning";
    return "white";
  }
}
</script>

<style scoped></style>
