import enum
from typing import List, Optional

from pubsub import pub
from src import plotter
from src.events.events_name import EventsName
from src.plotter.domain.alarm import Alarm, AlarmType
from src.plotter.domain.command import Command
from src.plotter.domain.command_details import CommandDetails

from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.domain.project import Project

class PlotterMode(enum.Enum):
    Work = 'Work'
    Simulation = 'Simulation'

class WorkMode(enum.Enum):
    Automatic = 'Automatic'
    Manual = 'Manual'

class PlotterStatus(enum.Enum):
    Connected= 'Connected'
    Disconnected= 'Disconnected'

class Plotter:
    def __init__(self, status: PlotterStatus) -> None:
        self.status: PlotterStatus = status
        self.position: PlotterPosition = PlotterPosition(0, 0, 0)
        self.plotter_mode = PlotterMode.Simulation
        self.work_mode = WorkMode.Manual
        self.project: Optional[Project] = None
        self.alarm: Alarm = None
        self.urgent_command: Command = None

    def __init__(self, status: PlotterStatus, position: PlotterPosition, plotter_mode: PlotterMode, work_mode: WorkMode, project: Project, alarm: Alarm, urgent_command: Command) -> None:
        self.status: PlotterStatus = status
        self.position: PlotterPosition = position
        self.plotter_mode = plotter_mode
        self.work_mode = work_mode
        self.project: Project = project
        self.alarm: Alarm = alarm
        self.urgent_command: Command = urgent_command

    def moveTo(self, position: PlotterPosition):
        self.position = position

    def is_work_mode(self):
        return self.plotter_mode == PlotterMode.Work
    
    def setWorkMode(self) -> bool:
        if(self.status == PlotterStatus.Connected):
            self.plotter_mode = PlotterMode.Work

    def setSimulationMode(self):
        self.plotter_mode = PlotterMode.Simulation

    def pause_project(self):
        if(self.project is not None):
            self.project.pause_project()
        self.work_mode = WorkMode.Manual

    def stop_project(self):        
        if(self.project is not None):
            self.project.stop_project()
        self.work_mode = WorkMode.Manual

    def start_project(self):
        if(self.project is not None):
            if(self.project.start_project()):
                self.work_mode = WorkMode.Automatic

    def complete_project(self):
        if(self.project is not None):
            self.project.complete_project()
            self.work_mode = WorkMode.Manual
            
            

    def add_project(self, project: Project):
        if(self.project is not None):
            self.project.stop_project()
        self.project = project

    def restore_project(self, num_of_commands):
        if(self.project is not None):
            self.project.complete_commands(num_of_commands)
            pub.sendMessage(EventsName.ProjectRestored)        

    def connect(self):
        self.status = PlotterStatus.Connected

    def disconnect(self):
        self.status = PlotterStatus.Disconnected
        if(self.project is not None):
            self.project.pause_project()

    def is_connected(self):
        return self.status == PlotterStatus.Connected

    def get_current_command(self) -> Command:
        if(self.work_mode != WorkMode.Automatic):
            return None
        if(self.project is None):
            return None
        if(self.project.is_active is False):
            return None
        
        return self.project.get_current_command()
    
    def get_next_command(self) -> Command:
        if(self.urgent_command != None):
            return self.urgent_command
        if(self.work_mode != WorkMode.Automatic):
            return None
        if(self.project is None):
            return None
        if(self.project.is_active is False):
            return None
        
        return self.project.get_next_command()
        
    def send_current_command(self):
        if(self.project is None):
            return None
        
        self.project.send_current_command()
        
    def complete_current_command(self):
        if(self.project is None):
            return None
        
        self.project.complete_current_command()
        
        if self.project.is_completed_project():
            self.complete_project()
        
    def is_alarm_active(self):
        if self.alarm != None and self.alarm.enabled == True:
            return True
        return False    
    
    def set_alarm(self, alarm: Alarm):
        self.alarm = alarm
        self.pause_project()
        
    def reset_alarm(self):
        self.alarm.disable_alarm()
        self.urgent_command = Command(CommandDetails("RESET"))
        
    def ignore_alarm(self):
        self.alarm.ignore_alarm(10)
        self.work_mode = WorkMode.Manual