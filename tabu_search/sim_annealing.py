from typing import ForwardRef, List
import math 
import random
import numpy as np
import enum
from optim_utils import *

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
    def __init__(self, initial_solution: List[Point], conditions: Conditions, is_first_and_last_element_static: bool = True) -> None:
        self.solution: List[Point] = initial_solution.copy()
        self.solution_score: int = calculate_value(self.solution)
        self.best_solution: List[Point] = initial_solution.copy()
        self.best_solution_score: int = self.solution_score
        self.solution_length = len(self.solution)
        self.is_first_and_last_element_static: bool = is_first_and_last_element_static
        
        self.conditions: Conditions = conditions
        self.T = conditions.T0
        self.epoch = 1
        
    def optimize(self):
        newPermutationIter = 0
        while(self.T > self.conditions.T_end):
            for k in range(1, self.conditions.L):
                if(self.is_first_and_last_element_static):                
                    i, j = np.random.randint(1, self.solution_length - 1, size=2)
                else:
                    i, j = np.random.randint(0, self.solution_length, size=2)
                    
                curr_score = self.solution_score
                self.solution = swap_indexes(self.solution, i, j)
                self.solution_score = calculate_value(self.solution)
                
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
                        self.solution_score = calculate_value(self.solution)
            
            if(self.conditions.annealing == Annealing.linear):
                self.T = linear_annealing(self.T, self.conditions.linear_step)
            elif(self.conditions.annealing == Annealing.geometric):
                self.T = geometric_annealing(self.T, self.conditions.a)
            else:
                self.T = logarithmic_annealing(self.T, self.epoch)
                
            self.epoch = self.epoch + 1
                

#init_solution = [Point(21, 72), Point(21, 71), Point(21, 70), Point(21, 69), Point(21, 68), Point(21, 67), Point(21, 66), Point(21, 65), Point(21, 64), Point(21, 63), Point(21, 62), Point(21, 61), Point(21, 60), Point(21, 59), Point(21, 58), Point(21, 57), Point(21, 56), Point(21, 55), Point(21, 54), Point(21, 53), Point(21, 52), Point(21, 51), Point(22, 51), Point(22, 52), Point(22, 53), Point(22, 54), Point(22, 55), Point(22, 56), Point(22, 57), Point(22, 58), Point(22, 59), Point(22, 60), Point(22, 61), Point(22, 62), Point(22, 63), Point(22, 64), Point(22, 65), Point(22, 66), Point(22, 67), Point(22, 68), Point(22, 69), Point(22, 70), Point(22, 71), Point(22, 72), Point(23, 72), Point(23, 71), Point(23, 52), Point(23, 51), Point(24, 51), Point(24, 52), Point(24, 71), Point(24, 72), Point(25, 72), Point(25, 71), Point(25, 52), Point(25, 51), Point(26, 51), Point(26, 52), Point(26, 71), Point(26, 72), Point(27, 72), Point(27, 71), Point(27, 52), Point(27, 51), Point(28, 51), Point(28, 52), Point(28, 71), Point(28, 72), Point(29, 72), Point(29, 71), Point(29, 52), Point(29, 51), Point(30, 51), Point(30, 52), Point(30, 71), Point(30, 72), Point(31, 72), Point(31, 71), Point(31, 52), Point(31, 51), Point(32, 51), Point(32, 52), Point(32, 71), Point(32, 72), Point(33, 72), Point(33, 71), Point(33, 52), Point(33, 51), Point(34, 51), Point(34, 52), Point(34, 71), Point(34, 72), Point(35, 72), Point(35, 71), Point(35, 52), Point(35, 51), Point(36, 51), Point(36, 52), Point(36, 71), Point(36, 72), Point(37, 72), Point(37, 71), Point(37, 52), Point(37, 51), Point(38, 51), Point(38, 52), Point(38, 71), Point(38, 72), Point(39, 72), Point(39, 71), Point(39, 52), Point(39, 51), Point(40, 51), Point(40, 52), Point(40, 71), Point(40, 72), Point(41, 72), Point(41, 71), Point(41, 70), Point(41, 69), Point(41, 68), Point(41, 67), Point(41, 66), Point(41, 65), Point(41, 64), Point(41, 63), Point(41, 62), Point(41, 61), Point(41, 60), Point(41, 59), Point(41, 58), Point(41, 57), Point(41, 56), Point(41, 55), Point(41, 54), Point(41, 53), Point(41, 52), Point(41, 51), Point(42, 51), Point(42, 52), Point(42, 53), Point(42, 54), Point(42, 55), Point(42, 56), Point(42, 57), Point(42, 58), Point(42, 59), Point(42, 60), Point(42, 61), Point(42, 62), Point(42, 63), Point(42, 64), Point(42, 65), Point(42, 66), Point(42, 67), Point(42, 68), Point(42, 69), Point(42, 70), Point(42, 71), Point(42, 72)]
init_solution = [Point(31, 51), Point(31, 52), Point(21, 53), Point(41, 53), Point(21, 54), Point(41, 54), Point(21, 55), Point(41, 55), Point(21, 56), Point(41, 56), Point(21, 57), Point(41, 57), Point(21, 58), Point(41, 58), Point(21, 59), Point(41, 59), Point(21, 60), Point(41, 60), Point(21, 61), Point(41, 61), Point(21, 62), Point(41, 62), Point(21, 63), Point(41, 63), Point(21, 64), Point(41, 64), Point(21, 65), Point(41, 65), Point(21, 66), Point(41, 66), Point(21, 67), Point(41, 67), Point(21, 68), Point(41, 68), Point(21, 69), Point(41, 69), Point(21, 70), Point(41, 70), Point(31, 71), Point(31, 72)]

#init_solution = [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0), Point(5, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(3, 1), Point(4, 1), Point(5, 1), Point(0, 0)]
sim_anealing = SimulatedAnnealing(initial_solution = init_solution, conditions=Conditions(100, 0.1, 0.1, 0.97, 300, Annealing.linear), is_first_and_last_element_static=True)

sim_anealing.optimize()
init_val = calculate_value(init_solution)
optim_val = calculate_value(sim_anealing.best_solution)

print(f"Init val: {init_val}, Optim val: {optim_val}")