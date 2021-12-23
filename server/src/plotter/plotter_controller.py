from typing import ContextManager, List
from fastapi import APIRouter, HTTPException, Depends
from fastapi_socketio import SocketManager
from config.container import *
from dependency_injector.wiring import Provide, inject

from config.shared import dependency
from src.plotter.infrastructure.plotter_dto import PlotterDto
from src.plotter.domain.plotter import Plotter
from src.plotter.module import PlotterModule
from src.plotter.infrastructure.plotter_repository import PlotterRepository
from src.plotter.usecase.connect_service import ConnectService, ConnectionSettingsInput, ConnectionSettingsResponse
from src.plotter.usecase.manual_command_service import ManualCommandInput, ManualCommandResponse, ManualCommandService
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
    await service.send_command(input)


# @socketio.event
# def my_event(message):
#     print('a')
#     emit('my_response', 'test')