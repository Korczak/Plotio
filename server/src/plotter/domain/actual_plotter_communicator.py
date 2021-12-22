from typing import List, Optional
from src.plotter.domain.plotter_communicator_interface import ConnectionSettings, PlotterCommunicatorInterface

from src.plotter.domain.plotter_position import PlotterPosition
from pymitter import EventEmitter
from pubsub import pub
import serial

import asyncio
import json


class ActualPlotterCommunicator(PlotterCommunicatorInterface):
    def __init__(self) -> None:
        self.position: PlotterPosition = PlotterPosition(0, 0, 0)
        
    async def get_position(self) -> PlotterPosition:
        if(self.is_connected()):
            return None
        
        response = self.arduino.readline().decode()
        print(response)
        self.position.posX = self.position.posX + 1
        
        return self.position

    async def connect(self, connection_settings: ConnectionSettings) -> bool:
        self.arduino = serial.Serial(port=self.connection_settings.port, baudrate=self.connection_settings.baudrate, timeout=self.connection_settings.timeout)
        self.connection_settings: ConnectionSettings = connection_settings
        return True
        
    async def is_connected(self) -> bool:
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        if self.connection_settings.port not in myports:
            return False
        return True
    
    async def send_command(self, position: PlotterPosition):
        self.arduino.write(f"KOMENDA {position.posX}, {position.posY}, {position.isHit}")
