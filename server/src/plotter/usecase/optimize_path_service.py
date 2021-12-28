from typing import List

from numpy import ndarray
from src.plotter.domain.command_group import CommandGroup
from src.plotter.domain.plotter import Plotter
from src.plotter.domain.project import OptimizationMethod
from src.plotter.infrastructure.plotter_repository import PlotterRepository

class OptimizePathService:
    def __init__(self, plotter_repository: PlotterRepository) -> None:
        self.plotter_repository: PlotterRepository = plotter_repository

    def optimize_command_group_path(self, labels: ndarray, unique_labels: List[int], plotter: Plotter, command_groups: List[CommandGroup]):
        plotter.project.optimize_command_group_path(labels, unique_labels, OptimizationMethod.TabuSearch, command_groups)
        self.plotter_repository.update_plotter(plotter)
        
    def optimize_path(self, plotter: Plotter):
        plotter.project.optimize_path(OptimizationMethod.DoNotOptimize)
        self.plotter_repository.update_plotter(plotter)
        