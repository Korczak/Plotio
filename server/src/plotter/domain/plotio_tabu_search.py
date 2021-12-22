from typing import ForwardRef, List
import math 
import random
import numpy as np

from src.plotter.domain.opimization_utils import *

class PlotioTabuSearch:
    def __init__(self, initial_solution: List[Point], tabu_tenure: int, maximum_neighbors: int = None, random_neighbors: bool = False, is_first_and_last_element_static: bool = True) -> None:
        self.solution: List[Point] = initial_solution
        self.solution_score: int = calculate_value(initial_solution)
        self.best_solution: List[Point] = initial_solution
        self.best_score: int = calculate_value(initial_solution)
        self.tabu_tenure: int = tabu_tenure
        self.restricted_moves: List[Move] = []       
        self.is_first_and_last_element_static = is_first_and_last_element_static
        self.maximum_neighbors: int = maximum_neighbors
        self.random_neighbors: bool = random_neighbors
        self.moves_to_skip = 0

    def is_in_neighbour(self, index_of_point_a: int, index_of_point_b: int):
        return abs(index_of_point_a - index_of_point_b) == 1
    
    def get_neighbours(self, solution: List[Point], solution_value: int) -> List[PossibleMove]:
        possible_moves: List[Move] = []
        
        starting_index = 0
        ending_index = len(solution) 
        
        if self.is_first_and_last_element_static:
            starting_index = 1
            ending_index = len(solution) - 1
        
        if(self.maximum_neighbors == None):    
            for i in range(starting_index, ending_index):
                for j in range(i + 1, ending_index):
                    move = Move(solution[i], solution[j], i, j)
                    new_value = calculate_value_after_move(solution, solution_value, move)
                    possible_moves.append(PossibleMove(move, new_value))
        elif self.random_neighbors:
            for num_of_neighbors in range(self.maximum_neighbors):
                point_a, point_b = np.random.randint(starting_index, ending_index, size=2)
                move = Move(solution[point_a], solution[point_b], point_a, point_b)
                
                new_value = calculate_value_after_move(solution, solution_value, move)
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
                    new_value = calculate_value_after_move(solution, solution_value, move)
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
                        self.best_solution = self.solution
                        self.best_score = self.solution_score
                        iter_without_optimization = 0
                    else:
                        iter_without_optimization = iter_without_optimization + 1
                        if(max_iter_without_optimization != None and iter_without_optimization > max_iter_without_optimization):
                            return self.best_solution
                    
                    if(len(self.restricted_moves) > self.tabu_tenure):
                        self.restricted_moves.pop(0)         
                    
                    break       
        
        return self.best_solution