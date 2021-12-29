import enum
from typing import List, Optional

from numpy import ndarray
from numpy.core.fromnumeric import argmin
from numpy.lib.function_base import delete
from numpy.random.mtrand import f
from src.plotter.domain.command import Command
from src.plotter.domain.command_group import CommandGroup
from src.plotter.domain.opimization_utils import *
from src.plotter.domain.optimization.nearest_objects import GroupOfPoints, get_nearest_object
from src.plotter.domain.plotio_preprocess_command_to_optization import PreprocessCommandsToOptimization
from src.plotter.domain.plotio_tabu_search import PlotioTabuSearch, Point, calculate_value
import math
from itertools import chain

from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.domain.simulated_annealing import Annealing, Conditions, SimulatedAnnealing


class OptimizationMethod(enum.Enum):
    TabuSearch = 'TabuSearch'
    SimulatedAnnealing = 'SimulatedAnnealing'
    DoNotOptimize = 'DoNotOptimize'

class ProjectStatus(enum.Enum):
    NotStarted = 'NotStarted'
    Ready = 'Ready'
    Running= 'Running'
    Idle = 'Idle'
    Paused= 'Paused'
    Stopped = 'Stopped'
    Completed = 'Completed'

class Project:
    def __init__(self, name: str, commands: List[Command]) -> None:
        self.name = name
        self.status: ProjectStatus = ProjectStatus.NotStarted
        self.all_commands: List[Command] = commands.copy()
        self.commands_to_do: List[Command] = []
        self.is_active = True
        self.image_content = None

    def __init__(self, name: str, is_active: bool, status: ProjectStatus, all_commands: List[Command], commands_to_do: List[Command], image_content: str, image_shape: List[int]) -> None:
        self.name = name
        self.is_active: bool = is_active
        self.status: ProjectStatus = status
        self.all_commands: List[Command] = all_commands.copy()
        self.commands_to_do: List[Command] = commands_to_do.copy()
        self.image_content: str = image_content
        self.image_shape: List[int] = image_shape

    def load_image(self, image_content: str):
        self.image_content = image_content

    def is_completed_project(self):
        return self.status == ProjectStatus.Completed

    def complete_project(self):
        self.is_active = False
        self.status = ProjectStatus.Completed
        
    def stop_project(self):
        self.is_active = False
        self.status = ProjectStatus.Stopped
        
    def start_project(self) -> bool:
        if(len(self.commands_to_do) != 0 and (self.status == ProjectStatus.Ready or self.status == ProjectStatus.Paused)):
            self.status = ProjectStatus.Running
            return True
        return False

    def pause_project(self):
        self.status = ProjectStatus.Paused

    def get_current_command(self) -> Command:
        if self.commands_to_do[0].is_running_command():
            return self.commands_to_do[0]
        return None

    def get_next_command(self) -> Command:
        return self.commands_to_do[0]
    
    def send_current_command(self) -> Command:
        self.commands_to_do[0].send_command()

    def complete_current_command(self) -> None:
        self.commands_to_do[0].complete_command()
        self.commands_to_do.pop(0)
        if len(self.commands_to_do) == 0:
            self.complete_project()
        
    def optimize_command_groups(self, method: OptimizationMethod, command_groups: List[CommandGroup]):        
        initial_solution = [Point(point.position.posX, point.position.posY, point.position.isHit) for point in self.all_commands]
        
        optimized_commands = None
        
        if(method == OptimizationMethod.TabuSearch):
            optimized_commands = self._optimize_with_tabu(initial_solution)
        elif(method == OptimizationMethod.SimulatedAnnealing):
            optimized_commands = self._optimize_with_simulated_annealing(initial_solution)
        else:
            optimized_commands = self.all_commands
        
        self.all_commands = optimized_commands
        self.commands_to_do = optimized_commands
        self.status = ProjectStatus.Ready
        
    def optimize_command_group_path(self, labels: ndarray, unique_labels: List[int], method: OptimizationMethod, command_groups: List[CommandGroup]):        
        optimized_commands = None
        
        if(method == OptimizationMethod.TabuSearch):
            optimized_commands = self._optimize_command_groups(labels, unique_labels, command_groups, OptimizationMethod.TabuSearch)
        elif(method == OptimizationMethod.SimulatedAnnealing):
            optimized_commands = self._optimize_command_groups(labels, unique_labels, command_groups, OptimizationMethod.SimulatedAnnealing)
        else:
            optimized_commands = self.all_commands
        
        optimal = calculate_value_of_commands(optimized_commands)
        normal = calculate_value_of_commands(self.all_commands)
        
        print(f"Optimal: {optimal}, Normal: {normal}")
        
        if(optimal < normal):
            self.all_commands = optimized_commands.copy()
            self.commands_to_do = optimized_commands.copy()
        self.status = ProjectStatus.Ready
        
    def optimize_path(self, method: OptimizationMethod):        
        initial_solution = [Point(point.position.posX, point.position.posY, point.position.isHit) for point in self.all_commands]
        
        optimized_commands = None
        
        if(method == OptimizationMethod.TabuSearch):
            optimized_commands = self._optimize_with_tabu(initial_solution)
        elif(method == OptimizationMethod.SimulatedAnnealing):
            optimized_commands = self._optimize_with_simulated_annealing(initial_solution)
        else:
            optimized_commands = self.all_commands
        
        self.all_commands = optimized_commands
        self.commands_to_do = optimized_commands
        self.status = ProjectStatus.Ready
        
    def _optimize_command_groups(self, labels: ndarray, unique_labels: List[int], command_groups: List[CommandGroup], method: OptimizationMethod) -> List[Point]:
        grouped_solution: List[GroupOfPoints] = []
        current_position: PlotterPosition = PlotterPosition(0, 0, 0)
        active_command_group = command_groups.copy()
        
        while active_command_group != None and len(active_command_group) > 0:
            next_position, command_group_id = get_nearest_object(current_position, active_command_group)    
            proposed_solution = self.get_proposed_solution(labels, labels[next_position.posY, next_position.posX])    
            # #for command_group in proposed_solution:
            # #    print(f"Point({command_group.posX}, {command_group.posY})")
            # #swap_points(proposed_solution, next_position, proposed_solution[0])
            # if len(proposed_solution) > 2 and len(proposed_solution) < 600:
            #     optimizer = PlotioTabuSearch(proposed_solution.copy(), int(math.sqrt(len(proposed_solution))), calculate_value_function=calculate_value, calculate_value_after_move=calculate_value_after_move, maximum_neighbors=min(50, len(proposed_solution)), random_neighbors=True, optimizer_settings=OptimizerSettings(True, False))
            #     #optimizer = SimulatedAnnealing(proposed_solution.copy(), Conditions(100, 0.1, 0.2, 0.97, 100, Annealing.linear), calculate_value_function=calculate_value, calculate_value_after_move=calculate_value_after_move, maximum_neighbors=400, random_neighbors=True, optimizer_settings=OptimizerSettings(True, False))
            #     optimizer.optimize(min(len(proposed_solution) * 5, 50*1000), None)
            #     optimized = optimizer.best_solution
            #     solution = solution + optimized
            #     print(f"Normal: {calculate_value(proposed_solution)}, Optimized: {calculate_value(optimized)}")
            # else:
            
            
            avgPosX = sum([com.posX for com in proposed_solution]) / len(proposed_solution)
            avgPosY = sum([com.posY for com in proposed_solution]) / len(proposed_solution)
            grouped_solution.append(GroupOfPoints(avgPosX, avgPosY, proposed_solution))
            del active_command_group[command_group_id]
            
            
        
        optimizer = PlotioTabuSearch(grouped_solution, int(math.sqrt(len(grouped_solution))), calculate_value_function=calculate_value, calculate_value_after_move=calculate_value_after_move, maximum_neighbors=min(50, len(proposed_solution)), random_neighbors=True, optimizer_settings=OptimizerSettings(True, False))
        optimizer.optimize(min(len(grouped_solution) * 5, 50*1000), None)
        optimized = optimizer.best_solution
        solution: List[PointWithCommands] = []
        print(f"Normal: {calculate_value(grouped_solution)}, Optimized: {calculate_value(optimized)}")
        for sol in optimized:
            solution = solution + sol.commands
        
        optimized_commands: List[Command] = []
        for command_group in solution:
            optimized_commands = optimized_commands + [Command(PlotterPosition(command.position.posX, command.position.posY, command.position.isHit)) for command in command_group.commands]
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
                avgPosX = sum([com.position.posX for com in commands]) / len(commands)
                avgPosY = sum([com.position.posY for com in commands]) / len(commands)
                proposed_solution_xy.append(PointWithCommands(int(avgPosX), int(avgPosY), commands))
                commands = []
                
        if len(commands) > 0:
            avgPosX = sum([com.position.posX for com in commands]) / len(commands)
            avgPosY = sum([com.position.posY for com in commands]) / len(commands)
            proposed_solution_xy.append(PointWithCommands(int(avgPosX), int(avgPosY), commands))
            commands = []
        
    def _optimize_with_tabu(self, initial_solution: List[Point]):
        preprocessed_commands = PreprocessCommandsToOptimization(initial_solution, 40, 40, self.image_shape[1], self.image_shape[0])
        extracted_groups = preprocessed_commands.extract_groups()
        
        #tabu_optimizer = PlotioTabuSearch(extracted_groups.copy(), 30, maximum_neighbors=200, random_neighbors=True, is_first_and_last_element_static=True)
        #tabu_optimized_groups = tabu_optimizer.optimize(5000, None)
        optimizer = SimulatedAnnealing(extracted_groups.copy(), Conditions(1000, 2, 0.1, 0.97, int(math.sqrt(len(extracted_groups))), Annealing.linear))
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


