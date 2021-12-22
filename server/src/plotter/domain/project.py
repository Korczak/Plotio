import enum
from typing import List, Optional
from src.plotter.domain.command import Command
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
        self.all_commands: List[Command] = commands
        self.commands_to_do: List[Command] = []
        self.is_active = True
        self.image_content = None

    def __init__(self, name: str, is_active: bool, status: ProjectStatus, all_commands: List[Command], commands_to_do: List[Command], image_content: str, image_shape: List[int]) -> None:
        self.name = name
        self.is_active: bool = is_active
        self.status: ProjectStatus = status
        self.all_commands: List[Command] = all_commands
        self.commands_to_do: List[Command] = commands_to_do
        self.image_content: str = image_content
        self.image_shape: List[int] = image_shape

    def load_image(self, image_content: str):
        self.image_content = image_content

    def complete_project(self):
        self.is_active = False
        self.status = ProjectStatus.Completed
        
    def stop_project(self):
        self.is_active = False
        self.status = ProjectStatus.Stopped
        
    def start_project(self) -> bool:
        if(len(self.commands_to_do) != 0 and self.status == ProjectStatus.Ready):
            self.status = ProjectStatus.Running
            return True
        return False

    def pause_project(self):
        self.status = ProjectStatus.Stopped

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
        
    def _optimize_with_simulated_annealing(self, initial_solution: List[Point]):
        optimizer = SimulatedAnnealing(initial_solution.copy(), Conditions(1000, 0.1, 0.1, 0.97, Annealing.linear))
        optimizer.optimize()
        
        sol_value = calculate_value(optimizer.best_solution)
        init_value = calculate_value(initial_solution)
        
        optimized_commands = [Command(PlotterPosition(pos.posX, pos.posY, pos.hit)) for pos in optimizer.best_solution]
        
        return optimized_commands
        
        
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


