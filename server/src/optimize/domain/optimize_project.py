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
    def __init__(self, name: str, all_commands: List[Command], commands_to_do: List[Command], image_content: ndarray) -> None:
        self.name = name
        self.all_commands: List[Command] = all_commands.copy()
        self.commands_to_do: List[Command] = commands_to_do
        self.image_content: ndarray = image_content
        self.labels: ndarray = None
        self.unique_labels: List[int] = None
        self.command_groups: List[CommandGroup] = None
    
    def optimize_command_groups(self, method: OptimizationMethod) -> List[Command[PlotterPosition]]:   
        object_color = 0
        equivalency_list, labels, num_of_commands = self._extract_sub_images(self.image_content, object_color)
        
        commandGroups: List[CommandGroup] = []
        
        unique_labels = list(set(equivalency_list.values()))
    
        if num_of_commands > 50000:
            return self.all_commands
        else:
            for label in unique_labels:
                commandGroups.append(CommandGroup([]))
            for x in range(0, self.image_content.shape[0]):
                for y in range(0, self.image_content.shape[1]):
                    if(labels[x, y] != 0):
                        commandGroups[unique_labels.index(labels[x, y])].commands.append(Command(PlotterPosition(y, x, 1)))
                        
            #commandGroups.append(CommandGroup([Command(PlotterPosition(0, 0, 0))]))     
            all_commands: List[Command] = []
            for commandGroup in commandGroups:
                all_commands = all_commands + commandGroup.commands        

        self.command_groups = commandGroups
        self.labels = labels
         
        initial_solution = [Point(point.command_detail.posX, point.command_detail.posY, point.command_detail.hitTimes) for point in self.all_commands]
        
        optimized_commands = None
        
        if(method == OptimizationMethod.DoNotOptimize):
            optimized_commands = self.all_commands
        else:
            optimized_commands = self._optimize_command_groups(self.labels, self.unique_labels, self.command_groups, method)
            
        current_val = calculate_value_of_commands(self.all_commands)
        optimized_val = calculate_value_of_commands(optimized_commands)
        
        print(f'Curr: {current_val}, Optimized: {optimized_val}')
        
        return optimized_commands
    
    def _extract_sub_images(self, thresh_img: np.ndarray, object_color: int):
        labels = np.zeros((thresh_img.shape[0], thresh_img.shape[1]))
        num_of_commands = 0
        
        curr_obj = 0
        equivalency_list = {}
        pixel_above, pixel_left = 0, 0
        
        
        for x in range(0, thresh_img.shape[0]):
            for y in range(0, thresh_img.shape[1]):
                if(thresh_img[x, y] == object_color):
                    pixel_above, pixel_left = 0, 0
                    
                    if y > 0:
                        if labels[x][y-1] > 0:
                            pixel_above = equivalency_list[labels[x][y-1]]
                    
                    if x > 0:
                        if labels[x-1][y] > 0:
                            pixel_left = equivalency_list[labels[x-1][y]]
                        
                    if pixel_above != 0 and pixel_left != 0:
                        classification = min(pixel_above, pixel_left)
                        equivalency_list[pixel_left] = classification
                        equivalency_list[pixel_above] = classification
                    elif pixel_above != 0:
                        classification = pixel_above
                    elif pixel_left != 0:
                        classification = pixel_left
                    else:
                        curr_obj += 1 
                        equivalency_list[curr_obj] = curr_obj
                        classification = curr_obj
                      
                    labels[x][y] = int(classification)

        for x in range(0, thresh_img.shape[0]):
            for y in range(0, thresh_img.shape[1]):
                if(thresh_img[x][y] == object_color):
                    labels[x][y] = equivalency_list[int(labels[x][y])]
                    num_of_commands = num_of_commands + 1
        return equivalency_list, labels, num_of_commands

    def _optimize_command_groups(self, labels: ndarray, unique_labels: List[int], command_groups: List[CommandGroup], method: OptimizationMethod) -> List[Point]:
        grouped_solution: List[FragmentWithCommands] = []
        next_position: PlotterPosition = PlotterPosition(0, 0, 0)
        active_command_group = command_groups.copy()
        
        while active_command_group != None and len(active_command_group) > 0:
            next_position, command_group_id = get_nearest_object(next_position, active_command_group, 1)    
            proposed_solution = self.get_proposed_solution(labels, labels[next_position.posY, next_position.posX])
            
            if len(proposed_solution) > 1:
                grouped_solution.append(FragmentWithCommands(proposed_solution[0].posX, proposed_solution[0].posY, proposed_solution[-1].posX, proposed_solution[-1].posY, proposed_solution))
            del active_command_group[command_group_id]
            

        if method == OptimizationMethod.TabuSearch:
            optimizer = PlotioTabuSearch(grouped_solution.copy(), int(math.sqrt(len(grouped_solution))), calculate_value_function=calculate_value_of_fragments, calculate_value_after_move=calculate_value_after_move, maximum_neighbors=min(50, len(proposed_solution)), random_neighbors=True, optimizer_settings=OptimizerSettings(True, False))
            optimizer.optimize(max(min(len(grouped_solution) * 20, 50*1000), 10000), None)
            optimized = optimizer.best_solution
        elif method == OptimizationMethod.SimulatedAnnealing:
            optimizer = SimulatedAnnealing(grouped_solution.copy(), Conditions(100, 0.1, 0.1, 0.97, 100, Annealing.linear),  calculate_value_function=calculate_value_of_fragments, calculate_value_after_move=calculate_value_after_move, optimizer_settings=OptimizerSettings(True, False))
            optimizer.optimize()
            optimized = optimizer.best_solution

        
        solution: List[PointWithCommands] = []
        init_solution: List[PointWithCommands] = []
        for sol in optimized:
            solution = solution + sol.commands
        for sol in grouped_solution:
            init_solution = init_solution + sol.commands
        
        optimized_commands: List[Command] = []
        for command_group in solution:
            optimized_commands = optimized_commands + [Command(PlotterPosition(command.command_detail.posX, command.command_detail.posY, command.command_detail.hitTimes)) for command in command_group.commands]
        
        non_optimized_commands: List[Command] = []
        for command_group in init_solution:
            non_optimized_commands = non_optimized_commands + [Command(PlotterPosition(command.command_detail.posX, command.command_detail.posY, command.command_detail.hitTimes)) for command in command_group.commands]
        
        print(f"Normal: {calculate_value_of_commands(non_optimized_commands)}, Optimized: {calculate_value_of_commands(optimized_commands)}")
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
        
        if len(proposed_solution) > 5:
            optimizer = PlotioTabuSearch(proposed_solution.copy(), int(math.sqrt(len(proposed_solution))), calculate_value_function=calculate_value, calculate_value_after_move=calculate_value_after_move, maximum_neighbors=min(50, len(proposed_solution)), random_neighbors=True, optimizer_settings=OptimizerSettings(True, False))
            optimizer.optimize(max(min(len(proposed_solution) * 20, 50*1000), 2000), 50)
            optimized = optimizer.best_solution

            optim_value = calculate_value(optimized)
            xy_value = calculate_value(proposed_solution)
            
            print(f"PROP: Normal: {xy_value}, Optimized: {optim_value}")
            return optimized, optim_value
        return proposed_solution, calculate_value(proposed_solution)

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
        optimizer = SimulatedAnnealing(extracted_groups.copy(), Conditions(1000, 2, 0.1, 0.97, int(math.sqrt(len(extracted_groups))), annealing= Annealing.linear))
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
