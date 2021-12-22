import enum
from typing import List, Optional
from src.plotter.domain.plotter_position import PlotterPosition

class CommandStatus(enum.Enum):
    Pending = 'Pending'
    Running = 'Running'
    Completed = 'Completed'
    Aborted = 'Aborted'

class Command:
    def __init__(self, position: PlotterPosition) -> None:
        self.position: PlotterPosition = position
        self.status: CommandStatus = CommandStatus.Pending

    def can_send_command(self):
        return self.status == CommandStatus.Pending

    def is_running_command(self):
        return self.status == CommandStatus.Running

    def try_send_command(self):
        if(self.status == CommandStatus.Pending or self.status == CommandStatus.Aborted):
            self.status = CommandStatus.Running
            return True
        return False
        
    def send_command(self):
        if(self.status == CommandStatus.Pending or self.status == CommandStatus.Aborted):
            self.status = CommandStatus.Running
            
    def try_complete_command(self):
        if(self.status == CommandStatus.Running):
            self.status = CommandStatus.Completed
            return True
        return False
    
    def complete_command(self):
        if(self.status == CommandStatus.Running):
            self.status = CommandStatus.Completed
        
    def try_abort_command(self):
        if(self.status == CommandStatus.Running):
            self.status = CommandStatus.Aborted
            return True
        return False
    
    def abort_command(self):
        if(self.status == CommandStatus.Running):
            self.status = CommandStatus.Aborted
