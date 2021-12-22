from enum import Enum
from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.infrastructure.plotter_dto import PlotterDto
from src.plotter.domain.plotter import Plotter, PlotterMode, WorkMode
from src.plotter.infrastructure.plotter_repository import PlotterRepository
from pubsub import pub

from src.plotter.infrastructure.project_repository import ProjectRepository

class PlotterModeEnum(str, Enum):
    Simulation = "Simulation"
    Work = "Work"

class PlotterWorkModeEnum(str, Enum):
    Automatic = "Automatic"
    Manual = "Manual"

class PlotterModeService:
    def __init__(self, plotter_repository: PlotterRepository) -> None:
        self.plotter_repository: PlotterRepository = plotter_repository

    def update_plotter_mode(self, input: PlotterModeEnum):
        plotter = self.plotter_repository.get_plotter()
        if(input == PlotterModeEnum.Simulation):
            plotter.setSimulationMode()
        elif(input == PlotterModeEnum.Work):
            plotter.setWorkMode()

        self.plotter_repository.update_plotter(plotter)

    def get_plotter_mode(self) -> PlotterModeEnum:
        plotter = self.plotter_repository.get_plotter()
        if(plotter.plotter_mode == PlotterMode.Work):
            return PlotterModeEnum.Work
        return PlotterModeEnum.Simulation

    def get_plotter_work_mode(self) -> PlotterWorkModeEnum:
        plotter = self.plotter_repository.get_plotter()
        if(plotter.work_mode == WorkMode.Manual):
            return PlotterWorkModeEnum.Manual
        return PlotterWorkModeEnum.Automatic