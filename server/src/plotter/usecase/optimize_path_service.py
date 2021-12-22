from src.plotter.domain.plotter import Plotter
from src.plotter.domain.project import OptimizationMethod
from src.plotter.infrastructure.plotter_repository import PlotterRepository

class OptimizePathService:
    def __init__(self, plotter_repository: PlotterRepository) -> None:
        self.plotter_repository: PlotterRepository = plotter_repository

    def optimize_path(self, plotter: Plotter):
        plotter.project.optimize_path(OptimizationMethod.DoNotOptimize)
        self.plotter_repository.update_plotter(plotter)
        