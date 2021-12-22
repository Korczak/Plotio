from pymitter import EventEmitter
from src.plotter.domain.command import Command
from src.plotter.domain.controller import Controller, Mode
from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.domain.simulation_plotter_communicator import SimulationPlotterCommunicator
from src.plotter.infrastructure.plotter_dto import PlotterDto
from src.plotter.domain.plotter import Plotter, PlotterStatus
from src.plotter.infrastructure.plotter_repository import PlotterRepository
from pydantic import BaseModel


class ManualCommandInput(BaseModel):
    command: str

class ManualCommandResponse(BaseModel):
    isSuccess: bool
    message: str

class ManualCommandService:

    def __init__(self, repository: PlotterRepository, event_emitter: EventEmitter) -> None:
        self.plotter_repository: PlotterRepository = repository
        self.event_emitter = event_emitter

    async def send_command(self, input: ManualCommandInput) -> None:
        plotter = self.plotter_repository.get_plotter()
        controller = Controller(mode = Mode.Manual, plotter= plotter)

        current_position = plotter.position

        move_amount = 5
        if(input.command == "Up"):
            command = Command(position=PlotterPosition(current_position.posX, current_position.posY + move_amount, 0))
        elif(input.command == "Down"):
            command = Command(position=PlotterPosition(current_position.posX, current_position.posY - move_amount, 0))
        elif(input.command == "Left"):
            command = Command(position=PlotterPosition(current_position.posX - move_amount, current_position.posY, 0))
        elif(input.command == "Right"):
            command = Command(position=PlotterPosition(current_position.posX + move_amount, current_position.posY, 0))
        else:
            return ManualCommandResponse(False)

        await controller.update_position(command, plotter_communicator=SimulationPlotterCommunicator(), eventEmitter=self.event_emitter)
        return ManualCommandResponse(isSuccess=True, message="Command sent")