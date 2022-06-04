import math
from typing import List

import numpy as np
from src.optimize.domain.opimization_utils import Point, PointWithCommands, get_distance

from src.plotter.domain.command_group import CommandGroup
from src.plotter.domain.plotter_position import PlotterPosition


def get_nearest_object(current_position: PlotterPosition, command_groups: List[CommandGroup], max_num_of_neighbors: int = 200):
    next_position: PlotterPosition = None
    min_distance: int = 99999
    command_group_id: int = 0
    
    for command_id, command_group in enumerate(command_groups):
        commands = command_group.commands
        if len(command_group.commands) > max_num_of_neighbors:
            commands = command_group.commands[:max_num_of_neighbors]
        possible_position = [get_distance(Point(command.command_detail.posX, command.command_detail.posY, command.command_detail.hitTimes), Point(current_position.posX, current_position.posY, current_position.hitTimes)) for command in commands]
        
        possible_position_min_id = np.argmin(possible_position)
        
        if min_distance > possible_position[possible_position_min_id]:
            min_distance = possible_position[possible_position_min_id]
            command_group_id = command_id
            next_position = command_group.commands[possible_position_min_id].command_detail
            
    return next_position, command_group_id


class GroupOfPoints:
    def __init__(self, posX: float, posY: float, commands: List[PointWithCommands]) -> None:
        self.posX: float = posX
        self.posY: float = posY
        self.commands: List[PointWithCommands] = commands
        
    def __str__(self) -> str:
        return f"({self.posX}, {self.posY})"
    
    def __eq__(self, other: object) -> bool:
        return self.posX == other.posX and self.posY == other.posY