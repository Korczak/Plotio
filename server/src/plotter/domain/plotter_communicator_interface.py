from typing import List, Optional

from src.plotter.domain.plotter_position import PlotterPosition
from pymitter import EventEmitter


class ConnectionSettings:
    def __init__(self, port: str, baudrate: int, timeout: float) -> None:
        self.port: str = port
        self.baudrate: int = baudrate
        self.timeout: float = timeout

class PlotterResponse:
    def __init__(self, alarmStatus: bool, isCommandDone: bool, position: PlotterPosition) -> None:
        self.alarmStatus: bool = alarmStatus
        self.isCommandDone: int = isCommandDone
        self.position: PlotterPosition = position

class PlotterCommunicatorInterface:
    async def get_response(self) -> PlotterResponse:
        pass
    async def connect(self, connection_settings: ConnectionSettings) -> bool:
        pass
    async def is_connected(self) -> bool:
        pass
    async def send_command(self, position: PlotterPosition):
        pass

