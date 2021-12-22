from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.infrastructure.plotter_dto import PlotterDto
from src.plotter.domain.plotter import Plotter
from src.plotter.infrastructure.plotter_repository import PlotterRepository
from pubsub import pub


class PlotterPositionInput:
    position: PlotterPosition

class PlotterPositionService:
    def __init__(self, repository: PlotterRepository) -> None:
        self.plotter_repository: PlotterRepository = repository

    def subscribe(self):
        pub.subscribe(self.on_update_position, 'PositionUpdated')
        pub.subscribe(self.on_command_done, 'CommandDone')

    def on_update_position(self, arg1: PlotterPosition):
        plotter = self.plotter_repository.get_plotter()
        plotter.moveTo(arg1)
        self.plotter_repository.update_plotter(plotter)
        
    def on_command_done(self, arg1: PlotterPosition):
        plotter = self.plotter_repository.get_plotter()
        plotter.moveTo(arg1)
        plotter.complete_current_command()
        self.plotter_repository.update_plotter(plotter)
