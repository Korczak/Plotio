from enum import Enum
from pymitter import EventEmitter
from src.plotter.domain.command import Command
from src.plotter.domain.controller import Controller, Mode
from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.infrastructure.plotter_dto import PlotterDto
from src.plotter.domain.plotter import Plotter, PlotterStatus
from src.plotter.infrastructure.plotter_repository import PlotterRepository
from pydantic import BaseModel
from src.plotter.domain.simulation_plotter_communicator import SimulationPlotterCommunicator
from src.plotter.domain.actual_plotter_communicator import ActualPlotterCommunicator


class DirectionEnum(str, Enum):
    X = 'X'
    Y = 'Y'
class PositionCommandInput(BaseModel):
    position: int
    direction: DirectionEnum
    
class ManualCommandInput(BaseModel):
    command: str

class ManualCommandResponse(BaseModel):
    isSuccess: bool
    message: str

class ManualCommandService:

    def __init__(self, repository: PlotterRepository, event_emitter: EventEmitter, actual_plotter: ActualPlotterCommunicator, simulation_plotter: SimulationPlotterCommunicator) -> None:
        self.plotter_repository: PlotterRepository = repository
        self.event_emitter = event_emitter
        self.actual_plotter: ActualPlotterCommunicator = actual_plotter
        self.simulation_plotter: SimulationPlotterCommunicator = simulation_plotter

    async def send_command(self, input: ManualCommandInput) -> None:
        plotter = self.plotter_repository.get_plotter()
        controller = Controller(mode = Mode.Manual, plotter= plotter)

        current_position = plotter.position

        move_amount = 5
        if(input.command == "Up"):
            command = Command(PlotterPosition(current_position.posX, current_position.posY + move_amount, 0))
        elif(input.command == "Down"):
            command = Command(PlotterPosition(current_position.posX, current_position.posY - move_amount, 0))
        elif(input.command == "Left"):
            command = Command(PlotterPosition(current_position.posX - move_amount, current_position.posY, 0))
        elif(input.command == "Right"):
            command = Command(PlotterPosition(current_position.posX + move_amount, current_position.posY, 0))
        elif(input.command == "Hit"):
            command = Command(PlotterPosition(current_position.posX, current_position.posY, 1))
        else:
            return ManualCommandResponse(False)

        if(plotter.is_work_mode()):
            self.actual_plotter.send_command(command.command_detail)
        else:
            self.simulation_plotter.send_command(command.command_detail)
        return ManualCommandResponse(isSuccess=True, message="Command sent")
    
    async def move_to(self, input: PositionCommandInput) -> None:
        plotter = self.plotter_repository.get_plotter()
        controller = Controller(mode = Mode.Manual, plotter= plotter)
        current_position = plotter.position

        if(input.direction == DirectionEnum.X):
            command = Command(PlotterPosition(input.position, current_position.posY, 0))
        elif(input.direction == DirectionEnum.Y):
            command = Command(PlotterPosition(current_position.posX, input.position, 0))
            
        if(plotter.is_work_mode()):
            self.actual_plotter.send_command(command.command_detail)
        else:
            self.simulation_plotter.send_command(command.command_detail)
        return ManualCommandResponse(isSuccess=True, message="Command sent")
    
    async def positioning(self) -> ManualCommandResponse:
        plotter = self.plotter_repository.get_plotter()
        controller = Controller(mode = Mode.Manual, plotter= plotter)
        current_position = plotter.position
            
        if(plotter.is_work_mode()):
            self.actual_plotter.positioning()
        else:
            return ManualCommandResponse(isSuccess=False, message="Nie można przeprowadzić pozycjonowania w symulacji")
        return ManualCommandResponse(isSuccess=True, message="Command sent")
    
    async def zeroing(self) -> ManualCommandResponse:
        plotter = self.plotter_repository.get_plotter()
            
        if(plotter.is_work_mode()):
            self.actual_plotter.send_command(PlotterPosition(0, 0, 0))
        else:
            self.simulation_plotter.send_command(PlotterPosition(0, 0, 0))
        return ManualCommandResponse(isSuccess=True, message="Command sent")