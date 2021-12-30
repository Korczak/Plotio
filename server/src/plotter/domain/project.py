import enum
from typing import List, Optional

from numpy import ndarray
from numpy.core.fromnumeric import argmin
from numpy.lib.function_base import delete
from numpy.random.mtrand import f
from pubsub import pub
from src.events.events_name import EventsName
from src.optimize.domain.opimization_utils import *
from src.plotter.domain.command import Command
from src.plotter.domain.command_group import CommandGroup
import math

from src.plotter.domain.plotter_position import PlotterPosition


class OptimizationMethod(enum.Enum):
    TabuSearch = 'TabuSearch'
    SimulatedAnnealing = 'SimulatedAnnealing'
    DoNotOptimize = 'DoNotOptimize'

class ProjectStatus(enum.Enum):
    NotStarted = 'NotStarted'
    Ready = 'Ready'
    Running= 'Running'
    Idle = 'Idle'
    Paused= 'Paused'
    Stopped = 'Stopped'
    Completed = 'Completed'

class Project:
    def __init__(self, name: str, commands: List[Command]) -> None:
        self.name = name
        self.status: ProjectStatus = ProjectStatus.NotStarted
        self.all_commands: List[Command] = commands.copy()
        self.commands_to_do: List[Command] = []
        self.is_active = True
        self.image_content: ndarray = None

    def __init__(self, name: str, is_active: bool, status: ProjectStatus, all_commands: List[Command], commands_to_do: List[Command], image_content: ndarray, image_with_processed_commands: ndarray, image_shape: List[int]) -> None:
        self.name = name
        self.is_active: bool = is_active
        self.status: ProjectStatus = status
        self.all_commands: List[Command] = all_commands.copy()
        self.commands_to_do: List[Command] = commands_to_do.copy()
        self.image_content: ndarray = image_content.copy()
        self.image_with_processed_commands: ndarray = image_with_processed_commands.copy()
        self.image_shape: List[int] = image_shape

    def load_image(self, image_content: str):
        self.image_content = image_content

    def is_completed_project(self):
        return self.status == ProjectStatus.Completed

    def complete_project(self):
        self.is_active = False
        self.status = ProjectStatus.Completed
        pub.sendMessage(EventsName.ProjectCompleted)
        
    def stop_project(self):
        self.is_active = False
        self.status = ProjectStatus.Stopped
        pub.sendMessage(EventsName.ProjectStopped)
        
    def start_project(self) -> bool:
        if(len(self.commands_to_do) != 0 and (self.status == ProjectStatus.Ready or self.status == ProjectStatus.Paused)):
            if self.status == ProjectStatus.Ready:
                pub.sendMessage(EventsName.ProjectStarted)
            else:
                pub.sendMessage(EventsName.ProjectResumed)
            self.status = ProjectStatus.Running
            return True
        return False

    def pause_project(self):
        self.status = ProjectStatus.Paused
        pub.sendMessage(EventsName.ProjectPaused)

    def get_current_command(self) -> Command:
        if self.commands_to_do[0].is_running_command():
            return self.commands_to_do[0]
        return None

    def get_next_command(self) -> Command:
        return self.commands_to_do[0]
    
    def send_current_command(self) -> Command:
        self.commands_to_do[0].send_command()

    def complete_current_command(self) -> None:
        self.image_with_processed_commands[self.commands_to_do[0].command_detail.posY, self.commands_to_do[0].command_detail.posX] = 125
        self.commands_to_do[0].complete_command()
        self.commands_to_do.pop(0)
        if len(self.commands_to_do) == 0:
            self.complete_project()
        
    def optimize_command_groups(self, optimized_commands: List[Command[PlotterPosition]]):               
        self.all_commands = optimized_commands
        self.commands_to_do = optimized_commands
        self.status = ProjectStatus.Ready
        

