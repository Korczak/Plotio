from typing import List
from fastapi import APIRouter
from config.container import *
from dependency_injector.wiring import  inject

from config.shared import dependency
from src.plotter.domain.plotter_settings import PlotterSettings
from src.plotter.usecase.alarm_service import AlarmResponse, AlarmService
from src.plotter.usecase.alert_service import AlertResponse, AlertService
from src.plotter.usecase.connect_service import ConnectService, ConnectionSettingsInput, ConnectionSettingsResponse
from src.plotter.usecase.manual_command_service import ManualCommandInput, ManualCommandResponse, ManualCommandService, PositionCommandInput
from src.plotter.usecase.plotter_settings_service import PlotterSettingsInput, PlotterSettingsModel, PlotterSettingsResponse, PlotterSettingsService
from src.plotter.usecase.progress_info_service import ProgressInfoResponse, ProgressInfoService
from src.plotter.usecase.project_service import ProjectService
from src.plotter.usecase.render_simaluation_service import PlotterPosition, RenderSimulationService
from src.plotter.usecase.plotter_mode_service import PlotterModeEnum, PlotterModeService, PlotterWorkModeEnum

router = APIRouter(
    prefix="/plotter",
    tags=["plotter"],
    responses={404: {"description": "Not found"}},
)


#@router.get("/")
#@inject
#async def get_plotters(repository: PlotterRepository = dependency(Container.plotter.plotter_repository)):
#    return repository.getAll()

@router.get("/commands/all", response_model=List[PlotterPosition])
@inject
async def get_all_commands(service: RenderSimulationService = dependency(Container.plotter.render_simulation_service)):
    return service.get_all_commands()

@router.get("/project/current/image", response_model=str)
@inject
async def get_project_image(service: RenderSimulationService = dependency(Container.plotter.render_simulation_service)):
    image_content = service.get_original_image()
    return image_content

@router.get("/project/current/processed-image", response_model=str)
@inject
async def get_project_image(service: RenderSimulationService = dependency(Container.plotter.render_simulation_service)):
    image_content = service.get_image_with_processed_commands()
    return image_content

@router.post("/project/start")
@inject
async def start_project(service: ProjectService = dependency(Container.plotter.project_service)):
    service.start_project()
    
@router.post("/project/pause")
@inject
async def pause_project(service: ProjectService = dependency(Container.plotter.project_service)):
    service.pause_project()
    
@router.post("/project/stop")
@inject
async def stop_project(service: ProjectService = dependency(Container.plotter.project_service)):
    service.stop_project()

@router.get("/position", response_model=PlotterPosition)
@inject
async def get_position(service: RenderSimulationService = dependency(Container.plotter.render_simulation_service)):
    return service.get_actual_position()

@router.get("/plotter/mode", response_model=PlotterModeEnum)
@inject
async def get_mode(service: PlotterModeService = dependency(Container.plotter.plotter_mode_service)):
    return service.get_plotter_mode()

@router.post("/plotter/mode")
@inject
async def set_mode(input: PlotterModeEnum, service: PlotterModeService = dependency(Container.plotter.plotter_mode_service)):
    return service.update_plotter_mode(input)


@router.get("/plotter/work/mode", response_model=PlotterWorkModeEnum)
@inject
async def get_work_mode(service: PlotterModeService = dependency(Container.plotter.plotter_mode_service)):
    return service.get_plotter_work_mode()


@router.get("/plotter/connect", response_model=bool)
@inject
async def is_connected_plotter(service: ConnectService = dependency(Container.plotter.connect_service)):
    return await service.is_connected()

@router.get("/plotter/connect/ports", response_model=List[str])
@inject
async def get_open_ports(service: ConnectService = dependency(Container.plotter.connect_service)):
    return await service.get_open_ports()

@router.post("/plotter/connect", response_model=ConnectionSettingsResponse)
@inject
async def connect_to_plotter(input: ConnectionSettingsInput, service: ConnectService = dependency(Container.plotter.connect_service)):
    return await service.connect(input)


@router.post("/command", response_model=ManualCommandResponse)
@inject
async def send_command(input: ManualCommandInput, service: ManualCommandService = dependency(Container.plotter.manual_command_service)):
    return await service.send_command(input)
    
@router.post("/command/move-to", response_model=ManualCommandResponse)
@inject
async def move_to_position(input: PositionCommandInput, service: ManualCommandService = dependency(Container.plotter.manual_command_service)):
    return await service.move_to(input)
    
@router.post("/command/positioning", response_model=ManualCommandResponse)
@inject
async def positioning(service: ManualCommandService = dependency(Container.plotter.manual_command_service)):
    return await service.positioning()
    
@router.post("/command/zeroing", response_model=ManualCommandResponse)
@inject
async def zeroing(service: ManualCommandService = dependency(Container.plotter.manual_command_service)):
    return await service.zeroing()
    
@router.get("/alerts", response_model=AlertResponse)
@inject
async def get_alerts(service: AlertService = dependency(Container.plotter.alert_service)):
    return await service.get_alerts()

@router.get("/progress/info", response_model=ProgressInfoResponse)
@inject
async def get_progress_info(service: ProgressInfoService = dependency(Container.plotter.progress_info_service)):
    return await service.get_progress()

@router.get("/plotter/settings", response_model=PlotterSettingsModel)
@inject
async def get_plotter_settings(service: PlotterSettingsService = dependency(Container.plotter.plotter_settings_service)):
    return await service.get_settings()

@router.post("/plotter/settings", response_model=PlotterSettingsResponse)
@inject
async def set_plotter_settings(input: PlotterSettingsInput, service: PlotterSettingsService = dependency(Container.plotter.plotter_settings_service)):
    return await service.set_settings(input)

@router.get("/plotter/alarm", response_model=AlarmResponse)
@inject
async def get_alarm(service: AlarmService = dependency(Container.plotter.alarm_service)):
    return await service.get_alarm()

@router.post("/plotter/alarm/reset")
@inject
async def reset_alarm(service: AlarmService = dependency(Container.plotter.alarm_service)):
    await service.reset_alarm()

@router.post("/plotter/alarm/ignore")
@inject
async def ignore_alarm(service: AlarmService = dependency(Container.plotter.alarm_service)):
    await service.ignore_alarm()


# @socketio.event
# def my_event(message):
#     print('a')
#     emit('my_response', 'test')