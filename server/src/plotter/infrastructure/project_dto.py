from typing import List

from numpy import ndarray
from src.plotter.domain.command import Command
from src.plotter.domain.project import ProjectStatus

class ProjectDto:
    def __init__(self, name: str, is_active: bool, status: ProjectStatus, all_commands: List[Command], commands_to_do: List[Command], previous_command: Command, image_content: ndarray, image_with_processed_commands: ndarray, image_shape: List[int], totalDistance:int, distanceCompleted: int) -> None:
        self.name = name
        self.totalDistance = totalDistance
        self.distanceCompleted = distanceCompleted
        self.previous_command: Command = previous_command
        self.is_active: bool = is_active
        self.status: ProjectStatus = status
        self.all_commands: List[Command] = all_commands
        self.commands_to_do: List[Command] = commands_to_do
        self.image_content: ndarray = image_content
        self.image_with_processed_commands: ndarray = image_with_processed_commands
        self.image_shape: List[int] = image_shape