import math
from typing import List

from src.optimize.domain.opimization_utils import *


class PreprocessCommandsToOptimization:
    def __init__(self, initial_solution: List[Point], number_of_rows: int, number_of_cols: int, max_width: int, max_height: int) -> None:
        self.initial_solution: List[Point] = initial_solution
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self.max_width = max_width
        self.max_height = max_height
        self.cell_width = max_width / number_of_rows
        self.cell_height = max_height / number_of_cols
        
    def extract_groups(self, ):
        extracted_groups: List[Point] = []
        
        for row in range(self.number_of_rows):
            for col in range(self.number_of_cols):
                group_contain_command = self.group_contain_command(row, col)
                
                if group_contain_command:
                    extracted_groups.append(Point(row, col))
        
        #extracted_groups.append(extracted_groups[0])
        return extracted_groups
                
    def group_contain_command(self, row: int, col: int) -> bool:
        start_width, start_height, end_width, end_height = self.get_boundaries_for_group(row, col)
        
        for command in self.initial_solution:
            if command.posX >= start_width and command.posX < end_width and command.posY >= start_height and command.posY < end_height:
                return True
        
        return False 
    
    def get_boundaries_for_group(self, row:int, col:int):
        return row * self.cell_width, col* self.cell_height, (row + 1) * self.cell_width, (col + 1) * self.cell_height


    def get_commands_for_group(self, row: int, col: int) -> List[Point]:
        start_width, start_height, end_width, end_height = self.get_boundaries_for_group(row, col)
        points_in_group: List[Point] = []

        for command in self.initial_solution:
            if command.posX >= start_width and command.posX < end_width and command.posY >= start_height and command.posY < end_height:
                points_in_group.append(command)
                
        return points_in_group