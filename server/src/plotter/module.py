from pymitter import EventEmitter
from src.plotter.adapter.image_adapter import ImageAdapter
from src.plotter.adapter.optimize_adapter import OptimizeAdapter
from src.plotter.domain.actual_plotter_communicator import ActualPlotterCommunicator
from src.plotter.domain.simulation_plotter_communicator import SimulationPlotterCommunicator
from src.plotter.infrastructure.alarm_repository import AlarmRepository
from src.plotter.infrastructure.alert_repository import AlertRepository
from src.plotter.infrastructure.plotter_settings_repository import PlotterSettingsRepository
from src.plotter.infrastructure.project_repository import ProjectRepository
from src.plotter.usecase.alarm_service import AlarmService
from src.plotter.usecase.alert_service import AlertService
from src.plotter.usecase.automatic_command_service import AutomaticCommandService
from src.plotter.usecase.connect_service import ConnectService
from src.plotter.usecase.manual_command_service import ManualCommandInput, ManualCommandService
from src.optimize.usecase.optimize_path_service import OptimizePathService
from src.plotter.usecase.plotter_position_service import PlotterPositionService
from src.plotter.usecase.plotter_settings_service import PlotterSettingsService
from src.plotter.usecase.progress_info_service import ProgressInfoService
from src.plotter.usecase.project_save_service import ProjectSaveService
from src.plotter.usecase.project_service import ProjectService
from src.plotter.usecase.render_simaluation_service import RenderSimulationService
from src.plotter.infrastructure.plotter_repository import PlotterRepository
from dependency_injector import containers, providers

from src.plotter.usecase.plotter_mode_service import PlotterModeService


class PlotterModule(containers.DeclarativeContainer):
    alarm_repository=providers.Singleton(AlarmRepository)
    project_repository=providers.Singleton(ProjectRepository)
    plotter_repository=providers.Singleton(PlotterRepository, project_repository=project_repository, alarm_repository=alarm_repository)
    alert_repository = providers.Singleton(AlertRepository)
    plotter_settings_repository = providers.Singleton(PlotterSettingsRepository)
    actual_plotter = providers.Singleton(ActualPlotterCommunicator)
    simulation_plotter = providers.Singleton(SimulationPlotterCommunicator)
    
    plotter_position_service = providers.Singleton(PlotterPositionService, repository=plotter_repository, alert_repository=alert_repository, actual_plotter = actual_plotter, simulation_plotter = simulation_plotter)
    render_simulation_service = providers.Singleton(RenderSimulationService, plotter_repository=plotter_repository, project_repository=project_repository)
    plotter_mode_service = providers.Singleton(PlotterModeService, plotter_repository=plotter_repository)
    project_service = providers.Singleton(ProjectService, plotter_repository=plotter_repository, project_repository = project_repository, alert_repository=alert_repository)
    project_save_service = providers.Singleton(ProjectSaveService, plotter_repository=plotter_repository, project_repository = project_repository)
    alert_service = providers.Singleton(AlertService, alert_repository=alert_repository)    
    progress_info_service = providers.Singleton(ProgressInfoService, plotter_repository=plotter_repository, plotter_settings_repository = plotter_settings_repository)
    alarm_service = providers.Singleton(AlarmService, alarm_repository=alarm_repository, plotter_repository = plotter_repository)

    
    automatic_command_service = providers.Singleton(AutomaticCommandService, 
                                                    plotter_repository=plotter_repository, 
                                                    project_repository=project_repository, 
                                                    event_emitter=providers.ProvidedInstance(EventEmitter),
                                                    actual_plotter = actual_plotter,
                                                    simulation_plotter = simulation_plotter
                                                    )
    
    connect_service = providers.Singleton(ConnectService,
                                          plotter_repository=plotter_repository,
                                          actual_plotter = actual_plotter,
                                          simulation_plotter = simulation_plotter, 
                                          alert_repository=alert_repository)
    
    plotter_settings_service = providers.Singleton(PlotterSettingsService, settings_repository=plotter_settings_repository, actual_plotter = actual_plotter)
    
    
    manual_command_service = providers.Singleton(
        ManualCommandService,
        repository=plotter_repository,
        event_emitter=providers.ProvidedInstance(EventEmitter),
        actual_plotter = actual_plotter,
        simulation_plotter = simulation_plotter
    )

    image_adapter = providers.Singleton(
        ImageAdapter, 
        project_repository=project_repository, 
        plotter_repository=plotter_repository)
    optimize_adapter = providers.Singleton(OptimizeAdapter, project_repository=project_repository)

