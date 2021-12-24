from enum import Enum
from typing import List
from pydantic.main import BaseModel
from src.plotter.domain.plotter import Plotter
from src.plotter.infrastructure.plotter_repository import PlotterRepository

  
class ProgressInfoResponse(BaseModel):
    commandsDone: int
    commandsTotal: int
    
class ProgressInfoService:
    def __init__(self, plotter_repository: PlotterRepository) -> None:
        self.plotter_repository: PlotterRepository = plotter_repository

    async def get_progress(self) -> ProgressInfoResponse:
        plotter: Plotter = self.plotter_repository.get_plotter()
        if(plotter.project == None):
            return ProgressInfoResponse(commandsDone=0, commandsTotal=0)
        
        return ProgressInfoResponse(commandsDone=len(plotter.project.all_commands) - len(plotter.project.commands_to_do), commandsTotal=len(plotter.project.all_commands))
