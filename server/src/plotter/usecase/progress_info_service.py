from enum import Enum
from typing import List
from pydantic.main import BaseModel
from src.plotter.domain.plotter import Plotter
from src.plotter.domain.plotter_settings import PlotterSettings
from src.plotter.infrastructure.plotter_repository import PlotterRepository
from src.plotter.infrastructure.plotter_settings_repository import PlotterSettingsRepository

  
class ProgressInfoResponse(BaseModel):
    commandsDone: int
    commandsTotal: int
    durationLeft: float
    
class ProgressInfoService:
    def __init__(self, plotter_repository: PlotterRepository, plotter_settings_repository: PlotterSettingsRepository) -> None:
        self.plotter_repository: PlotterRepository = plotter_repository
        self.plotter_settings_repository = plotter_settings_repository

    async def get_progress(self) -> ProgressInfoResponse:
        settings: PlotterSettings = self.plotter_settings_repository.get_settings()
        plotter: Plotter = self.plotter_repository.get_plotter()
        if(plotter.project == None):
            return ProgressInfoResponse(durationLeft=0,commandsDone=0, commandsTotal=0)
        
        pixel_per_time = 0.006 / 500 * settings.speed_of_motors
        distance_duration = plotter.project.get_distance_to_complete()*settings.pixel_density*pixel_per_time
        hammer_duration = plotter.project.get_commands_count() * 0.1
        duration_left = (distance_duration+hammer_duration)/60
        #print(plotter.project.get_distance_to_complete())
        #print(distance_duration)
        #print(hammer_duration)
        return ProgressInfoResponse(durationLeft=duration_left,commandsDone=len(plotter.project.all_commands) - len(plotter.project.commands_to_do), commandsTotal=len(plotter.project.all_commands))
