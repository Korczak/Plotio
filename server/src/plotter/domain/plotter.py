import enum
from typing import List, Optional
from src import plotter
from src.plotter.domain.command import Command

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

    def __init__(self, status: PlotterStatus, position: PlotterPosition, plotter_mode: PlotterMode, work_mode: WorkMode, project: Project) -> None:
        self.status: PlotterStatus = status
        self.position: PlotterPosition = position
        self.plotter_mode = plotter_mode
        self.work_mode = work_mode
        self.project: Project = project

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
        
        return self.project.get_current_command()
    
    def get_next_command(self) -> Command:
        if(self.work_mode != WorkMode.Automatic):
            return None
        if(self.project is None):
            return None
        if(self.project.is_active is False):
            return None
        
        return self.project.get_next_command()
        
    def send_current_command(self):
        if(self.project is None):
            raise Exception("Project is null")
        
        self.project.send_current_command()
        
    def complete_current_command(self):
        if(self.project is None):
            raise Exception("Project is null")
        
        self.project.complete_current_command()
        
        