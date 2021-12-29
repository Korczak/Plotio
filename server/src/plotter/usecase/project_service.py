from enum import Enum
from pydantic import BaseModel
from src.plotter.domain.alert import Alert, AlertType
from src.plotter.infrastructure.alert_repository import AlertRepository
from src.plotter.infrastructure.plotter_repository import PlotterRepository

from src.plotter.infrastructure.project_repository import ProjectRepository

class ProjectCommands(str, Enum):
    Start = "Start"
    Pause = "Pause"
    Stop = "Stop"


class ProjectService:
    def __init__(self, plotter_repository : PlotterRepository, project_repository: ProjectRepository, alert_repository: AlertRepository) -> None:
        self.plotter_repository: PlotterRepository = plotter_repository
        self.project_repository : ProjectRepository = project_repository
        self.alert_repository: AlertRepository = alert_repository

    def start_project(self):
        plotter = self.plotter_repository.get_plotter()
        plotter.start_project()
        self.plotter_repository.update_plotter(plotter)
        
    def stop_project(self):
        plotter = self.plotter_repository.get_plotter()
        plotter.stop_project()
        self.plotter_repository.update_plotter(plotter)

    def pause_project(self):
        plotter = self.plotter_repository.get_plotter()
        plotter.pause_project()
        self.plotter_repository.update_plotter(plotter)



