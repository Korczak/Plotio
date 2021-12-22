import enum
from typing import List, Optional

from pymitter import EventEmitter
from src.plotter.domain.plotter_communicator_interface import PlotterCommunicatorInterface
from src.plotter.domain.command import Command
from src.plotter.domain.plotter import Plotter

from src.plotter.domain.plotter_position import PlotterPosition


class Mode(enum.Enum):
    Manual= "Manual"
    Automatic= "Automatic"

class Controller:
    def __init__(self, mode: Mode, plotter: Plotter) -> None:
        self.mode: Mode = mode
        self.plotter = plotter

    def manual(self):
        self.mode = Mode.Manual

    def automatic(self):
        self.mode = Mode.Automatic