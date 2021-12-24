from pubsub import pub
from pymitter import EventEmitter
from src.plotter.domain.actual_plotter_communicator import ActualPlotterCommunicator
from src.plotter.domain.command import Command, CommandStatus
from pydantic import BaseModel
from src.plotter.domain.controller import Controller, Mode
from src.plotter.domain.plotter import PlotterStatus, WorkMode
from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.domain.simulation_plotter_communicator import SimulationPlotterCommunicator

from src.plotter.infrastructure.plotter_repository import PlotterRepository
from src.plotter.infrastructure.project_repository import ProjectRepository
import asyncio
from multiprocessing import Process
import time

class AutomaticCommandService:

    def __init__(self,
                 plotter_repository: PlotterRepository,
                 project_repository: ProjectRepository, 
                 event_emitter: EventEmitter,
                 actual_plotter: ActualPlotterCommunicator,
                 simulation_plotter: SimulationPlotterCommunicator) -> None:
        self.plotter_repository: PlotterRepository = plotter_repository
        self.project_repository: ProjectRepository = project_repository
        self.event_emitter = event_emitter
        self.actual_plotter: ActualPlotterCommunicator = actual_plotter
        self.simulation_plotter: SimulationPlotterCommunicator = simulation_plotter

    async def send_to_controller(self):
        while(True):
            plotter = self.plotter_repository.get_plotter()
            command = plotter.get_next_command()
            if(command is not None and command.can_send_command()):
                #print("Automatic command service")
                if(command.try_send_command()):
                    plotter.send_current_command()
                    
                    controller = Controller(mode = Mode.Automatic, plotter= plotter)
                    if(plotter.is_work_mode()):
                        self.actual_plotter.send_command(command.position)
                    else:
                        self.simulation_plotter.send_command(command.position)
                        
                    
                    self.plotter_repository.update_plotter(plotter)

            await asyncio.sleep(0.1)

    async def receive_from_controller(self):
        while(True):
            plotter = self.plotter_repository.get_plotter()
            current_command = plotter.get_current_command()
            plotter_position: PlotterPosition = None
            
            #print("czytam")
            if(plotter.is_work_mode()):
                #print("arduino1")
                if plotter.status == PlotterStatus.Disconnected:
                    await asyncio.sleep(0.1)
                    continue
                #print("arduino2")

                plotter_response = self.actual_plotter.get_response()
                if plotter_response != None:
                    plotter_position = plotter_response.position
            else:
                plotter_response = self.simulation_plotter.get_response()
                if plotter_response != None:
                    plotter_position = plotter_response.position
                
            if(plotter_position is not None):
                pub.sendMessage('PositionUpdated', arg1=plotter_position)
            if(current_command is not None and plotter_response != None and plotter_response.isCommandDone == True):
                pub.sendMessage('CommandDone', arg1=plotter_position)
            
            await asyncio.sleep(0.1)
        
