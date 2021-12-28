import math
from typing import List

import numpy as np

from src.plotter.domain.command_group import CommandGroup
from src.plotter.domain.opimization_utils import Point, get_distance
from src.plotter.domain.plotter_position import PlotterPosition


def get_nearest_object(current_position: PlotterPosition, command_groups: List[CommandGroup]):
    next_position: PlotterPosition = None
    min_distance: int = 99999
    command_group_id: int = 0
    
    for command_id, command_group in enumerate(command_groups):
        possible_position = [get_distance(Point(command.position.posX, command.position.posY, command.position.isHit), Point(current_position.posX, current_position.posY, current_position.isHit)) for command in command_group.commands]
        
        possible_position_min_id = np.argmin(possible_position)
        
        if min_distance > possible_position[possible_position_min_id]:
            min_distance = possible_position[possible_position_min_id]
            command_group_id = command_id
            next_position = command_group.commands[possible_position_min_id].position
            
    return next_position, command_group_id