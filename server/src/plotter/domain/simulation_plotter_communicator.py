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
        self.desired_position: PlotterPosition = PlotterPosition(0, 0, 0)
    
    def get_response(self) -> PlotterResponse:
        if abs(self.position.posX - self.desired_position.posX) < 5:
            self.position.posX = self.desired_position.posX
        else:
            if self.position.posX < self.desired_position.posX:
                self.position.posX = self.position.posX + 1
            else:
                self.position.posX = self.position.posX - 1    
        
        if abs(self.position.posY - self.desired_position.posY) < 5:
            self.position.posY = self.desired_position.posY
        else:
            if self.position.posY < self.desired_position.posY:
                self.position.posY = self.position.posY + 1
            else:
                self.position.posY = self.position.posY - 1    
        
        command_done = False
        if(self.position.posX == self.desired_position.posX and self.position.posY == self.desired_position.posY):
            command_done = True
        
        # self.position = self.desired_position
        return PlotterResponse(False, command_done, self.position)

    def connect(self, connection_settings: ConnectionSettings) -> bool:
        return True
    
    def is_connected(self) -> bool:
        return True
    
    def send_command(self, position: PlotterPosition):
        self.desired_position = position
