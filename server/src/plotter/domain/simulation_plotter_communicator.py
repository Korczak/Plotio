from typing import List, Optional
from src.plotter.domain.plotter_communicator_interface import *

from src.plotter.domain.plotter_position import PlotterPosition
from pymitter import EventEmitter
from pubsub import pub

import asyncio
import json


class SimulationPlotterCommunicator(PlotterCommunicatorInterface):
    def __init__(self) -> None:
        self.position: PlotterPosition = PlotterPosition(0, 0, 0)
    
    def get_response(self) -> PlotterResponse:
        return PlotterResponse(False, True, self.position)

    def connect(self, connection_settings: ConnectionSettings) -> bool:
        return True
    
    def is_connected(self) -> bool:
        return True
    
    def send_command(self, position: PlotterPosition):
        self.position = position
