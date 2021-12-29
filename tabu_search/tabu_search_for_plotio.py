from typing import List
import math

import numpy as np

from optim_utils import * 

class PlotioTabuSearch:
    def __init__(self, initial_solution: List[Point], tabu_tenure: int, optimizer_settings: OptimizerSettings, maximum_neighbors: int = None, random_neighbors: bool = False) -> None:
        self.solution: List[Point] = initial_solution.copy()
        self.solution_score: int = calculate_value(initial_solution)
        self.best_solution: List[Point] = initial_solution.copy()
        self.best_score: int = calculate_value(initial_solution)
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
                        self.best_solution = self.solution.copy()
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
    
#init_solution = [Point(21, 72), Point(21, 71), Point(21, 70), Point(21, 69), Point(21, 68), Point(21, 67), Point(21, 66), Point(21, 65), Point(21, 64), Point(21, 63), Point(21, 62), Point(21, 61), Point(21, 60), Point(21, 59), Point(21, 58), Point(21, 57), Point(21, 56), Point(21, 55), Point(21, 54), Point(21, 53), Point(21, 52), Point(21, 51), Point(22, 51), Point(22, 52), Point(22, 53), Point(22, 54), Point(22, 55), Point(22, 56), Point(22, 57), Point(22, 58), Point(22, 59), Point(22, 60), Point(22, 61), Point(22, 62), Point(22, 63), Point(22, 64), Point(22, 65), Point(22, 66), Point(22, 67), Point(22, 68), Point(22, 69), Point(22, 70), Point(22, 71), Point(22, 72), Point(23, 72), Point(23, 71), Point(23, 52), Point(23, 51), Point(24, 51), Point(24, 52), Point(24, 71), Point(24, 72), Point(25, 72), Point(25, 71), Point(25, 52), Point(25, 51), Point(26, 51), Point(26, 52), Point(26, 71), Point(26, 72), Point(27, 72), Point(27, 71), Point(27, 52), Point(27, 51), Point(28, 51), Point(28, 52), Point(28, 71), Point(28, 72), Point(29, 72), Point(29, 71), Point(29, 52), Point(29, 51), Point(30, 51), Point(30, 52), Point(30, 71), Point(30, 72), Point(31, 72), Point(31, 71), Point(31, 52), Point(31, 51), Point(32, 51), Point(32, 52), Point(32, 71), Point(32, 72), Point(33, 72), Point(33, 71), Point(33, 52), Point(33, 51), Point(34, 51), Point(34, 52), Point(34, 71), Point(34, 72), Point(35, 72), Point(35, 71), Point(35, 52), Point(35, 51), Point(36, 51), Point(36, 52), Point(36, 71), Point(36, 72), Point(37, 72), Point(37, 71), Point(37, 52), Point(37, 51), Point(38, 51), Point(38, 52), Point(38, 71), Point(38, 72), Point(39, 72), Point(39, 71), Point(39, 52), Point(39, 51), Point(40, 51), Point(40, 52), Point(40, 71), Point(40, 72), Point(41, 72), Point(41, 71), Point(41, 70), Point(41, 69), Point(41, 68), Point(41, 67), Point(41, 66), Point(41, 65), Point(41, 64), Point(41, 63), Point(41, 62), Point(41, 61), Point(41, 60), Point(41, 59), Point(41, 58), Point(41, 57), Point(41, 56), Point(41, 55), Point(41, 54), Point(41, 53), Point(41, 52), Point(41, 51), Point(42, 51), Point(42, 52), Point(42, 53), Point(42, 54), Point(42, 55), Point(42, 56), Point(42, 57), Point(42, 58), Point(42, 59), Point(42, 60), Point(42, 61), Point(42, 62), Point(42, 63), Point(42, 64), Point(42, 65), Point(42, 66), Point(42, 67), Point(42, 68), Point(42, 69), Point(42, 70), Point(42, 71), Point(42, 72)]
#init_solution = [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0), Point(5, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(3, 1), Point(4, 1), Point(5, 1), Point(0, 0)]
#init_solution = [Point(31, 51), Point(31, 52), Point(21, 53), Point(41, 53), Point(21, 54), Point(41, 54), Point(21, 55), Point(41, 55), Point(21, 56), Point(41, 56), Point(21, 57), Point(41, 57), Point(21, 58), Point(41, 58), Point(21, 59), Point(41, 59), Point(21, 60), Point(41, 60), Point(21, 61), Point(41, 61), Point(21, 62), Point(41, 62), Point(21, 63), Point(41, 63), Point(21, 64), Point(41, 64), Point(21, 65), Point(41, 65), Point(21, 66), Point(41, 66), Point(21, 67), Point(41, 67), Point(21, 68), Point(41, 68), Point(21, 69), Point(41, 69), Point(21, 70), Point(41, 70), Point(31, 71), Point(31, 72)]
init_solution = [Point(55, 61), Point(56, 62), Point(56, 63), Point(56, 64), Point(56, 65), Point(56, 66), Point(56, 67), Point(57, 68), Point(56, 69), Point(57, 70), Point(57, 71), Point(57, 72), Point(57, 73), Point(57, 74), Point(57, 75), Point(58, 76), Point(58, 77), Point(58, 78), Point(59, 79), Point(299, 79), Point(59, 80), Point(299, 80), Point(59, 81), Point(295, 81), Point(298, 81), Point(301, 81), Point(60, 82), Point(298, 82), Point(60, 83), Point(294, 83), Point(302, 83), Point(60, 84), Point(295, 84), Point(302, 84), Point(61, 85), Point(299, 85), Point(61, 86), Point(301, 86), Point(62, 87), Point(301, 87), Point(62, 88), Point(301, 88), Point(62, 89), Point(301, 89), Point(62, 90), Point(299, 90), Point(302, 90), Point(62, 91), Point(298, 91), Point(302, 91), Point(62, 92), Point(298, 92), Point(302, 92), Point(63, 93), Point(297, 93), Point(302, 93), Point(63, 94), Point(297, 94), Point(302, 94), Point(63, 95), Point(297, 95), Point(301, 95), Point(64, 96), Point(296, 96), Point(301, 96), Point(64, 97), Point(296, 97), Point(301, 97), Point(64, 98), Point(296, 98), Point(301, 98), Point(64, 99), Point(295, 99), Point(300, 99), Point(64, 100), Point(295, 100), Point(300, 100), Point(64, 101), Point(294, 101), Point(300, 101), Point(64, 102), Point(294, 102), Point(298, 102), Point(301, 102), Point(64, 103), Point(293, 103), Point(298, 103), Point(301, 103), Point(65, 104), Point(293, 104), Point(298, 104), Point(301, 104), Point(65, 105), Point(293, 105), Point(299, 105), Point(65, 106), Point(292, 106), Point(298, 106), Point(66, 107), Point(292, 107), Point(298, 107), Point(66, 108), Point(292, 108), Point(298, 108), Point(67, 109), Point(291, 109), Point(297, 109), Point(67, 110), Point(290, 110), Point(297, 110), Point(67, 111), Point(290, 111), Point(296, 111), Point(68, 112), Point(290, 112), Point(295, 112), Point(68, 113), Point(289, 113), Point(295, 113), Point(69, 114), Point(289, 114), Point(295, 114), Point(70, 115), Point(288, 115), Point(294, 115), Point(70, 116), Point(288, 116), Point(293, 116), Point(295, 116), Point(70, 117), Point(288, 117), Point(294, 117), Point(71, 118), Point(287, 118), Point(291, 118), Point(295, 118), Point(71, 119), Point(287, 119), Point(291, 119), Point(295, 119), Point(71, 120), Point(286, 120), Point(290, 120), Point(295, 120), Point(72, 121), Point(286, 121), Point(290, 121), Point(294, 121), Point(73, 122), Point(286, 122), Point(290, 122), Point(293, 122), Point(74, 123), Point(285, 123), Point(289, 123), Point(293, 123), Point(74, 124), Point(285, 124), Point(288, 124), Point(293, 124), Point(74, 125), Point(286, 125), Point(293, 125), Point(75, 126), Point(285, 126), Point(293, 126), Point(76, 127), Point(285, 127), Point(293, 127), Point(77, 128), Point(283, 128), Point(286, 128), Point(77, 129), Point(284, 129), Point(78, 130), Point(284, 130), Point(79, 131), Point(283, 131), Point(80, 132), Point(282, 132), Point(80, 133), Point(281, 133), Point(81, 134), Point(280, 134), Point(82, 135), Point(279, 135), Point(83, 136), Point(278, 136), Point(84, 137), Point(278, 137), Point(84, 138), Point(277, 138), Point(85, 139), Point(276, 139), Point(86, 140), Point(275, 140), Point(88, 141), Point(275, 141), Point(89, 142), Point(274, 142), Point(90, 143), Point(273, 143), Point(91, 144), Point(273, 144), Point(91, 145), Point(272, 145), Point(92, 146), Point(271, 146), Point(93, 147), Point(271, 147), Point(95, 148), Point(270, 148), Point(96, 149), Point(270, 149), Point(98, 150), Point(269, 150), Point(99, 151), Point(268, 151), Point(100, 152), Point(267, 152), Point(102, 153), Point(266, 153), Point(101, 154), Point(105, 154), Point(263, 154), Point(267, 154), Point(101, 155), Point(106, 155), Point(264, 155), Point(102, 156), Point(107, 156), Point(264, 156), Point(103, 157), Point(109, 157), Point(261, 157), Point(105, 158), Point(111, 158), Point(260, 158), Point(106, 159), Point(112, 159), Point(258, 159), Point(107, 160), Point(113, 160), Point(256, 160), Point(108, 161), Point(115, 161), Point(255, 161), Point(110, 162), Point(116, 162), Point(253, 162), Point(111, 163), Point(117, 163), Point(251, 163), Point(112, 164), Point(119, 164), Point(249, 164), Point(113, 165), Point(120, 165), Point(247, 165), Point(114, 166), Point(121, 166), Point(246, 166), Point(116, 167), Point(122, 167), Point(245, 167), Point(116, 168), Point(123, 168), Point(242, 168), Point(118, 169), Point(124, 169), Point(240, 169), Point(119, 170), Point(125, 170), Point(238, 170), Point(121, 171), Point(127, 171), Point(236, 171), Point(122, 172), Point(128, 172), Point(234, 172), Point(127, 173), Point(232, 173), Point(129, 174), Point(231, 174), Point(131, 175), Point(230, 175), Point(132, 176), Point(229, 176), Point(134, 177), Point(227, 177), Point(136, 178), Point(226, 178), Point(139, 179), Point(225, 179), Point(140, 180), Point(224, 180), Point(143, 181), Point(223, 181), Point(145, 182), Point(222, 182), Point(147, 183), Point(221, 183), Point(150, 184), Point(219, 184), Point(152, 185), Point(218, 185), Point(155, 186), Point(215, 186), Point(219, 186), Point(158, 187), Point(212, 187), Point(218, 187), Point(160, 188), Point(211, 188), Point(217, 188), Point(165, 189), Point(208, 189), Point(216, 189), Point(185, 190), Point(215, 190), Point(191, 191), Point(191, 192)]
#init_solution = [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0), Point(5, 0), Point(0, 1), Point(1, 1), Point(2, 1), Point(3, 1), Point(4, 1), Point(5, 1), Point(0, 0)]

print(len(init_solution))
#tabu_search = PlotioTabuSearch(initial_solution = init_solution, is_first_and_last_element_static=True, tabu_tenure= math.sqrt(len(init_solution)))
tabu_search = PlotioTabuSearch(init_solution.copy(), int(math.sqrt(len(init_solution))), maximum_neighbors=50, random_neighbors=True, optimizer_settings=OptimizerSettings(True, True))
#swapped_solution = tabu_search.swap_points(init_solution, Point(10, 10), Point(1, 1))
#sol_value = tabu_search.calculate_value(swapped_solution)
#possible_moves = tabu_search.get_neighbours(init_solution, sol_value)

#print([str(move.move) for move in possible_moves])
solution = tabu_search.optimize(len(init_solution) * 20, None)

init_val = calculate_value(init_solution)
optim_val = calculate_value(solution, True)

print(f"Init val: {init_val}, Optim val: {optim_val}")
