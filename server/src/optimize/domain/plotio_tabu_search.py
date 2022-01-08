from typing import Any, Generic, List, TypeVar
import math 
import random
import numpy as np

from src.optimize.domain.opimization_utils import *
T = TypeVar('T')



class PlotioTabuSearch(Generic[T]):
    def __init__(self, initial_solution: List[T], tabu_tenure: int, optimizer_settings: OptimizerSettings, calculate_value_function: Any =calculate_value, calculate_value_after_move: Any =calculate_value_after_move, maximum_neighbors: int = None, random_neighbors: bool = False) -> None:
        self.calculate_value_function: Any = calculate_value_function
        self.calculate_value_after_move: Any = calculate_value_after_move
        self.solution: List[Point] = initial_solution.copy()
        self.solution_score: int = self.calculate_value_function(initial_solution)
        self.best_solution: List[Point] = initial_solution.copy()
        self.best_score: int = self.calculate_value_function(initial_solution)
        self.tabu_tenure: int = tabu_tenure
        self.restricted_moves: List[Move] = []       
        self.optimizer_settings: OptimizerSettings = optimizer_settings
        self.maximum_neighbors: int = maximum_neighbors
        self.random_neighbors: bool = random_neighbors
        self.moves_to_skip = 0

    def is_in_neighbour(self, index_of_point_a: int, index_of_point_b: int):
        return abs(index_of_point_a - index_of_point_b) == 1
    
    def get_neighbours(self, solution: List[Point], solution_value: int) -> List[PossibleMove]:
        possible_moves: List[Move] = []
        
        starting_index = 0
        ending_index = len(solution) 
        
        if self.optimizer_settings.is_first_element_static:
            starting_index = 1
        if self.optimizer_settings.is_last_element_static:
            ending_index = len(solution) - 1
        
        if(self.maximum_neighbors == None):    
            for i in range(starting_index, ending_index):
                for j in range(i + 1, ending_index):
                    move = Move(solution[i], solution[j], i, j)
                    new_value = self.calculate_value_after_move(solution, solution_value, move)
                    possible_moves.append(PossibleMove(move, new_value))
        elif self.random_neighbors:
            for num_of_neighbors in range(self.maximum_neighbors):
                point_a, point_b = np.random.randint(starting_index, ending_index, size=2)
                move = Move(solution[point_a], solution[point_b], point_a, point_b)
                swap_indexes(solution, point_a, point_b)
                new_value = self.calculate_value_function(solution)
                swap_indexes(solution, point_a, point_b)
                new_move = PossibleMove(move, new_value)
                
                # if(new_move in possible_moves):
                #     num_of_neighbors = num_of_neighbors - 1
                #     continue
                possible_moves.append(new_move)
        else:
            num_of_neighbors = 0
            skipped_moves = 0
            for i in range(starting_index, ending_index):
                for j in range(i + 1, ending_index):
                    if(self.moves_to_skip > skipped_moves):
                        skipped_moves = skipped_moves + 1
                        continue
                    
                    move = Move(solution[i], solution[j], i, j)
                    new_value = self.calculate_value_after_move(solution, solution_value, move)
                    possible_moves.append(PossibleMove(move, new_value))
                    if(num_of_neighbors > self.maximum_neighbors):
                        self.moves_to_skip = self.moves_to_skip + num_of_neighbors
                        return possible_moves
                    num_of_neighbors = num_of_neighbors + 1
                    
            self.moves_to_skip = 0
            
                
        
        return possible_moves
        
        
    def optimize(self, max_iteration: int = 100, max_iter_without_optimization: int = 5):
        iter_without_optimization = 0
        for iteration in range(max_iteration):
            possible_moves: List[PossibleMove] = self.get_neighbours(self.solution, self.solution_score)
            
            possible_moves.sort()
            
            for possible_move in possible_moves:
                if possible_move.move not in self.restricted_moves:
                    self.restricted_moves.append(possible_move.move)
                    self.solution = swap_points(self.solution, possible_move.move.point_a, possible_move.move.point_b)
                    self.solution_score = possible_move.value
                    
                    if(self.best_score > self.solution_score):
                        self.best_solution = self.solution.copy()
                        self.best_score = self.solution_score
                        iter_without_optimization = 0
                        #print(self.calculate_value_function(self.best_solution))
                        #print(f"ZNALEZIONO LEPSZE: {self.best_score}")
                    else:
                        iter_without_optimization = iter_without_optimization + 1
                        if(max_iter_without_optimization != None and iter_without_optimization > max_iter_without_optimization):
                            return self.best_solution
                    
                    if(len(self.restricted_moves) > self.tabu_tenure):
                        self.restricted_moves.pop(0)         
                    
                    break       
        
        return self.best_solution