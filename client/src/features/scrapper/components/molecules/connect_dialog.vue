<template>
  <div>
    <v-dialog v-model="dialogSync" width="500" :persistent="connecting">
      <v-card>
        <loading-in-progress
          v-if="connecting"
          title="Łączenie z urządzeniem..."
        ></loading-in-progress>
        <v-container v-else>
          <v-card-title> Połącz się </v-card-title>
          <v-form lazy-validation ref="form">
            <v-select
              v-model="port"
              label="Port:"
              :items="ports"
              :rules="[(v) => !!v || 'Port musi zostać wybrany']"
            ></v-select>
            <v-text-field
              v-model="baudrate"
              label="Baudrate:"
              type="number"
              :rules="[(v) => !!v || 'Baudrate musi zostać wybrany']"
            ></v-text-field>
            <v-text-field
              v-model="timeout"
              label="Timeout:"
              type="number"
              :rules="[(v) => !!v || 'Timeout musi zostać wybrany']"
            ></v-text-field>
            <v-card-actions>
              <v-btn color="error" @click="discard">Anuluj</v-btn>
              <v-spacer></v-spacer>
              <v-btn color="success" @click="connect">Połącz</v-btn>
            </v-card-actions>
          </v-form>
        </v-container>
      </v-card>
      <error-snackbar v-model="error" :text="errorMessage"></error-snackbar>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import {
  connectToPlotterPlotterPlotterConnectPost,
  getOpenPortsPlotterPlotterConnectPortsGet,
} from "@/api";
import { Component, PropSync, Vue } from "vue-property-decorator";

@Component({ components: {} })
export default class ConnectDialog extends Vue {
  @PropSync("dialog", { type: Boolean }) dialogSync!: boolean;

  port: string | null = null;
  ports: string[] = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6"];
  baudrate: number = 9600;
  timeout: number = 0.1;
  connecting: boolean = false;
  error: boolean = false;
  errorMessage: string | null = "";

  async mounted() {
    await getOpenPortsPlotterPlotterConnectPortsGet();

    // this.ports = ports.data;
  }

  async connect() {
    if (
      (this.$refs.form as Vue & { validate: () => boolean }).validate() == false
    ) {
      return;
    }
    this.connecting = true;
    let connectResponse = await connectToPlotterPlotterPlotterConnectPost({
      body: {
        port: this.port!,
        baudrate: this.baudrate,
        timeout: this.timeout,
      },
    });
    this.connecting = false;
    if (connectResponse.data.is_success) {
      this.$emit("onConnect");
      this.dialogSync = false;
    } else {
      this.error = true;
      this.errorMessage = connectResponse.data.error_message;
    }
  }

  discard() {
    this.dialogSync = false;
  }
}
</script>

<style scoped></style>
