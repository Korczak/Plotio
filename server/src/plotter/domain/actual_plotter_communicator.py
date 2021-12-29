from typing import Any, List, Optional
from src.plotter.domain.command_details import CommandDetails
from src.plotter.domain.plotter_communicator_interface import *

from src.plotter.domain.plotter_position import PlotterPosition
from pymitter import EventEmitter
from pubsub import pub
import serial
import serial.tools.list_ports

import asyncio
import json

from src.plotter.domain.plotter_settings import PlotterSettings

class ActualPlotterCommunicator(PlotterCommunicatorInterface):
    def __init__(self) -> None:
        self.connected = False
        self.position: PlotterPosition = PlotterPosition(0, 0, 0)
        
    def get_response(self) -> PlotterResponse:
        if(self.is_connected() == False):
            return None
        try:
            response = self.arduino.readline().decode()
            print(response)
            processed_response = response.split(",")
            return PlotterResponse(bool(int(processed_response[0])), bool(int(processed_response[1])), PlotterPosition(int(processed_response[2]), int(processed_response[3]), 0))
        except:
        	return None
        return None

    def connect(self, connection_settings: ConnectionSettings) -> bool:
        self.arduino = serial.Serial(port=connection_settings.port, baudrate=connection_settings.baudrate, timeout=connection_settings.timeout)
        self.connected = True
        self.connection_settings: ConnectionSettings = connection_settings
        
        if(self.is_connected()):
            return True
            
        return False
        
    def is_connected(self) -> bool:
        myports = [p.device for p in list(serial.tools.list_ports.comports())]
        if self.connection_settings.port not in myports:
            return False
        return True
    
    def get_opened_ports(self) -> List[str]:
        myports = [p.device for p in list(serial.tools.list_ports.comports())]
        return myports
    
    def send_command(self, command_detail: Any):
        if isinstance(command_detail, CommandDetails):
            text = f"{command_detail.text}".encode()
            print(text)
            self.arduino.write(text)
        elif isinstance(command_detail, PlotterPosition):
            text = f"KOMENDA,{command_detail.posX},{command_detail.posY},{command_detail.isHit}".encode()
            print(text)
            self.arduino.write(text)
           
    def send_settings(self, settings: PlotterSettings):
        command = f"USTAWIENIA,{settings.speed_of_motors},{settings.speed_of_Z}".encode()
        self.arduino.write(command)
        
    def positioning(self):
        command = "POZYCJONOWANIE".encode()
        self.arduino.write(command)

