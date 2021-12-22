import Vue from "vue";
import socketio, { ManagerOptions } from "socket.io-client";
import VueSocketIO from "vue-3-socket.io";

const io = socketio("ws://localhost:5000/", {
  path: "/ws/socket.io/",
  transports: ["polling"],
  extraHeaders: {},
  withCredentials: false,
});
io.on("connection", () => {
  console.log("connection");
});
io.on("connect", () => {
  console.log("connect");
});
io.on("connect_error", () => {
  console.log("connect error");
});
io.on("error", () => {
  console.log("error");
});

Vue.use(
  new VueSocketIO({
    debug: true,
    connection: io,
    options: {
      path: "/ws/socket.io",
    },
  })
);
