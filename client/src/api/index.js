import { request } from './request';

export function getAllCommandsPlotterCommandsAllGet() {
  return request("get", `/plotter/commands/all`, { "header": { "Content-Type": "application/json", }, })();
}

export function getProjectImagePlotterProjectCurrentImageGet() {
  return request("get", `/plotter/project/current/image`, { "header": { "Content-Type": "application/json", }, })();
}

export function startProjectPlotterProjectStartPost() {
  return request("post", `/plotter/project/start`, { "header": { "Content-Type": "application/json", }, })();
}

export function pauseProjectPlotterProjectPausePost() {
  return request("post", `/plotter/project/pause`, { "header": { "Content-Type": "application/json", }, })();
}

export function stopProjectPlotterProjectStopPost() {
  return request("post", `/plotter/project/stop`, { "header": { "Content-Type": "application/json", }, })();
}

export function getPositionPlotterPositionGet() {
  return request("get", `/plotter/position`, { "header": { "Content-Type": "application/json", }, })();
}

export function getModePlotterPlotterModeGet() {
  return request("get", `/plotter/plotter/mode`, { "header": { "Content-Type": "application/json", }, })();
}

export function setModePlotterPlotterModePost(params) {
  return request("post", `/plotter/plotter/mode`, { "header": { "Content-Type": "application/json", }, })(params);
}

export function getWorkModePlotterPlotterWorkModeGet() {
  return request("get", `/plotter/plotter/work/mode`, { "header": { "Content-Type": "application/json", }, })();
}

export function isConnectedPlotterPlotterPlotterConnectGet() {
  return request("get", `/plotter/plotter/connect`, { "header": { "Content-Type": "application/json", }, })();
}

export function connectToPlotterPlotterPlotterConnectPost(params) {
  return request("post", `/plotter/plotter/connect`, { "header": { "accept": "application/json", "Content-Type": "application/json", }, })(params);
}

export function getOpenPortsPlotterPlotterConnectPortsGet() {
  return request("get", `/plotter/plotter/connect/ports`, { "header": { "Content-Type": "application/json", }, })();
}

export function sendCommandPlotterCommandPost(params) {
  return request("post", `/plotter/command`, { "header": { "accept": "application/json", "Content-Type": "application/json", }, })(params);
}

export function moveToPositionPlotterCommandMoveToPost(params) {
  return request("post", `/plotter/command/move-to`, { "header": { "accept": "application/json", "Content-Type": "application/json", }, })(params);
}

export function positioningPlotterCommandPositioningPost() {
  return request("post", `/plotter/command/positioning`, { "header": { "Content-Type": "application/json", }, })();
}

export function zeroingPlotterCommandZeroingPost() {
  return request("post", `/plotter/command/zeroing`, { "header": { "Content-Type": "application/json", }, })();
}

export function getAlertsPlotterAlertsGet() {
  return request("get", `/plotter/alerts`, { "header": { "Content-Type": "application/json", }, })();
}

export function getProgressInfoPlotterProgressInfoGet() {
  return request("get", `/plotter/progress/info`, { "header": { "Content-Type": "application/json", }, })();
}

export function getPlotterSettingsPlotterPlotterSettingsGet() {
  return request("get", `/plotter/plotter/settings`, { "header": { "Content-Type": "application/json", }, })();
}

export function setPlotterSettingsPlotterPlotterSettingsPost(params) {
  return request("post", `/plotter/plotter/settings`, { "header": { "accept": "application/json", "Content-Type": "application/json", }, })(params);
}

export function addImageImageAddImagePost(params) {
  return request("post", `/image/add-image`, { "header": { "accept": "application/json", "Content-Type": "application/json", }, })(params);
}

export function rootGet() {
  return request("get", `/`, { "header": { "Content-Type": "application/json", }, })();
}

