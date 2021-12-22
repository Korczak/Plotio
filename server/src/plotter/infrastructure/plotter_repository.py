from typing import List
from src.plotter.domain.plotter import Plotter, PlotterMode, WorkMode
from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.infrastructure.plotter_dto import PlotterDto
from src.plotter.infrastructure.project_repository import ProjectRepository


class PlotterRepository:    
    def __init__(self, project_repository: ProjectRepository) -> None:
        self._plotter_db: PlotterDto = PlotterDto("Disconnected", PlotterMode.Simulation, WorkMode.Manual, PlotterPosition(0, 0, 0))
        self.project_repository = project_repository

    def update_plotter(self, plotter: Plotter):
        self._plotter_db = PlotterDto(plotter.status, plotter.plotter_mode, plotter.work_mode, plotter.position)
        if(plotter.project is not None):
            self.project_repository.update_project(plotter.project)
        
    def get_plotter(self) -> Plotter:
        project = self.project_repository.get_active_project()
        return Plotter(
            self._plotter_db.status, 
            PlotterPosition(self._plotter_db.posX, self._plotter_db.posY, self._plotter_db.isHit), 
            self._plotter_db.plotterMode, 
            self._plotter_db.workMode,
            project)

    def get_last_command(self) -> PlotterDto:
        return self._plotter_db[-1]
        
            
