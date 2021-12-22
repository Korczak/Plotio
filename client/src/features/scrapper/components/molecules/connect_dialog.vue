<template>
  <div>
    <v-dialog v-model="dialogSync" width="500">
      <v-card>
        <v-container>
          <v-card-title> Połącz się </v-card-title>
          <v-select v-model="port" label="Port:" :items="ports"></v-select>
          <v-text-field
            v-model="baudrate"
            label="Baudrate:"
            type="number"
          ></v-text-field>
          <v-text-field
            v-model="timeout"
            label="Timeout:"
            type="number"
          ></v-text-field>
          <v-card-actions>
            <v-btn color="error" @click="discard">Anuluj</v-btn>
            <v-spacer></v-spacer>
            <v-btn color="success" @click="connect">Połącz</v-btn>
          </v-card-actions>
        </v-container>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { connectToPlotterPlotterPlotterConnectPost } from "@/api";
import { Component, PropSync, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class ConnectDialog extends Vue {
  @PropSync("dialog", { type: Boolean }) dialogSync!: boolean;

  port: string = "COM3";
  ports: string[] = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6"];
  baudrate: number = 9600;
  timeout: number = 0.1;

  async connect() {
    await connectToPlotterPlotterPlotterConnectPost({
      body: {
        port: this.port,
        baudrate: this.baudrate,
        timeout: this.baudrate,
      },
    });
    this.$emit("onConnect");
    this.dialogSync = false;
  }

  discard() {
    this.dialogSync = false;
  }
}
</script>

<style scoped></style>
