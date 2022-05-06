from typing import Any, List, Optional
from src.plotter.domain.command_details import CommandDetails
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
        self.step = 5
        self.max_width = 800
        self.max_height = 800
    
    def get_response(self) -> PlotterResponse:        
        if abs(self.position.posX - self.desired_position.posX) < self.step:
            self.position.posX = self.desired_position.posX
        else:
            if self.position.posX < self.desired_position.posX:
                self.position.posX = self.position.posX + self.step
            else:
                self.position.posX = self.position.posX - self.step  
        
        if abs(self.position.posY - self.desired_position.posY) < self.step:
            self.position.posY = self.desired_position.posY
        else:
            if self.position.posY < self.desired_position.posY:
                self.position.posY = self.position.posY + self.step
            else:
                self.position.posY = self.position.posY - self.step
        
        command_done = False
        if(self.position.posX == self.desired_position.posX and self.position.posY == self.desired_position.posY):
            command_done = True
        
        alarm_status = False
#        if(self.position.posX > self.max_width or self.position.posX < 0 or self.position.posY > self.max_height or self.position.posY < 0):
#            alarm_status = True
        
        return PlotterResponse(alarm_status, command_done, self.position)

    def connect(self, connection_settings: ConnectionSettings) -> bool:
        return True
    
    def is_connected(self) -> bool:
        return True
    
    def send_command(self, command_detail: Any):
        print("SEND COMMAND SIMULATION")
        if isinstance(command_detail, CommandDetails):
            if(command_detail.text == "RESET"):
                self.desired_position = PlotterPosition(0, 0, 0)
        elif isinstance(command_detail, PlotterPosition):
            self.desired_position = command_detail
