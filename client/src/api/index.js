import { request } from './request';

export function getAllCommandsPlotterCommandsAllGet() {
  return request("get", `/plotter/commands/all`, { "header": { "Content-Type": "application/json", }, })();
}

export function getProjectImagePlotterProjectCurrentImageGet() {
  return request("get", `/plotter/project/current/image`, { "header": { "Content-Type": "application/json", }, })();
}

export function getProjectImagePlotterProjectCurrentProcessedImageGet() {
  return request("get", `/plotter/project/current/processed-image`, { "header": { "Content-Type": "application/json", }, })();
}

export function restoreProjectPlotterProjectRestorePost() {
  return request("post", `/plotter/project/restore`, { "header": { "Content-Type": "application/json", }, })();
}

export function saveProjectPlotterProjectSaveToFilePost() {
  return request("post", `/plotter/project/save-to-file`, { "header": { "Content-Type": "application/json", }, })();
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

export function getAlarmPlotterPlotterAlarmGet() {
  return request("get", `/plotter/plotter/alarm`, { "header": { "Content-Type": "application/json", }, })();
}

export function resetAlarmPlotterPlotterAlarmResetPost() {
  return request("post", `/plotter/plotter/alarm/reset`, { "header": { "Content-Type": "application/json", }, })();
}

export function ignoreAlarmPlotterPlotterAlarmIgnorePost() {
  return request("post", `/plotter/plotter/alarm/ignore`, { "header": { "Content-Type": "application/json", }, })();
}

export function addImageImageAddImagePost(params) {
  return request("post", `/image/add-image`, { "header": { "accept": "application/json", "Content-Type": "application/json", }, })(params);
}

export function editImageImageEditImagePost(params) {
  return request("post", `/image/edit-image`, { "header": { "accept": "application/json", "Content-Type": "application/json", }, })(params);
}

export function approveImageImageApproveImagePost() {
  return request("post", `/image/approve-image`, { "header": { "Content-Type": "application/json", }, })();
}

export function getImagePreviewImagePreviewGet() {
  return request("get", `/image/preview`, { "header": { "Content-Type": "application/json", }, })();
}

export function optimizeProjectOptimizeOptimizeProjectActualPost() {
  return request("post", `/optimize/optimize/project/actual`, { "header": { "Content-Type": "application/json", }, })();
}

export function rootGet() {
  return request("get", `/`, { "header": { "Content-Type": "application/json", }, })();
}

