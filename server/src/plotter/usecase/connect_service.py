from pubsub import pub
from pymitter import EventEmitter
from src.plotter.domain.actual_plotter_communicator import ActualPlotterCommunicator
from src.plotter.domain.command import Command, CommandStatus
from pydantic import BaseModel
from src.plotter.domain.controller import Controller, Mode
from src.plotter.domain.plotter_communicator_interface import ConnectionSettings
from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.domain.simulation_plotter_communicator import SimulationPlotterCommunicator

from src.plotter.infrastructure.plotter_repository import PlotterRepository
from src.plotter.infrastructure.project_repository import ProjectRepository
import asyncio
from multiprocessing import Process
import time


class ConnectionSettingsInput(BaseModel):
    port: str
    baudrate: int
    timeout: float
    
    
class ConnectService:

    def __init__(self,
                 plotter_repository: PlotterRepository,
                 actual_plotter: ActualPlotterCommunicator,
                 simulation_plotter: SimulationPlotterCommunicator) -> None:
        self.plotter_repository: PlotterRepository = plotter_repository
        self.actual_plotter: ActualPlotterCommunicator = actual_plotter
        self.simulation_plotter: SimulationPlotterCommunicator = simulation_plotter

    async def connect(self, connection_settings: ConnectionSettingsInput):
        plotter = self.plotter_repository.get_plotter()
        
        self.actual_plotter.connect(ConnectionSettings(connection_settings.port, connection_settings.baudrate, connection_settings.timeout))
        self.simulation_plotter.connect(ConnectionSettings(connection_settings.port, connection_settings.baudrate, connection_settings.timeout))
        plotter.connect()
        
        self.plotter_repository.update_plotter(plotter)
        
    async def is_connected(self) -> bool:
        plotter = self.plotter_repository.get_plotter()
        return plotter.is_connected()