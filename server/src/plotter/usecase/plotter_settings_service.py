from enum import Enum
from typing import List
from pydantic.main import BaseModel
from src.plotter.domain.actual_plotter_communicator import ActualPlotterCommunicator, PlotterSettings
from src.plotter.domain.alert import AlertType
from src.plotter.infrastructure.alert_repository import AlertRepository
from src.plotter.infrastructure.plotter_settings_repository import PlotterSettingsRepository

class PlotterSettingsResponse(BaseModel):
    is_success: bool
    message: str
    
class PlotterSettingsInput(BaseModel):
    speedOfMotors: int
    speedOfZ: int
    
class PlotterSettingsModel(BaseModel):
    speedOfMotors: int
    speedOfZ: int
    
    
class PlotterSettingsService:
    def __init__(self, settings_repository: PlotterSettingsRepository, actual_plotter: ActualPlotterCommunicator) -> None:
        self.settings_repository: PlotterSettingsRepository = settings_repository
        self.actual_plotter: ActualPlotterCommunicator = actual_plotter

    async def get_settings(self) -> PlotterSettingsModel:
        settings = self.settings_repository.get_settings()
        return PlotterSettingsModel(speedOfMotors=settings.speed_of_motors, speedOfZ=settings.speed_of_Z)
    
    async def set_settings(self, settings: PlotterSettingsInput) -> PlotterSettingsResponse:
        if(self.actual_plotter.is_connected()):
            self.actual_plotter.send_settings(PlotterSettings(settings.speedOfMotors, settings.speedOfZ))
            return PlotterSettingsResponse(is_success=True, message="")
            
        return PlotterSettingsResponse(is_success=False, message="Plotter nie jest połączony")