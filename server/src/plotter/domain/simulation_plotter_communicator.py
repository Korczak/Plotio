from typing import List, Optional
from src.plotter.domain.plotter_communicator_interface import ConnectionSettings, PlotterCommunicatorInterface

from src.plotter.domain.plotter_position import PlotterPosition
from pymitter import EventEmitter
from pubsub import pub

import asyncio
import json


class SimulationPlotterCommunicator(PlotterCommunicatorInterface):
    def __init__(self) -> None:
        self.position: PlotterPosition = PlotterPosition(0, 0, 0)
    
    async def get_position(self) -> PlotterPosition:
        await asyncio.sleep(0.0001) 
        return self.position

    async def connect(self, connection_settings: ConnectionSettings) -> bool:
        return True
    
    async def is_connected(self) -> bool:
        return True
    
    async def send_command(self, position: PlotterPosition):
        self.position = position
