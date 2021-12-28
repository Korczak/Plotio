from src.plotter.domain.alert import Alert, AlertType
from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.infrastructure.alert_repository import AlertRepository
from src.plotter.infrastructure.plotter_dto import PlotterDto
from src.plotter.domain.plotter import Plotter
from src.plotter.infrastructure.plotter_repository import PlotterRepository
from pubsub import pub
from src.plotter.domain.simulation_plotter_communicator import SimulationPlotterCommunicator
from src.plotter.domain.actual_plotter_communicator import ActualPlotterCommunicator


class PlotterPositionInput:
    position: PlotterPosition

class PlotterPositionService:
    def __init__(self, 
                 repository: PlotterRepository, 
                 alert_repository: AlertRepository, 
                 actual_plotter: ActualPlotterCommunicator,
                 simulation_plotter: SimulationPlotterCommunicator) -> None:
        self.plotter_repository: PlotterRepository = repository
        self.alert_repository: AlertRepository = alert_repository
        self.actual_plotter: ActualPlotterCommunicator = actual_plotter
        self.simulation_plotter: SimulationPlotterCommunicator = simulation_plotter

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
        
        command = plotter.get_next_command()
        
        if(command is not None and command.can_send_command()):
            if(command.try_send_command()):
                plotter.send_current_command()
                
                if(plotter.is_work_mode()):
                    self.actual_plotter.send_command(command.position)
                else:
                    self.simulation_plotter.send_command(command.position) 

        if(plotter.project.is_completed_project()):
            self.alert_repository.add_alert(Alert("Ukończono projekt", AlertType.Success))
        
        self.plotter_repository.update_plotter(plotter)
