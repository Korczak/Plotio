from typing import List
from src.plotter.domain.plotter import Plotter, PlotterMode, WorkMode
from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.domain.plotter_settings import PlotterSettings
from src.plotter.infrastructure.plotter_dto import PlotterDto
from src.plotter.infrastructure.plotter_settings_dto import PlotterSettingsDto
from src.plotter.infrastructure.project_repository import ProjectRepository


class PlotterSettingsRepository:    
    def __init__(self) -> None:
        self._settings_db: PlotterSettingsDto = PlotterSettingsDto(0, 0)

    def update_settings(self, settings: PlotterSettings):
        self._plotter_db = PlotterSettingsDto(settings.speed_of_motors, settings.speed_of_Z)
        
    def get_settings(self) -> PlotterSettings:
        return PlotterSettings(self._plotter_db.speed_of_motors, self._plotter_db.speed_of_Z)