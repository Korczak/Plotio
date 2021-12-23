from typing import List, Optional
from src.plotter.domain.plotter_communicator_interface import ConnectionSettings, PlotterCommunicatorInterface

from src.plotter.domain.plotter_position import PlotterPosition
from pymitter import EventEmitter
from pubsub import pub
import serial
import serial.tools.list_ports

import asyncio
import json


class ActualPlotterCommunicator(PlotterCommunicatorInterface):
    def __init__(self) -> None:
        self.position: PlotterPosition = PlotterPosition(0, 0, 0)
        
    def get_position(self) -> PlotterPosition:
        if(self.is_connected()):
            return None
        
        response = self.arduino.readline().decode()
        print(response)
        self.position.posX = self.position.posX + 1
        
        return self.position

    def connect(self, connection_settings: ConnectionSettings) -> bool:
        self.arduino = serial.Serial(port=connection_settings.port, baudrate=connection_settings.baudrate, timeout=connection_settings.timeout)
        self.connection_settings: ConnectionSettings = connection_settings
        
        connection_attempts: int = 0
        while(connection_attempts < 5):
            if(self.is_connected()):
                return True
            
        return False
        
    def is_connected(self) -> bool:
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        if self.connection_settings.port not in myports:
            return False
        return True
    
    def get_opened_ports(self) -> List[str]:
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        return myports
    
    def send_command(self, position: PlotterPosition):
        self.arduino.write(f"{position.posX},{position.posY},{position.isHit}")
