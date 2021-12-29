from typing import Any, ForwardRef, List
import math 
import random
import numpy as np
from src.plotter.domain.opimization_utils import *

from src.plotter.domain.plotio_tabu_search import Move, Point, PossibleMove
import enum

class Annealing(enum.Enum):
    linear = 1
    geometric = 2
    logarithmic = 3
    
class Conditions:
    def __init__(self,T0: float, T_end: float, linear_step: float, a: float, L: int, annealing: Annealing):
        self.T0: float = T0
        self.T_end: float = T_end
        self.linear_step: float = linear_step
        self.a: float = a
        self.L: int = L
        self.annealing: Annealing = annealing
    
    def __str__(self):
        return "{0}, {1}".format(self.T0, self.annealing)
    
def linear_annealing(T: float, x: float):
        return T-x

def geometric_annealing(T: float, a: float):
    return a*T

def logarithmic_annealing(T: float, epoch: float):
    return T/math.log(epoch+1)


class SimulatedAnnealing:
    def __init__(self, initial_solution: List[Point], conditions: Conditions, optimizer_settings: OptimizerSettings, calculate_value_function: Any =calculate_value, calculate_value_after_move: Any =calculate_value_after_move, maximum_neighbors: int = None, random_neighbors: bool = False) -> None:
        self.solution: List[Point] = initial_solution.copy()
        self.solution_score: int = calculate_value_function(self.solution)
        self.best_solution: List[Point] = initial_solution.copy()
        self.best_solution_score: int = self.solution_score
        self.solution_length = len(self.solution)

        self.optimizer_settings: OptimizerSettings = optimizer_settings
        self.calculate_value_function: Any = calculate_value_function
        self.calculate_value_after_move: Any = calculate_value_after_move

        self.conditions: Conditions = conditions
        self.T = conditions.T0
        self.epoch = 1
        
    def optimize(self):
        newPermutationIter = 0
        first_elem_index, last_elem_index = 0, self.solution_length
        if(self.optimizer_settings.is_first_element_static):
            first_elem_index = 1
        if(self.optimizer_settings.is_last_element_static):
            last_elem_index = self.solution_length - 1
            
        while(self.T > self.conditions.T_end):
            for k in range(1, self.conditions.L): 
                i, j = np.random.randint(first_elem_index, last_elem_index, size=2)
                    
                curr_score = self.solution_score
                self.solution = swap_indexes(self.solution, i, j)
                self.solution_score = self.calculate_value_function(self.solution)
                
                if self.best_solution_score > self.solution_score:
                    self.best_solution_score = self.solution_score
                    self.best_solution = self.solution.copy()
                else:
                    x = np.random.uniform()
                    diff_of_solutions = self.solution_score - curr_score
                    if diff_of_solutions < 0 or x < np.exp((-diff_of_solutions) / self.T):
                        newPermutationIter = newPermutationIter + 1
                    else:
                        self.solution = swap_indexes(self.solution, i, j)
                        self.solution_score = self.calculate_value_function(self.solution)
            
            if(self.conditions.annealing == Annealing.linear):
                self.T = linear_annealing(self.T, self.conditions.linear_step)
            elif(self.conditions.annealing == Annealing.geometric):
                self.T = geometric_annealing(self.T, self.conditions.a)
            else:
                self.T = logarithmic_annealing(self.T, self.epoch)
                
            self.epoch = self.epoch + 1
                
