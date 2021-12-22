from typing import List
import math 


class Point:
    def __init__(self, posX: float, posY: float) -> None:
        self.posX: float = posX
        self.posY: float = posY
        
    def __str__(self) -> str:
        return f"({self.posX}, {self.posY})"
    
    def __eq__(self, other: object) -> bool:
        return self.posX == other.posX and self.posY == other.posY

class Move:
    def __init__(self, point_a: Point, point_b: Point) -> None:
        self.point_a = point_a
        self.point_b = point_b
        
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


class PlotioTabuSearch():
    def __init__(self, initial_solution: List[Point], tabu_tenure: int, is_first_and_last_element_static: bool = True) -> None:
        self.solution: List[Point] = initial_solution
        self.solution_score: int = self.calculate_value(initial_solution)
        self.best_solution: List[Point] = initial_solution
        self.best_score: int = self.calculate_value(initial_solution)
        self.tabu_tenure: int = tabu_tenure
        self.restricted_moves: List[Move] = []       
        self.is_first_and_last_element_static = is_first_and_last_element_static
        
    def get_distance(self, point_a: Point, point_b: Point):
        return max(abs(point_a.posX - point_b.posX), abs(point_a.posY - point_b.posY))
        
    def calculate_value(self, solution: List[Point], show = False):
        value = 0
        current_pos = self.solution[0]
        
        for node in solution[1:]:
            value = value + self.get_distance(current_pos, node)
            current_pos = node
        
        
        if(show):
            solution_text = [str(sol) for sol in solution]
            print(f'Value of solution {solution_text} is {value}')
        
        return value
    
    def swap_points(self, solution: List[Point], i:Point, j: Point):
        solution = solution.copy()
        
        i_index = solution.index(i)
        j_index = solution.index(j)
        solution[i_index], solution[j_index] = solution[j_index], solution[i_index]
        return solution
    
    def calculate_value_after_move(self, solution: List[Point], solution_value: int, move: Move):
        copied_solution = solution.copy()
        
        point_a_index = solution.index(move.point_a)
        point_b_index = solution.index(move.point_b)
        
        new_value = solution_value
        
        new_value = self.remove_point_from_solution(copied_solution, point_a_index, new_value, move.point_a)
        new_value = self.remove_point_from_solution(copied_solution, point_b_index, new_value, move.point_b)
        
        copied_solution = self.swap_points(copied_solution, move.point_a, move.point_b)
        
        new_value = self.add_point_to_solution(copied_solution, point_a_index, new_value, move.point_b)
        new_value = self.add_point_to_solution(copied_solution, point_b_index, new_value, move.point_a)
        
        return new_value
        
    def remove_point_from_solution(self, solution: List[Point], index_of_point: int, new_value: int, point: Point) -> int:
        if(index_of_point - 1 > 0):
            new_value = new_value - self.get_distance(solution[index_of_point - 1], point)
        if(index_of_point + 1 < len(solution)):
            new_value = new_value - self.get_distance(point, solution[index_of_point + 1])
        
        return new_value
        
    def add_point_to_solution(self, solution: List[Point], index_of_point: int, new_value: int, point: Point) -> int:
        if(index_of_point - 1> 0):
            new_value = new_value + self.get_distance(solution[index_of_point - 1], point)
        if(index_of_point + 1< len(solution)):
            new_value = new_value + self.get_distance(point, solution[index_of_point + 1])
        
        return new_value
    
    def is_in_neighbour(self, index_of_point_a: int, index_of_point_b: int):
        return abs(index_of_point_a - index_of_point_b) == 1
    
    def get_neighbours(self, solution: List[Point], solution_value: int) -> List[PossibleMove]:
        possible_moves: List[Move] = []
        
        starting_index = 0
        ending_index = len(solution) 
        
        if self.is_first_and_last_element_static:
            starting_index = 1
            ending_index = len(solution) - 1
        
        for i in range(starting_index, ending_index):
            for j in range(i + 1, ending_index):
                move = Move(solution[i], solution[j])
                new_value = self.calculate_value_after_move(solution, solution_value, move)
                possible_moves.append(PossibleMove(move, new_value))
                
        return possible_moves
        
        
    def optimize(self, max_iteration = 100):
        for iteration in range(max_iteration):
            possible_moves: List[PossibleMove] = self.get_neighbours(self.solution, self.solution_score)
            
            possible_moves.sort()
            
            for possible_move in possible_moves:
                if possible_move.move not in self.restricted_moves:
                    self.restricted_moves.append(possible_move.move)
                    self.solution = self.swap_points(self.solution, possible_move.move.point_a, possible_move.move.point_b)
                    self.solution_score = possible_move.value
                    
                    if(self.best_score > self.solution_score):
                        self.best_solution = self.solution
                        self.best_score = self.solution_score
                    
                    if(len(self.restricted_moves) > self.tabu_tenure):
                        self.restricted_moves.pop(0)         
                    
                    break       
        
        return self.best_solution
    
init_solution = [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0), Point(5, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(3, 1), Point(4, 1), Point(5, 1), Point(0, 0)]
tabu_search = PlotioTabuSearch(initial_solution = init_solution, is_first_and_last_element_static=True, tabu_tenure= math.sqrt(len(init_solution)))

#swapped_solution = tabu_search.swap_points(init_solution, Point(10, 10), Point(1, 1))
#sol_value = tabu_search.calculate_value(swapped_solution)
#possible_moves = tabu_search.get_neighbours(init_solution, sol_value)

#print([str(move.move) for move in possible_moves])
solution = tabu_search.optimize(100)
tabu_search.calculate_value(init_solution, True)
tabu_search.calculate_value(solution, True)
