type RequestResult<Data> = Promise<{ response: Response; data: Data; }>;

type GetAllCommandsPlotterCommandsAllGetResult0 = RequestResult<({ "positionX": number; "positionY": number; })[]>;
/**
* Get All Commands
*/
export function getAllCommandsPlotterCommandsAllGet(): GetAllCommandsPlotterCommandsAllGetResult0;

type GetProjectImagePlotterProjectCurrentImageGetResult0 = RequestResult<string>;
/**
* Get Project Image
*/
export function getProjectImagePlotterProjectCurrentImageGet(): GetProjectImagePlotterProjectCurrentImageGetResult0;

type StartProjectPlotterProjectStartPostResult0 = RequestResult<object>;
/**
* Start Project
*/
export function startProjectPlotterProjectStartPost(): StartProjectPlotterProjectStartPostResult0;

type PauseProjectPlotterProjectPausePostResult0 = RequestResult<object>;
/**
* Pause Project
*/
export function pauseProjectPlotterProjectPausePost(): PauseProjectPlotterProjectPausePostResult0;

type StopProjectPlotterProjectStopPostResult0 = RequestResult<object>;
/**
* Stop Project
*/
export function stopProjectPlotterProjectStopPost(): StopProjectPlotterProjectStopPostResult0;

type GetPositionPlotterPositionGetResult0 = RequestResult<{ "positionX": number; "positionY": number; }>;
/**
* Get Position
*/
export function getPositionPlotterPositionGet(): GetPositionPlotterPositionGetResult0;

type GetModePlotterPlotterModeGetResult0 = RequestResult<"Simulation" | "Work">;
/**
* Get Mode
*/
export function getModePlotterPlotterModeGet(): GetModePlotterPlotterModeGetResult0;

type SetModePlotterPlotterModePostParams0 = { "query": { "input": "Simulation" | "Work"; }; };
type SetModePlotterPlotterModePostResult0 = RequestResult<object>;
/**
* Set Mode
*/
export function setModePlotterPlotterModePost(params: SetModePlotterPlotterModePostParams0): SetModePlotterPlotterModePostResult0;

type GetWorkModePlotterPlotterWorkModeGetResult0 = RequestResult<"Automatic" | "Manual">;
/**
* Get Work Mode
*/
export function getWorkModePlotterPlotterWorkModeGet(): GetWorkModePlotterPlotterWorkModeGetResult0;

type IsConnectedPlotterPlotterPlotterConnectGetResult0 = RequestResult<boolean>;
/**
* Is Connected Plotter
*/
export function isConnectedPlotterPlotterPlotterConnectGet(): IsConnectedPlotterPlotterPlotterConnectGetResult0;

type ConnectToPlotterPlotterPlotterConnectPostParams0 = { "body"?: { "port": string; "baudrate": number; "timeout": number; }; };
type ConnectToPlotterPlotterPlotterConnectPostResult0 = RequestResult<object>;
/**
* Connect To Plotter
*/
export function connectToPlotterPlotterPlotterConnectPost(params: ConnectToPlotterPlotterPlotterConnectPostParams0): ConnectToPlotterPlotterPlotterConnectPostResult0;

type SendCommandPlotterCommandPostParams0 = { "body"?: { "command": string; }; };
type SendCommandPlotterCommandPostResult0 = RequestResult<{ "isSuccess": boolean; "message": string; }>;
/**
* Send Command
*/
export function sendCommandPlotterCommandPost(params: SendCommandPlotterCommandPostParams0): SendCommandPlotterCommandPostResult0;

type AddImageImageAddImagePostParams0 = { "body"?: { "name": string; "content": string; }; };
type AddImageImageAddImagePostResult0 = RequestResult<object>;
/**
* Add Image
*/
export function addImageImageAddImagePost(params: AddImageImageAddImagePostParams0): AddImageImageAddImagePostResult0;

type RootGetResult0 = RequestResult<object>;
/**
* Root
*/
export function rootGet(): RootGetResult0;

