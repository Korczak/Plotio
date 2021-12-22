
from typing import List

class Point:
    def __init__(self, posX: float, posY: float, hit: 0 | 1 = 1) -> None:
        self.posX: float = posX
        self.posY: float = posY
        self.hit: 0 | 1 = hit
        
    def __str__(self) -> str:
        return f"({self.posX}, {self.posY})"
    
    def __eq__(self, other: object) -> bool:
        return self.posX == other.posX and self.posY == other.posY

class Move:
    def __init__(self, point_a: Point, point_b: Point, point_a_index: int, point_b_index: int) -> None:
        self.point_a = point_a
        self.point_b = point_b
        self.point_a_index = point_a_index
        self.point_b_index = point_b_index
        
    def __str__(self) -> str:
        return f"({self.point_a.posX}, {self.point_a.posY}) -> ({self.point_b.posX}, {self.point_b.posY})"
    
    def __eq__(self, other: object) -> bool:
        if self.point_a == other.point_a and self.point_b == other.point_b:
            return True
        
        if self.point_a == other.point_b and self.point_b == other.point_a:
            return True
        
        return False

class PossibleMove:
    def __init__(self, move, value) -> None:
        self.move : Move = move
        self.value : int = value     
        
    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other: object) -> bool:
        if self.move == other.move:
            return True
        
        return False

def swap_points(solution: List[Point], i:Point, j: Point):       
    i_index = solution.index(i)
    j_index = solution.index(j)
    solution[i_index], solution[j_index] = solution[j_index], solution[i_index]
    return solution

def swap_indexes(solution: List[Point], i_index: int, j_index: int):       
    solution[i_index], solution[j_index] = solution[j_index], solution[i_index]
    return solution

def calculate_value_after_move(solution: List[Point], solution_value: int, move: Move):
    
    new_value = solution_value
    
    new_value = remove_point_from_solution(solution, move.point_a_index, new_value, move.point_a)
    new_value = remove_point_from_solution(solution, move.point_b_index, new_value, move.point_b)
    
    copied_solution = swap_indexes(solution, move.point_a_index, move.point_b_index)
    
    new_value = add_point_to_solution(copied_solution, move.point_a_index, new_value, move.point_b)
    new_value = add_point_to_solution(copied_solution, move.point_b_index, new_value, move.point_a)
    
    copied_solution = swap_indexes(solution, move.point_a_index, move.point_b_index)
    
    return new_value
    
def remove_point_from_solution(solution: List[Point], index_of_point: int, new_value: int, point: Point) -> int:
    if(index_of_point - 1 > 0):
        new_value = new_value - get_distance(solution[index_of_point - 1], point)
    if(index_of_point + 1 < len(solution)):
        new_value = new_value - get_distance(point, solution[index_of_point + 1])
    
    return new_value
    
def add_point_to_solution(solution: List[Point], index_of_point: int, new_value: int, point: Point) -> int:
    if(index_of_point - 1> 0):
        new_value = new_value + get_distance(solution[index_of_point - 1], point)
    if(index_of_point + 1< len(solution)):
        new_value = new_value + get_distance(point, solution[index_of_point + 1])
    
    return new_value


def get_distance(point_a: Point, point_b: Point):
    return max(abs(point_a.posX - point_b.posX), abs(point_a.posY - point_b.posY))

def calculate_value(solution: List[Point], show = False):
    value = 0
    current_pos = solution[0]
    
    for node in solution[1:]:
        value = value + get_distance(current_pos, node)
        current_pos = node
    
    
    if(show):
        solution_text = [str(sol) for sol in solution]
        print(f'Value of solution {solution_text} is {value}')
    
    return value