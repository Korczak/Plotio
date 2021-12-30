from typing import List

from numpy import ndarray
from src.plotter.domain.command import Command
from src.plotter.domain.command_group import CommandGroup

class ProjectDto:
    def __init__(self, name: str, all_commands: List[Command], commands_to_do: List[Command], image_content: ndarray, labels: ndarray, unique_labels: List[int], command_groups: List[CommandGroup]) -> None:
        self.name = name
        self.all_commands: List[Command] = all_commands.copy()
        self.commands_to_do: List[Command] = commands_to_do
        self.image_content: ndarray = image_content
        self.labels: ndarray = labels
        self.unique_labels: List[int] = unique_labels
        self.command_groups: List[CommandGroup] = command_groups
