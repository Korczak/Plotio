from typing import List, Optional
from src.plotter.domain.plotter_communicator_interface import *

from src.plotter.domain.plotter_position import PlotterPosition
from pymitter import EventEmitter
from pubsub import pub
import serial
import serial.tools.list_ports

import asyncio
import json


class ActualPlotterCommunicator(PlotterCommunicatorInterface):
    def __init__(self) -> None:
        self.connected = False
        self.position: PlotterPosition = PlotterPosition(0, 0, 0)
        
    def get_response(self) -> PlotterResponse:
        #print("elo1")
        if(self.is_connected() == False):
            return None
        #print("elo2")
        try:
            response = self.arduino.readline().decode()
            print(response)
            processed_response = response.split(",")
            return PlotterResponse(bool(int(processed_response[0])), bool(int(processed_response[1])), PlotterPosition(int(processed_response[2]), int(processed_response[3]), 0))
        except:
        	return None
        return None

    def connect(self, connection_settings: ConnectionSettings) -> bool:
        self.arduino = serial.Serial(port="COM6", baudrate=9600, timeout=.1)
        self.connected = True
        self.connection_settings: ConnectionSettings = connection_settings
        
        if(self.is_connected()):
            return True
            
        return False
        
    def is_connected(self) -> bool:
        return self.connected
        #myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        #print(myports[0,0])
        #if self.connection_settings.port not in myports:
        #    return False
        #return True
    
    def get_opened_ports(self) -> List[str]:
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        print(myports)
        return myports
    
    def send_command(self, position: PlotterPosition):
        text = f"{position.posX},{position.posY},{position.isHit}".encode()
        print(text)
        self.arduino.write(text)

