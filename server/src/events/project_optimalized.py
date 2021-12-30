from typing import List

from src.plotter.domain.command import Command
from src.plotter.domain.plotter_position import PlotterPosition


class ProjectOptimized:
    def __init__(self, optimized_commands: List[Command[PlotterPosition]]) -> None:    
        self.optimized_commands: List[Command[PlotterPosition]] = optimized_commands