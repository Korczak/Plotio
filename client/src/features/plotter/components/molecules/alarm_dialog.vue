<template>
  <div>
    <v-dialog v-model="alarm.is_enabled" width="500" persistent>
      <v-card align-center v-if="!isReset">
        <v-container justify-center>
          <v-card-title> Alarm </v-card-title>
          <v-card-text>{{ alarm.text }}</v-card-text>
          <v-card-actions>
            <v-btn color="warning" @click="ignore">
              Ignoruj na 10 sekund
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="reset"> Resetuj </v-btn>
          </v-card-actions>
        </v-container>
      </v-card>
      <v-card v-else>
        <loading-in-progress title="Resetowanie..."></loading-in-progress>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import {
  getAlarmPlotterPlotterAlarmGet,
  ignoreAlarmPlotterPlotterAlarmIgnorePost,
  resetAlarmPlotterPlotterAlarmResetPost,
} from "@/api";
import { Component } from "vue-property-decorator";
import RetrieverLoop from "../atoms/retriever-loop";

interface Alarm {
  is_enabled: boolean;
  text: string;
}

@Component({ components: {} })
export default class AlarmDialog extends RetrieverLoop {
  alarm: Alarm = { is_enabled: false, text: "" };
  isReset: boolean = false;

  mounted() {
    this.retrieve_loop(this.getAlarm);
  }

  async getAlarm() {
    const alarm = await getAlarmPlotterPlotterAlarmGet();

    this.alarm = {
      is_enabled: alarm.data.is_alarm,
      text: alarm.data.message,
    };

    if (this.alarm.is_enabled == false) {
      this.isReset = false;
    }
  }

  async ignore() {
    await ignoreAlarmPlotterPlotterAlarmIgnorePost();
    this.alarm.is_enabled = false;
  }

  async reset() {
    await resetAlarmPlotterPlotterAlarmResetPost();
    this.isReset = true;
  }
}
</script>

<style scoped></style>
