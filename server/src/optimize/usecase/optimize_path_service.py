from typing import List

from numpy import ndarray
from pubsub import pub
from src.events.events_name import EventsName
from src.events.project_optimalized import ProjectOptimized
from src.optimize.infrastructure.project_repository import ProjectRepository
from src.plotter.domain.command import Command
from src.plotter.domain.command_group import CommandGroup
from src.optimize.domain.optimize_project import OptimizationMethod, OptimizeProject
from src.plotter.domain.plotter_position import PlotterPosition

class OptimizePathService:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self.project_repository: ProjectRepository = project_repository

    async def optimize_command_group_path(self, optimization_method: OptimizationMethod = OptimizationMethod.DoNotOptimize):
        project: OptimizeProject = self.project_repository.get_active_project()
        
        if project == None: 
            return
        
        optimized_commands: List[Command[PlotterPosition]] = project.optimize_command_groups(optimization_method)
        
        self.project_repository.update_project(project)
        pub.sendMessage(EventsName.ProjectOptimalized, arg1=ProjectOptimized(optimized_commands))