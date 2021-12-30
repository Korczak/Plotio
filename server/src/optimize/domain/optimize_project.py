import enum
from typing import List, Optional
from numpy import ndarray, number

from pubsub import pub
from src import plotter
from src.optimize.domain.nearest_objects import *
from src.optimize.domain.opimization_utils import *
from src.optimize.domain.plotio_preprocess_command_to_optization import PreprocessCommandsToOptimization
from src.optimize.domain.plotio_tabu_search import PlotioTabuSearch
from src.optimize.domain.simulated_annealing import Annealing, Conditions, SimulatedAnnealing
from src.plotter.domain.alarm import Alarm, AlarmType
from src.plotter.domain.command import Command
from src.plotter.domain.command_details import CommandDetails
from src.plotter.domain.command_group import CommandGroup

from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.domain.project import OptimizationMethod, Project
from itertools import chain


class OptimizeProject:
    def __init__(self, name: str, all_commands: List[Command], commands_to_do: List[Command], image_content: ndarray, labels: ndarray, unique_labels: List[int], command_groups: List[CommandGroup]) -> None:
        self.name = name
        self.all_commands: List[Command] = all_commands.copy()
        self.commands_to_do: List[Command] = commands_to_do
        self.image_content: ndarray = image_content
        self.labels: ndarray = labels
        self.unique_labels: List[int] = unique_labels
        self.command_groups: List[CommandGroup] = command_groups
    
    def optimize_command_groups(self, method: OptimizationMethod) -> List[Command[PlotterPosition]]:        
        initial_solution = [Point(point.command_detail.posX, point.command_detail.posY, point.command_detail.isHit) for point in self.all_commands]
        
        optimized_commands = None
        
        if(method == OptimizationMethod.TabuSearch):
            optimized_commands = self._optimize_command_groups(self.labels, self.unique_labels, self.command_groups, method)
        elif(method == OptimizationMethod.SimulatedAnnealing):
            optimized_commands = self._optimize_with_simulated_annealing(initial_solution)
        else:
            optimized_commands = self.all_commands
        
        return optimized_commands
    
    def _optimize_command_groups(self, labels: ndarray, unique_labels: List[int], command_groups: List[CommandGroup], method: OptimizationMethod) -> List[Point]:
        grouped_solution: List[GroupOfPoints] = []
        next_position: PlotterPosition = PlotterPosition(0, 0, 0)
        active_command_group = command_groups.copy()
        
        while active_command_group != None and len(active_command_group) > 0:
            next_position, command_group_id = get_nearest_object(next_position, active_command_group)    
            proposed_solution = self.get_proposed_solution(labels, labels[next_position.posY, next_position.posX])
            
            avgPosX = sum([com.posX for com in proposed_solution]) / len(proposed_solution)
            avgPosY = sum([com.posY for com in proposed_solution]) / len(proposed_solution)
            grouped_solution.append(GroupOfPoints(avgPosX, avgPosY, proposed_solution))
            del active_command_group[command_group_id]
            

        optimizer = PlotioTabuSearch(grouped_solution, int(math.sqrt(len(grouped_solution))), calculate_value_function=calculate_value, calculate_value_after_move=calculate_value_after_move, maximum_neighbors=min(50, len(proposed_solution)), random_neighbors=True, optimizer_settings=OptimizerSettings(True, False))
        optimizer.optimize(max(min(len(grouped_solution) * 20, 50*1000), 5000), None)
        optimized = optimizer.best_solution
        solution: List[PointWithCommands] = []
        print(f"Normal: {calculate_value(grouped_solution)}, Optimized: {calculate_value(optimized)}")
        for sol in optimized:
            solution = solution + sol.commands
        
        optimized_commands: List[Command] = []
        for command_group in solution:
            optimized_commands = optimized_commands + [Command(PlotterPosition(command.command_detail.posX, command.command_detail.posY, command.command_detail.isHit)) for command in command_group.commands]
        return optimized_commands

    def get_proposed_solution(self, label_image: ndarray, label: int) -> List[PointWithCommands]:
        proposed_solution_xy, xy_value = self.get_proposed_solution_xy(label_image, label)
        #proposed_solution_yx, yx_value = self.get_proposed_solution_yx(label_image, label)
                
        #if(xy_value < yx_value):
        #    return proposed_solution_xy
        return proposed_solution_xy

    def get_proposed_solution_yx(self, label_image, label):
        proposed_solution_yx: List[Point] = []
                    
        for y in range(0, label_image.shape[1]):
            if(y % 2 == 0):
                for x in range(0, label_image.shape[0]):
                    if(label_image[x, y] == label):
                        proposed_solution_yx.append(Point(y, x, 1))
            else:
                for x in range(label_image.shape[0] - 1, 0, -1):
                    if(label_image[x, y] == label):
                        proposed_solution_yx.append(Point(y, x, 1))
                        
        yx_value = calculate_value(proposed_solution_yx)
        return proposed_solution_yx,yx_value

    def get_proposed_solution_xy(self, label_image, label):
        proposed_solution_xy: List[PointWithCommands] = []
        
        for x in range(0, label_image.shape[0]):
            #if x % 2 == 0:
            commands: List[Command] = []
            if x % 2 == 0:
                self.get_proposition_for_row(label_image, label, proposed_solution_xy, x, commands, 0, label_image.shape[1], 1)
            else:
                self.get_proposition_for_row(label_image, label, proposed_solution_xy, x, commands,  label_image.shape[1] - 1, 0, -1)
        
        current_position: PlotterPosition = PlotterPosition(0, 0, 0)
        active_command_groups: List[PointWithCommands] = proposed_solution_xy.copy()
        proposed_solution: List[PointWithCommands] = []
        while active_command_groups != None and len(active_command_groups) > 0:
            next_position, command_group_id = get_nearest_object(current_position, active_command_groups)
            
            current_position = next_position
            proposed_solution.append(active_command_groups[command_group_id])
            del active_command_groups[command_group_id]
                        
        xy_value = calculate_value(proposed_solution)
        return proposed_solution ,xy_value

    def get_proposition_for_row(self, label_image, label, proposed_solution_xy, x, commands, start_index, end_index, step):
        for y in range(start_index, end_index, step):
            if(label_image[x, y] == label):
                commands.append(Command(PlotterPosition(y, x, 1)))
            elif len(commands) > 0:
                avgPosX = sum([com.command_detail.posX for com in commands]) / len(commands)
                avgPosY = sum([com.command_detail.posY for com in commands]) / len(commands)
                proposed_solution_xy.append(PointWithCommands(int(avgPosX), int(avgPosY), commands))
                commands = []
                
        if len(commands) > 0:
            avgPosX = sum([com.command_detail.posX for com in commands]) / len(commands)
            avgPosY = sum([com.command_detail.posY for com in commands]) / len(commands)
            proposed_solution_xy.append(PointWithCommands(int(avgPosX), int(avgPosY), commands))
            commands = []
        
    def _optimize_with_tabu(self, initial_solution: List[Point]):
        preprocessed_commands = PreprocessCommandsToOptimization(initial_solution, 40, 40, self.image_content.shape[1], self.image_content.shape[0])
        extracted_groups = preprocessed_commands.extract_groups()
        
        #tabu_optimizer = PlotioTabuSearch(extracted_groups.copy(), 30, maximum_neighbors=200, random_neighbors=True, is_first_and_last_element_static=True)
        #tabu_optimized_groups = tabu_optimizer.optimize(5000, None)
        optimizer = SimulatedAnnealing(extracted_groups.copy(), Conditions(1000, 2, 0.1, 0.97, int(math.sqrt(len(extracted_groups))), aling.linear))
        optimizer.optimize()
        
        for group in extracted_groups:
            print(str(group))
        
        groups_solution: List[List[Point]] = []
        for group in optimizer.best_solution:
            groups_solution.append(preprocessed_commands.get_commands_for_group(group.posX, group.posY))
            
        for group_index in range(0, len(groups_solution)-1):
            maximum_neighbors = len(groups_solution[group_index])
            if(maximum_neighbors > 1000):
                maximum_neighbors = 1000
            tabu_tenure = 5
            max_iter = len(groups_solution[group_index]) * 5
            max_iter_without_optimization = len(groups_solution[group_index])
            
            if(group_index == 0):
                solution_to_optimize = groups_solution[group_index].copy()
                solution_to_optimize.append(groups_solution[group_index+1][0]) 
                optimizer = PlotioTabuSearch(solution_to_optimize, tabu_tenure, maximum_neighbors, True, True)
                groups_solution[group_index] = optimizer.optimize(max_iter, max_iter_without_optimization)[1:-1]
            elif(group_index == len(groups_solution) - 1):
                solution_to_optimize = groups_solution[group_index].copy()
                solution_to_optimize.insert(0, groups_solution[group_index-1][-1])
                solution_to_optimize.append(Point(0, 0)) 
                optimizer = PlotioTabuSearch(solution_to_optimize, tabu_tenure, maximum_neighbors, True, True)
                groups_solution[group_index] = optimizer.optimize(max_iter, max_iter_without_optimization)[1:-1]
            else:
                solution_to_optimize = groups_solution[group_index].copy()
                solution_to_optimize.insert(0, groups_solution[group_index-1][-1])
                solution_to_optimize.append(groups_solution[group_index+1][0]) 
                optimizer = PlotioTabuSearch(solution_to_optimize, tabu_tenure, maximum_neighbors, True, True)
                groups_solution[group_index] = optimizer.optimize(max_iter, max_iter_without_optimization)[1:-1]
        
        solution = list(chain(*groups_solution))
        
        sol_value = calculate_value(solution)
        init_value = calculate_value(initial_solution)
        
        optimized_commands = [Command(PlotterPosition(pos.posX, pos.posY, pos.hit)) for pos in solution]
        
        return optimized_commands
